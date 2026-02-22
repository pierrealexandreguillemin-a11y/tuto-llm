# Guide de contribution

## Prérequis

- Python 3.10+
- Git

## Installation

```bash
cd "tuto llm"
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate sur Windows
pip install -r requirements.txt
pip install -e .
pre-commit install --hook-type pre-commit --hook-type commit-msg --hook-type pre-push
```

## Normes qualité

Ce projet suit des normes ISO strictes adaptées au contexte éducatif.

### ISO 5055 — Qualité du code

- **Linter** : `ruff check src/ tests/`
- **Formatter** : `ruff format src/ tests/`
- **Types** : `mypy src/`
- Zéro erreur requise avant commit

### ISO 25010 — Maintenabilité

- Complexité cyclomatique max **15** (C901)
- Le code éducatif est naturellement verbeux, d'où un seuil plus élevé

### ISO 29119 — Tests

- **Couverture** : >= 70% sur `src/`
- **Tests unitaires** : `pytest tests/test_core.py tests/test_data.py tests/test_training.py` (115 tests)
- **Smoke tests** : `pytest tests/test_notebooks.py -m slow`
- Commande complète : `pytest tests/ --cov=src --cov-fail-under=70`

### ISO 27001 — Sécurité

- Ne jamais committer de secrets (.env, clés API, etc.)
- `pip-audit` vérifie les vulnérabilités des dépendances
- `gitleaks` détecte les secrets dans le code

### ISO 12207 — Cycle de vie

Commits conventionnels obligatoires :

| Préfixe | Usage |
|---------|-------|
| `feat:` | Nouvelle fonctionnalité |
| `fix:` | Correction de bug |
| `test:` | Ajout/modification de tests |
| `docs:` | Documentation |
| `chore:` | Maintenance, config |
| `refactor:` | Refactoring sans changement fonctionnel |

### ISO 42001 — Gouvernance IA

- Chaque notebook doit citer ses sources (microgpt.py, vidéo Karpathy, etc.)
- Les claims techniques doivent être vérifiables contre le code source
- Voir `docs/AI_POLICY.md` pour la politique complète

## Workflow de développement

1. Créer une branche depuis `master`
2. Modifier le code
3. Vérifier : `pre-commit run --all-files`
4. Tester : `pytest tests/ -v --cov=src --cov-fail-under=70`
5. Committer avec un message conventionnel
6. Ouvrir une Pull Request

## Architecture

Les **notebooks** contiennent le code inline pour la pédagogie.
Le dossier **src/tuto_llm/** duplique les fonctions clés pour permettre
les tests unitaires. Les deux doivent rester synchronisés.

```
src/tuto_llm/
  core.py       # softmax, mat_vec, forward_llm, generer_llm...
  data.py       # charger_dataset, nettoyer_mot, valider_vocab, formater_training
  training.py   # forward_with_cache, backward_llm, cross_entropy_loss, calcul_loss
  vocab.py      # VOCAB, char_to_id, id_to_char
```
