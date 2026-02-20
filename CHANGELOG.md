# Changelog

Toutes les modifications notables de ce projet sont documentées ici.
Format basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/),
versionné selon [Conventional Commits](https://www.conventionalcommits.org/fr/).

## [1.0.0] - 2026-02-20

Normalisation ISO complète du projet. Le repo passe de 5 notebooks bruts
sans infrastructure à un projet conforme aux normes ISO 5055, 25010,
29119, 27001, 12207 et 42001.

### Added

- **Infrastructure projet** : `pyproject.toml` (ruff, mypy, pytest,
  coverage, commitizen), `requirements.txt`, structure `src/tests/docs/`
- **Code extrait** : `src/tuto_llm/core.py` (softmax, mat_vec, vec_add,
  relu, rand_matrix, calculer_probas, forward_llm, generer_llm) et
  `src/tuto_llm/vocab.py` (VOCAB, VOCAB_SIZE, char_to_id, id_to_char)
- **32 tests unitaires** dans `tests/test_core.py` : TestSoftmax (6),
  TestMatVec (3), TestVecAdd (4), TestRelu (4), TestRandMatrix (3),
  TestCalculerProbas (3), TestForwardLlm (5), TestGeneration (4)
- **Smoke tests notebooks** dans `tests/test_notebooks.py` : exécution
  des 5 notebooks via nbconvert
- **Pre-commit hooks** (`.pre-commit-config.yaml`, 13 hooks, 3 stages) :
  - pre-commit : gitleaks, ruff lint+format, mypy, check-yaml/json/toml,
    trailing-whitespace, end-of-file-fixer, check-merge-conflict
  - commit-msg : commitizen (commits conventionnels)
  - pre-push : pytest-cov 70%, pip-audit
- **Documentation ISO** : `CLAUDE.md`, `CONTRIBUTING.md`,
  `docs/ISO_STANDARDS_REFERENCE.md`, `docs/AI_POLICY.md`
- **Citations sources (ISO 42001)** dans les 5 notebooks : microgpt.py,
  vidéo "Let's build GPT", "Attention Is All You Need", 3Blue1Brown

### Fixed

- ~150 accents français manquants dans README.md et les 5 notebooks
  (modèle, leçon, entraîne, mémoire, réseau, paramètre, etc.)
- `NUM_HEADS=2` alors qu'une seule tête implémentée dans notebook 05
  — aligné sur `NUM_HEADS=1`
- Formule de paramètres : 4 matrices -> 3 matrices Q/K/V (pas Q/K/V/O)
- `/dev/null` dans test_notebooks.py incompatible Windows
  — remplacé par `tempfile.TemporaryDirectory()`
- `python -m jupyter nbconvert` — entry point cassé sur Windows
  — remplacé par `python -m nbconvert`
- PYTHONPATH manquant dans le hook pre-push pytest
- pip-audit scannait les packages globaux — scopé à `-r requirements.txt`
- Tests vacueux : `test_temperature` (seulement `isinstance`)
  — remplacé par un test de distribution réelle
- Lint notebooks : B007 (variable de boucle inutilisée),
  SIM108 (ternaire) — per-file-ignores pour code éducatif

### Metrics

| Métrique | Valeur |
|----------|--------|
| Tests | 32 pass |
| Couverture src/ | 99% (seuil : 70%) |
| Erreurs ruff | 0 |
| Erreurs mypy | 0 |
| Secrets détectés (gitleaks) | 0 |
| CVE détectées (pip-audit) | 0 |
| Notebooks exécutables | 5/5 |

### Normes ISO appliquées

| Norme | Contrôle | Outil |
|-------|----------|-------|
| ISO/IEC 5055:2021 | Qualité du code | ruff lint + mypy |
| ISO/IEC 25010:2023 | Maintenabilité | C901 complexité max 15 |
| ISO/IEC 29119:2022 | Tests | pytest, couverture >= 70% |
| ISO/IEC 27001:2022 | Sécurité | gitleaks, pip-audit |
| ISO/IEC 12207:2017 | Cycle de vie | commitizen, commits conventionnels |
| ISO/IEC 42001:2023 | Gouvernance IA | citations sources, anti-hallucination |

### Roadmap (tâches restantes)

- [ ] **Entraînement réel** : les poids du mini-LLM sont actuellement
  aléatoires. Ajouter un notebook d'entraînement sur le dataset `data/`
  pour produire des poids appris et des prénoms réalistes.
- [ ] **Extraction `rand_vector`** : la fonction `rand_vector` est
  présente dans le notebook 05 mais non extraite dans `src/tuto_llm/`.
  Utilisée uniquement localement, elle pourrait être ajoutée à `core.py`
  pour la cohérence de l'extraction.
- [ ] **CI/CD** : ajouter un workflow GitHub Actions (`.github/workflows/`)
  pour reproduire le pipeline pre-commit + pytest sur chaque Pull Request.
  Cela garantirait la conformité ISO même sans hooks locaux installés.
- [ ] **nbval** : mentionné dans le plan initial mais non installé.
  Les smoke tests via nbconvert suffisent pour le moment. nbval pourrait
  être ajouté pour valider les outputs attendus des cellules.
