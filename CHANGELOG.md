# Changelog

Toutes les modifications notables de ce projet sont documentées ici.
Format basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/),
versionné selon [Conventional Commits](https://www.conventionalcommits.org/fr/).

## [1.4.0] - 2026-02-22

Intégration du dataset Pokémon pré-généré, préparation de l'héritage
entre notebooks (gitignore des JSON intermédiaires).

### Added

- **`data/pokemon.txt`** : 1 009 noms de base Pokémon (a-z, triés).
  Source : PokéAPI. Noms de base uniquement (avant le premier tiret).
  (c) Nintendo / Creatures Inc. / GAME FREAK inc., usage éducatif.
- **`tests/test_data.py::TestIntegrationPokemon`** : 7 tests
  (taille, a-z, doublons, tri, min_len, vocab, formatage).

### Changed

- **`scripts/build_datasets.py`** : Ajout `build_pokemon()` avec
  User-Agent, extraction noms de base, constante `MIN_POKEMON_LEN`.
  Pipeline passe de 3 à 4 datasets.
- **`docs/DATASETS.md`** : Pokémon déplacé de "extensions possibles"
  vers "Datasets intégrés" (section 4) avec avertissement copyright.
- **`README.md`** : Pokémon au tableau datasets, compteurs mis à jour
  (115 tests, 4 datasets, 8 autres documentés).
- **`CLAUDE.md`** : `pokemon.txt` ajouté à la structure, compteurs.
- **`CONTRIBUTING.md`** : Compteur tests mis à jour.
- **`docs/ISO_STANDARDS_REFERENCE.md`** : 108 → 115 tests.
- **`.gitignore`** : Ajout `data/nb*.json` (fichiers intermédiaires
  notebooks, préparation héritage entre notebooks).

### Removed

- **`scripts/_benchmark_nb.py`** : Fichier orphelin de benchmark
  (3 erreurs ruff, non prévu dans le projet).

### Metrics

| Métrique | Valeur |
|----------|--------|
| Tests | 115 pass (42 core + 53 data + 20 training) |
| Couverture src/ | 100% (seuil : 70%) |
| Erreurs ruff | 0 |
| Erreurs mypy | 0 |
| Datasets intégrés | 4 (prénoms, dinosaures, pokémon, haiku) |

---

## [1.3.0] - 2026-02-22

Entraînement réel du mini-LLM : rétropropagation analytique, SGD en ligne,
génération de prénoms appris sur 10 000 prénoms INSEE.

### Added

- **`notebooks/06_entrainer_le_modele.ipynb`** : Notebook d'entraînement
  complet. Forward avec cache, backward analytique (7 étapes), boucle SGD
  sur 10k prénoms × 3 epochs. Sections "En vrai..." sur GPU, Adam, RLHF.
- **`src/tuto_llm/training.py`** : Module d'entraînement avec
  `cross_entropy_loss`, `forward_with_cache`, `backward_llm`, `calcul_loss`.
- **`tests/test_training.py`** : 20 tests (4 cross-entropy + 4 forward +
  8 backward avec vérification numérique + 4 calcul_loss).

### Changed

- **`tests/test_notebooks.py`** : Ajout notebook 06 avec timeout étendu
  (600s preprocessor, 660s subprocess) pour l'entraînement.
- **`notebooks/05_mon_premier_llm.ipynb`** : Lien vers leçon 6 ajouté.
- **`docs/DATASETS.md`** : Section "Entraînement" mise à jour (v1.3.0),
  ajout audit des temps de computation (6 notebooks) et section
  "Projet de niveau 2" (PyTorch, scaling, vocabulaire étendu).
- **`docs/AI_POLICY.md`** : 5 → 6 notebooks, analogie "chaîne de
  dominos" ajoutée, sections "En vrai..." documentées.
- **`docs/ISO_STANDARDS_REFERENCE.md`** : 26 → 108 tests, 5 → 6 notebooks.
- **`CONTRIBUTING.md`** : Ajout `training.py` dans l'architecture,
  tous les fichiers de tests listés.

### Fixed

- **`.pre-commit-config.yaml`** : Le hook pre-push pytest ne lançait
  que `test_core.py` (42 tests, 32% coverage). Corrigé pour inclure
  les 3 fichiers de tests (108 tests, 100% coverage).

### Metrics

| Métrique | Valeur |
|----------|--------|
| Tests | 108 pass (42 core + 46 data + 20 training) |
| Couverture src/ | 100% (seuil : 70%) |
| Erreurs ruff | 0 |
| Erreurs mypy | 0 |
| Notebooks exécutables | 6/6 |

### Roadmap

- [x] **Entraînement réel** : notebook 06 avec backprop analytique (v1.3.0)
- [ ] **Notebook dinosaures** : entraîner sur dinosaures.txt
- [ ] **nbval** : validation des outputs attendus

---

## [1.2.0] - 2026-02-21

Intégration de 3 datasets, pipeline reproductible, documentation exhaustive,
et module de chargement/formatage pour l'entraînement du mini-LLM.

### Added

- **`data/prenoms.txt`** : ~30 800 prénoms INSEE nettoyés (lowercase, sans
  accents, a-z, min 2 chars). Source : INSEE fichier des prénoms depuis 1900.
- **`data/dinosaures.txt`** : ~1 524 noms de dinosaures nettoyés. Source :
  gist Dvelezs94. Inspiré du cours makemore de Karpathy.
- **`data/haiku.csv`** : 1 000 haiku (échantillon, licence incertaine).
  Stocké pour usage futur, nécessite vocab étendu.
- **`src/tuto_llm/data.py`** : Module utilitaire avec `charger_dataset`,
  `charger_csv`, `nettoyer_mot`, `valider_vocab` (avec `min_len`),
  `formater_training` (type hints, docstrings Google style).
- **`tests/test_data.py`** : 46 tests (21 unitaires + 12 intégration
  prénoms/dinosaures + 3 intégration haiku + 4 CSV + 4 formatage + 2 min_len).
- **`docs/DATASETS.md`** : Référence complète des datasets intégrés,
  compatibles char-level, et autres concepts ML (12 datasets documentés).
- **`scripts/build_datasets.py`** : Pipeline reproductible de téléchargement
  et nettoyage des 3 datasets (dinosaures, prénoms, haiku).

### Metrics

| Métrique | Valeur |
|----------|--------|
| Tests | 88 pass (42 core + 46 data) |
| Couverture src/ | 100% (seuil : 70%) |
| Erreurs ruff | 0 |
| Erreurs mypy | 0 |
| Datasets intégrés | 3 (prenoms, dinosaures, haiku) |
| Datasets documentés | 12 |

---

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

- [x] **Entraînement réel** : notebook 06 avec rétropropagation analytique,
  SGD en ligne, 10k prénoms × 3 epochs (v1.3.0).
- [x] **Extraction `rand_vector`** : extraite dans `core.py` avec
  9 tests unitaires (v1.1.0).
- [x] **CI/CD** : workflow GitHub Actions avec 6 jobs parallèles,
  actions pinnées sur SHA, notebook smoke tests inclus (v1.1.0).
- [x] **Datasets d'entraînement** : 3 datasets intégrés (prénoms,
  dinosaures, haiku), pipeline reproductible, 46 tests, documentation
  exhaustive de 12 datasets (v1.2.0).
- [ ] **Notebook dinosaures** : entraîner sur dinosaures.txt pour montrer
  que le même modèle apprend des distributions différentes.
- [ ] **nbval** : mentionné dans le plan initial mais non installé.
  Les smoke tests via nbconvert suffisent pour le moment. nbval pourrait
  être ajouté pour valider les outputs attendus des cellules.
