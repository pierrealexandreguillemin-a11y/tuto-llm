# Tuto LLM - Claude Code Memory

> Cours progressif pour créer un mini-LLM (10-14 ans)
> Normes : ISO 5055, 25010, 29119, 27001, 12207, 42001

## Commandes

- `PYTHONPATH=src python -m pytest tests/ -v` : Lancer tous les tests
- `PYTHONPATH=src python -m pytest tests/ --cov=src --cov-fail-under=70` : Tests avec couverture 70%
- `PYTHONPATH=src python -m pytest tests/ -m "not slow"` : Tests rapides (sans notebooks)
- `python -m ruff check src/` : Lint Python (ISO 5055)
- `python -m ruff format src/ tests/` : Formatter le code
- `python -m mypy src/` : Vérification de types
- `python -m pre_commit run --all-files` : Tous les hooks qualité

## Style de code

- Python 3.10+ avec type hints
- Docstrings Google style pour fonctions publiques
- Imports : stdlib, third-party, local (séparés par ligne vide)
- Max 88 caractères par ligne (ruff default)
- Complexité cyclomatique max 15 (code éducatif)

## Structure du projet

```
data/               # Datasets pour entraînement
  prenoms.txt       # ~30k prénoms INSEE (a-z)
  dinosaures.txt    # ~1.5k noms de dinosaures (a-z)
  pokemon.txt       # ~1k noms Pokémon (a-z, (c) Nintendo, usage éducatif)
  haiku.csv         # 1k haiku (usage futur, vocab étendu)
notebooks/          # 6 leçons Jupyter (code inline pour pédagogie)
src/tuto_llm/       # Fonctions extraites pour tests unitaires
  core.py           # softmax, mat_vec, forward_llm, generer_llm...
  data.py           # charger_dataset, charger_csv, nettoyer_mot, valider_vocab, formater_training
  training.py       # forward_with_cache, backward_llm, cross_entropy_loss, calcul_loss
  vocab.py          # VOCAB, char_to_id, id_to_char
tests/              # Tests unitaires + smoke tests notebooks
  test_core.py      # 42 tests sur les fonctions extraites
  test_data.py      # 53 tests (unitaires + intégration données)
  test_training.py  # 20 tests (unitaires + vérification numérique gradients)
  test_notebooks.py # Exécution des 6 notebooks (marqués slow)
scripts/            # Scripts utilitaires
  build_datasets.py # Pipeline reproductible de construction des datasets
docs/               # Documentation ISO et gouvernance IA
  DATASETS.md       # Référence complète des datasets (12 documentés)
```

## Conformité ISO (OBLIGATOIRE)

- **ISO 27001** : Jamais lire .env, secrets/, *.pem, *.key
- **ISO 29119** : Coverage >= 70% sur src/, tests pour code exécutable
- **ISO 25010** : Complexité cyclomatique <= 15
- **ISO 12207** : Commits conventionnels (feat/fix/test/docs/chore/refactor)
- **ISO 42001** : Citations obligatoires dans les notebooks, anti-hallucination
- **ISO 5055** : Ruff lint + mypy sans erreur

## Workflow

1. Lire le fichier AVANT de le modifier
2. Exécuter les tests après chaque modification
3. Ne jamais réduire la couverture de tests
4. Les notebooks gardent leur code inline (pédagogie)
5. src/ duplique les fonctions pour les tests uniquement

## Références

- @README.md : Vision pédagogique + état du projet
- @docs/DATASETS.md : Référence complète des datasets et audit qualité
- @docs/AI_POLICY.md : Politique de gouvernance IA
- @docs/ISO_STANDARDS_REFERENCE.md : Référence des normes ISO
- @CONTRIBUTING.md : Guide de contribution
