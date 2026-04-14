# Soutenance - callMeMaybe

## Pitch rapide (30-45s)

Ce projet prend des prompts en langage naturel et produit une sortie JSON structuree qui decrit une decision de function calling.  
Pour chaque prompt, je retourne un objet avec `prompt`, `name`, et `parameters`, conforme au schema des fonctions disponibles.  
J'ai organise le code en trois blocs: chargement/validation des donnees, generation de la decision, et orchestration CLI.

## Objectif du projet

- Transformer une demande utilisateur en appel de fonction exploitable par une machine.
- Garantir une sortie JSON parseable.
- Respecter les types attendus par le schema (`number`, `string`, `boolean`).
- Gérer proprement les erreurs d'entree et d'execution.

## Architecture du projet

- `src/models.py`
  - Modeles Pydantic (`FunctionDef`, `TestPrompt`, `FunctionCall`)
  - Validation structurelle des donnees
- `src/loader.py`
  - Chargement des fichiers JSON d'entree
  - Gestion des erreurs JSON/fichiers manquants
  - Sauvegarde du resultat final
- `src/generator.py`
  - Logique de selection de fonction
  - Construction des parametres selon le schema
- `src/__main__.py`
  - Point d'entree CLI
  - Boucle sur tous les prompts
  - Ecriture du fichier de sortie

## Pipeline d'execution

1. Charger `functions_definition.json` et `function_calling_tests.json`.
2. Initialiser le modele.
3. Pour chaque prompt:
   - choisir la fonction cible,
   - construire `parameters` conformes au schema,
   - instancier un `FunctionCall`.
4. Ecrire tous les resultats dans `data/output/function_calling_results.json`.

## Choix techniques defensables

- Utilisation de Pydantic pour fiabiliser les structures de donnees.
- Separation nette des responsabilites (models, loader, generator, main).
- Gestion explicite des exceptions pour eviter les crashs silencieux.
- Sortie JSON strictement formatee et directement exploitable.

## Gestion des erreurs

- Fichier introuvable -> `FileNotFoundError` avec message clair.
- JSON invalide -> `ValueError` explicite.
- Donnees non conformes au schema -> erreur de validation Pydantic.
- Cas d'extraction impossible -> erreur metier explicite.

## Commandes de demonstration

```bash
uv sync
make run
```

ou:

```bash
uv run python -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/function_calling_results.json
```

## Ce que je montre pendant la soutenance

- Le format des fichiers d'entree.
- Le passage prompt -> `FunctionCall`.
- Le fichier de sortie final et sa validite JSON.
- La conformite des types de `parameters` avec le schema.

## Questions probables et reponses courtes

- **Pourquoi Pydantic ?**  
  Pour valider automatiquement les structures et echouer proprement en cas de schema incorrect.

- **Comment garantis-tu la robustesse ?**  
  Validation stricte des entrees, erreurs explicites, et generation controlee de la sortie.

- **Comment verifier la conformite du resultat ?**  
  Le resultat est une liste de `FunctionCall` valides, avec les cles attendues et des types conformes.

- **Que se passe-t-il si les prompts changent ?**  
  Le pipeline reste le meme: selection de fonction puis generation des parametres selon le schema charge depuis le fichier de definitions.

## Conclusion (10s)

Le projet est structure, testable, et focalise sur la fiabilite: transformer du langage naturel en decisions de function calling JSON valides et exploitables.
