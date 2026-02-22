# Référence des normes ISO appliquées

Ce document décrit les normes ISO appliquées au projet Tuto LLM
et leur implémentation concrète.

## Vue d'ensemble

| Norme | Focus | Outil | Seuil |
|-------|-------|-------|-------|
| ISO/IEC 5055:2021 | Qualité du code | ruff, mypy | 0 erreur |
| ISO/IEC 25010:2023 | Maintenabilité | ruff C901 | Complexité ≤ 15 |
| ISO/IEC 29119:2022 | Tests | pytest, coverage | Couverture ≥ 70% |
| ISO/IEC 27001:2022 | Sécurité | gitleaks, pip-audit | 0 secret, 0 CVE |
| ISO/IEC 12207:2017 | Cycle de vie | commitizen | Commits conventionnels |
| ISO/IEC 42001:2023 | Gouvernance IA | revue manuelle | Citations sources |

---

## ISO/IEC 5055:2021 — Qualité automatisée du code

**Objectif** : Mesurer et maintenir la qualité structurelle du code source.

**Implémentation** :
- Ruff lint avec règles E, W, F, I, UP, B, C901, S, SIM
- Mypy pour la vérification de types (Python 3.10+)
- Appliqué sur `src/` et `tests/`

**Vérification** : `ruff check src/ && mypy src/`

---

## ISO/IEC 25010:2023 — Qualité produit (Maintenabilité)

**Objectif** : Garantir que le code reste compréhensible et modifiable.

**Implémentation** :
- Complexité cyclomatique maximale : **15** (C901)
- Seuil adapté au contexte éducatif (code volontairement explicite)
- Projets comparables utilisent 10 (pocket_arbiter) ou 10 (chess-app)

**Vérification** : Intégré dans `ruff check`

---

## ISO/IEC 29119:2022 — Tests logiciels

**Objectif** : Assurer la fiabilité par des tests systématiques.

**Implémentation** :
- Tests unitaires sur `src/tuto_llm/` (115 tests : 42 core + 53 data + 20 training)
- Smoke tests sur les 6 notebooks (exécution complète)
- Couverture minimale : **70%** sur `src/` (100% atteint)
- Proportionné au contexte éducatif (vs 80% pour pocket_arbiter)

**Vérification** : `pytest tests/ --cov=src --cov-fail-under=70`

---

## ISO/IEC 27001:2022 — Sécurité de l'information

**Objectif** : Protéger contre les fuites de données et vulnérabilités.

**Implémentation** :
- Gitleaks en pre-commit (détection de secrets)
- pip-audit en pre-push (vulnérabilités des dépendances)
- Règles Bandit via ruff (S prefix)
- .gitignore exclut .env et fichiers sensibles

**Vérification** : `gitleaks protect --staged` + `pip-audit`

---

## ISO/IEC 12207:2017 — Cycle de vie logiciel

**Objectif** : Standardiser le processus de développement.

**Implémentation** :
- Commits conventionnels via commitizen
- Types : feat, fix, test, docs, chore, refactor
- Validation en hook commit-msg

**Vérification** : `cz check --commit-msg-file`

---

## ISO/IEC 42001:2023 — Gouvernance IA

**Objectif** : Assurer la transparence et la fiabilité du contenu IA.

**Implémentation** :
- Citations sources dans chaque notebook
- Vérification anti-hallucination des claims techniques
- Politique documentée dans `docs/AI_POLICY.md`

**Sources référencées** :
- [microgpt.py](https://gist.github.com/karpathy/8627fe009c40f57531cb18360106ce95) — Andrej Karpathy
- [Vidéo "Let's build GPT"](https://www.youtube.com/watch?v=kCc8FmEb1nY) — Andrej Karpathy
- [3Blue1Brown - Neural Networks](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi)

**Vérification** : Revue manuelle des notebooks
