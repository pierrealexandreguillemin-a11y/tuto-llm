# Changelog

Toutes les modifications notables de ce projet sont documentées ici.
Format basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/),
versionné selon [Conventional Commits](https://www.conventionalcommits.org/fr/).

## [1.1.0] - 2026-02-21

Cohérence du projet : extraction complète des fonctions, CI/CD,
et audit qualité rigoureux avec corrections de tous les findings.

### Added

- **`rand_vector`** extraite du notebook 05 dans `src/tuto_llm/core.py`
  avec type hints et docstring Google style
- **10 nouveaux tests** : TestRandVector (9), test_arret_sur_point (1)
  — total : 42 tests (était 32)
- **GitHub Actions CI** (`.github/workflows/ci.yml`) : 6 jobs parallèles
  lint, format, mypy, tests+coverage, notebook smoke tests, pip-audit
- **`[build-system]`** ajouté dans `pyproject.toml` (PEP 517)

### Fixed

- `vec_add` : divergence `strict=True` (core.py) vs `strict=False`
  (notebook) documentée comme intentionnelle
- GitHub Actions pinnées sur SHA complets (ISO 27001 supply-chain)
- `requirements.txt` : `>=` remplacé par `~=` (bornes compatibles)
- `pip install -e .` ajouté dans CI pour mypy et tests
- Notebook smoke tests ajoutés dans CI (étaient exclus)
- Test du early-stop `generer_llm` (ligne 194 était non couverte)
- Edge cases ajoutés : `rand_vector(scale=0)`, `rand_vector(-1)`

### Metrics

| Métrique | Valeur |
|----------|--------|
| Tests | 42 pass |
| Couverture src/ | 100% (seuil : 70%) |
| Erreurs ruff | 0 |
| Erreurs mypy | 0 |
| Secrets détectés (gitleaks) | 0 |
| CVE détectées (pip-audit) | 0 |
| Notebooks exécutables | 5/5 |
| Jobs CI | 6 |

---

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
- [x] **Extraction `rand_vector`** : extraite dans `core.py` avec
  9 tests unitaires (v1.1.0).
- [x] **CI/CD** : workflow GitHub Actions avec 6 jobs parallèles,
  actions pinnées sur SHA, notebook smoke tests inclus (v1.1.0).
- [ ] **nbval** : mentionné dans le plan initial mais non installé.
  Les smoke tests via nbconvert suffisent pour le moment. nbval pourrait
  être ajouté pour valider les outputs attendus des cellules.
