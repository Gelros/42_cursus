# Soutenance - callMeMaybe

## Pitch rapide (30-45s)

Ce projet transforme des prompts en langage naturel en decisions de function
calling au format JSON. Pour chaque prompt, la sortie contient `prompt`, `name`
et `parameters`, en respectant le schema des fonctions chargees.

## Objectifs du projet

- Convertir un texte utilisateur en appel de fonction exploitable par une machine.
- Garder une sortie JSON valide et coherente.
- Respecter les types attendus (`number`, `string`, `boolean`).
- Echouer rapidement avec des erreurs explicites.

## Architecture

- `src/models.py`: schemas Pydantic (`FunctionDef`, `TestPrompt`, `FunctionCall`)
- `src/loader.py`: gestion des fichiers JSON avec validation
- `src/generator.py`: selection de fonction et generation des parametres
- `src/__main__.py`: orchestration CLI et traitement en lot
- `llm_sdk/__init__.py`: chargement du modele local et inférence

## Pipeline d'execution

1. Charger `functions_definition.json` et les prompts de test.
2. Initialiser le modele.
3. Pour chaque prompt :
   - choisir la fonction cible,
   - generer des parametres types,
   - construire un `FunctionCall`.
4. Sauvegarder tous les resultats dans `data/output/function_calling_results.json`.

## Choix techniques defensables

- Pydantic garantit la validation des schemas.
- Separation claire des responsabilites par module.
- Gestion explicite des exceptions pour les entrees invalides.
- Fallbacks deterministes quand la generation LLM est instable.

## Gestion des erreurs

- Fichier manquant -> `FileNotFoundError`
- JSON invalide -> `ValueError`
- Schema invalide -> erreur de validation Pydantic
- Etat de generation invalide -> erreur d'execution explicite

## Commandes de demo

```bash
make install
make run
make lint
```

## Ce qu'il faut montrer en soutenance

- Format des fichiers d'entree et schema.
- Transformation d'un prompt en `FunctionCall`.
- Validite du JSON de sortie.
- Verification statique avec `flake8` et `mypy`.

## Q&R rapide

- **Pourquoi Pydantic ?**  
  Il valide les contrats de donnees et echoue clairement quand elles sont invalides.

- **Comment garantir la robustesse ?**  
  Verifications strictes en entree, erreurs explicites et fallbacks deterministes.

- **Comment verifier la qualite de sortie ?**  
  Modeles valides plus controles `flake8` et `mypy`.

- **Que se passe-t-il avec de nouveaux prompts ?**  
  Le meme pipeline s'applique, car le comportement est pilote par le schema d'entree.
