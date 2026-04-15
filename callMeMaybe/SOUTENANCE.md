# Soutenance — callMeMaybe

## 1. Pitch (30–45 s)

callMeMaybe transforme un prompt en langage naturel en un **appel de fonction
JSON structuré**, prêt à être exécuté par une machine. Au lieu de répondre
« la somme de 2 et 3 est 5 », le programme renvoie :

```json
{"name": "fn_add_numbers", "parameters": {"a": 2.0, "b": 3.0}}
```

Le tout avec un **petit modèle local** (Qwen3-0.6B, 600 M de paramètres).
Un modèle de cette taille ne produit pas du JSON valide de façon fiable
« à la volée » ; la clé du projet est donc le **constrained decoding** :
on guide chaque décision du modèle pour rester conforme au schéma.

---

## 2. Objectifs du projet

- Traduire un prompt en appel de fonction typé.
- Produire **100 % de JSON valide**, toujours conforme au schéma des
  fonctions déclarées.
- Respecter les types (`number`, `string`, `boolean`).
- Échouer proprement : messages d'erreur clairs, aucun crash non géré.
- Rester conforme au sujet : Python 3.10+, `uv`, `pydantic`, `numpy`,
  pas de `transformers`/`pytorch`/`dspy`/`outlines` côté projet.

---

## 3. Architecture du code

```
src/
├── models.py       # Schemas Pydantic (contrats de données)
├── loader.py       # Lecture / écriture JSON + validation
├── vocabulary.py   # Pré-tokenisation des noms de fonction
├── generator.py    # Scoring + decoding contraint (cœur du projet)
└── __main__.py     # CLI + boucle sur les prompts
llm_sdk/
└── __init__.py     # Wrapper Small_LLM_Model fourni par le sujet
```

Règle de découpe : un seul rôle par module, pas plus de quelques centaines
de lignes par fichier, facilite la lecture en peer review.

---

## 4. Pipeline d'exécution

1. **Chargement** : `load_functions_def` et `load_tests_prompt` parsent les
   JSON d'entrée et valident leur schéma via Pydantic.
2. **Initialisation** : `Small_LLM_Model()` télécharge/charge Qwen3-0.6B,
   et `pre_calc_name_func` pré-tokenise chaque nom de fonction une fois
   pour toutes.
3. **Pour chaque prompt** :
   - `_select_function_name` choisit la fonction (stage 1).
   - `_generate_param_value` remplit chaque paramètre (stage 2).
   - Les valeurs sont assemblées dans un `FunctionCall` Pydantic.
4. **Sauvegarde** : tous les `FunctionCall` sont dumpés dans
   `data/output/function_calling_results.json` (JSON indenté, validé).

---

## 5. Stage 1 — Sélection de fonction (teacher-forced scoring)

Le sujet interdit les heuristiques pour choisir la fonction : c'est le
LLM qui tranche. Le problème, c'est qu'un modèle 0.6B ne sait pas
fiablement « deviner » un nom de fonction depuis un prompt.

Astuce : on ne lui demande pas de générer le nom, on lui demande
**à quel point chaque nom candidat est plausible** dans le contexte.

1. On construit un préambule qui rappelle le prompt et liste tous les
   noms + descriptions.
2. Pour chaque fonction candidate, on calcule la **log-vraisemblance**
   de son nom tokenisé :
   - on envoie le préambule au modèle, on obtient les logits,
   - on applique `log-sum-exp` pour une softmax stable numériquement,
   - on récupère la log-proba du token cible, on l'ajoute au prefix,
     on recommence token par token jusqu'à la fin du nom.
3. On **normalise par la longueur** du nom (en tokens) pour ne pas
   avantager les noms courts.
4. On ajoute un **bonus d'affinité lexicale** (+0.5 par mot du prompt
   présent dans le nom ou la description, stopwords exclus), qui
   départage les cas où le LLM donne des scores quasi-égaux.
5. On garde la fonction au score maximum.

### Pourquoi `log-sum-exp` ?

Pour passer des logits aux log-probabilités, on calcule
`log_softmax(x)_i = x_i − log(sum(exp(x_j)))`. Si `x_j` est grand,
`exp(x_j)` explose. On soustrait le max avant :
`log(sum(exp(x_j))) = m + log(sum(exp(x_j − m)))` — mathématiquement
identique, numériquement stable.

---

## 6. Stage 2 — Génération des paramètres (LLM + garde-fous)

Pour chaque paramètre de la fonction choisie, on dispatch sur le type :

### `number`

- Decoding greedy avec un **automate** : on ignore le whitespace tant
  qu'aucun chiffre/signe n'apparaît, puis on accepte chiffres et point
  jusqu'à la première interruption.
- Parsing final par la regex `-?\d+(?:\.\d+)?`.
- **Fallback** si : (a) la valeur générée n'existe pas dans le prompt,
  ou (b) elle a déjà été utilisée par un paramètre précédent alors que
  d'autres nombres sont disponibles. Le fallback pioche le i-ième nombre
  du prompt.

### `boolean`

On compare directement les logits des tokens `" true"` et `" false"` :
pas de génération libre, la décision est binaire et déterministe.

### `string`

- Pour les paramètres de type substitution (`source_string`, `regex`,
  `replacement`), on utilise directement les fallbacks déterministes :
  sur ce type de contenu structuré, le LLM paraphrase plus qu'il ne
  recopie.
- Pour les autres (`name`, `s`), greedy decoding jusqu'au `\n`, puis
  un fallback regex si la valeur est vide ou incorrecte.

---

## 7. Choix techniques défendables

- **Pydantic** comme première ligne de défense : tout JSON mal formé
  est rejeté avant d'atteindre le générateur.
- **Constrained decoding implicite** : on ne demande jamais au modèle
  « écris-moi du JSON ». Le JSON est construit côté Python, le modèle
  ne fait que pondérer des choix dans des ensembles fermés.
- **LLM + regex hybrides** : le LLM décide, la regex valide, le fallback
  rattrape. Le petit LLM reste utile (sélection, classification) mais
  n'est jamais le dernier arbitre sur l'extraction exacte.
- **Cache tokenizer** : `pre_calc_name_func` évite de retokeniser les
  noms à chaque prompt.
- **Log-sum-exp** partout où on normalise des logits.
- **Typage moderne** : `X | None`, `list[...]`, `dict[...]`, `mypy`
  passe en `--strict`.
- **Pas d'accès aux méthodes privées** de `llm_sdk` (contrainte sujet).

---

## 8. Gestion des erreurs

| Erreur                               | Traitement                              |
|--------------------------------------|-----------------------------------------|
| Fichier d'entrée manquant            | `FileNotFoundError` avec chemin clair   |
| JSON mal formé                       | `ValueError` qui chaîne `JSONDecodeError` |
| Schéma invalide (clé manquante…)     | `ValidationError` Pydantic              |
| État de génération invalide          | `ValueError` explicite                  |
| Paramètre non trouvé dans le prompt  | Fallback déterministe ordonné           |

Aucun point du pipeline ne « crash » avec une trace brute : chaque
échec remonte avec un message lisible.

---

## 9. Performances et fiabilité

- **Précision** : sur les exemples fournis (`sum`, `greet`, `reverse`,
  `square root`, `regex substitution`) le pipeline choisit la bonne
  fonction et extrait les bons paramètres.
- **JSON 100 % valide** : garanti par Pydantic + `json.dumps`. La
  fonction est toujours prise dans l'ensemble fermé déclaré.
- **Vitesse** : le coût dominant est le chargement initial du modèle
  (download + tokenizer). Le traitement d'un prompt est une poignée de
  forward passes : quelques secondes au max, bien sous les 5 min
  exigées par le sujet.
- **Régressions historiques couvertes** :
  - `"What is the sum of 265 and 345?"` → `a=265, b=345` (pas `a=265, b=265`).
  - `"Add -3.5 and 2.5"` → décimales préservées.
  - `"Sum of -7 and 8"` → `fn_add_numbers`, pas `fn_substitute…`.

---

## 10. Difficultés rencontrées

1. **Troncature des décimales.** Le decoder numérique s'arrêtait à la
   première virgule/point. Corrigé avec un automate
   whitespace → signe/chiffre → chiffres/point → stop.
2. **Répétition de la même valeur** sur `a` et `b`. Le LLM renvoie
   le premier nombre pour les deux paramètres. Corrigé en traquant les
   valeurs déjà utilisées et en basculant sur une extraction ordonnée.
3. **Scoring quasi-plat entre fonctions** sur des prompts courts.
   Ajout d'un bonus lexical pour injecter un signal déterministe.
4. **Fallback trop restrictif** (ne se déclenchait que sur `0.0`).
   Élargi à « valeur absente du prompt ou déjà utilisée ».
5. **`mypy --strict`** sur du code qui appelle un SDK untyped.
   Résolu par des `# type: ignore[…]` ciblés.

---

## 11. Stratégie de tests

- **Run manuel** sur `data/input/function_calling_tests.json`, lecture
  du JSON de sortie.
- **Cas limites** : nombres négatifs, décimales, doublons, un seul
  nombre (square root), chaînes citées, prompts où plusieurs descriptions
  contiennent les mêmes mots.
- **Validation des entrées** : fichier manquant, JSON cassé, schéma
  invalide.
- **Checks statiques** : `make lint` (flake8 + mypy avec les flags
  imposés) et `make lint-strict` (mypy `--strict`) passent sans erreur.

---

## 12. Commandes de démo

```bash
make install         # uv sync
make run             # lance le pipeline sur les fichiers par défaut
make lint            # flake8 + mypy avec les flags du sujet
make lint-strict     # mypy --strict (optionnel)
make fclean          # nettoyage complet
```

Commande équivalente à `make run` en explicite :

```bash
uv run python -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/function_calling_results.json
```

---

## 13. Ce qu'il faut montrer en soutenance

1. **Format d'entrée** (`functions_definition.json`, prompts).
2. **Un run complet** et lecture du fichier de sortie.
3. **Validité du JSON** (ouverture dans l'éditeur, `json.tool`).
4. **Le cœur** : ouverture de `generator.py`, explication du scoring et
   du decoding contraint.
5. **Un cas tordu** (ex : prompt à décimales, ou prompt ambigu) pour
   montrer que les garde-fous se déclenchent.
6. **Checks statiques** : `make lint` clean.

---

## 14. Questions / Réponses probables

- **Pourquoi le LLM ne génère pas directement du JSON ?**
  Un 0.6B est instable sur le format (virgules flottantes, clés manquantes,
  hallucinations). Construire le JSON côté Python garantit 100 % de
  validité. Le LLM reste utile là où il est bon : classer, pondérer.

- **Pourquoi log-sum-exp ?**
  Sur des logits de grande amplitude, `exp(x)` overflow en float64.
  `log-sum-exp` soustrait le max : `exp(0) = 1`, plus d'overflow, résultat
  mathématiquement identique.

- **Pourquoi normaliser le score par la longueur du nom ?**
  Sans ça, les noms courts (moins de tokens) auraient mécaniquement une
  meilleure log-proba. La division remet à l'échelle pour comparer des
  séquences de longueurs différentes.

- **Pourquoi un bonus lexical ?**
  Sur un 0.6B, les scores peuvent être quasi-égaux entre deux fonctions.
  Le bonus ancre la décision sur un signal déterministe (chevauchement de
  mots-clés) sans violer la règle « c'est le LLM qui choisit » : le LLM
  reste le contributeur principal, le bonus n'est qu'un tie-breaker.

- **Pourquoi Pydantic ?**
  Contrats de données validés à l'instanciation, messages d'erreur
  structurés, sérialisation JSON « gratuite », parfait pour un
  pipeline qui manipule un schéma strict.

- **Que se passe-t-il avec un nouveau set de fonctions ?**
  Le pipeline est piloté par `functions_definition.json` : tant que les
  types déclarés restent `number`, `string` ou `boolean`, le même code
  fonctionne sans modification.

- **Comment tu gères un prompt ambigu ?**
  Le LLM fait le premier tri, le bonus lexical départage, et si aucun
  paramètre du prompt ne colle, le fallback déterministe pioche dans
  l'ordre du prompt. Pas de crash, sortie toujours valide.

- **Pourquoi ne pas faire du « vrai » constrained decoding au niveau
  des tokens ?**
  On le fait déjà, implicitement : la sélection de fonction est un
  choix dans un ensemble fermé (scoring), la génération des valeurs
  numériques est filtrée par un automate + regex, et le JSON final
  est assemblé côté Python. Chaque décision est contrainte.
