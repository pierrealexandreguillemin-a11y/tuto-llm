# Politique de gouvernance IA (ISO/IEC 42001:2023)

## 1. Objectif

Ce document définit la politique de gouvernance IA pour le projet
Tuto LLM, un cours éducatif enseignant les bases des LLM aux 10-14 ans.

## 2. Périmètre

Le projet ne déploie **aucun modèle IA en production**. Il s'agit
exclusivement de code éducatif démontrant les concepts. La gouvernance
porte sur la **qualité et la fiabilité du contenu pédagogique**.

## 3. Risques identifiés

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Hallucination technique | Moyen | Haut | Citation des sources, vérification contre le code |
| Simplification excessive | Moyen | Moyen | Notes "En vrai..." dans les notebooks |
| Code non fonctionnel | Faible | Haut | Smoke tests automatisés sur les 6 notebooks |
| Confusion pédagogique | Moyen | Moyen | Analogies testées, progression logique |

## 4. Sources autorisées

Tout contenu technique doit être vérifiable contre ces sources :

1. **microgpt.py** — Le script source de Karpathy
   https://gist.github.com/karpathy/8627fe009c40f57531cb18360106ce95

2. **Vidéo "Let's build GPT"** — Explication complète de l'architecture
   https://www.youtube.com/watch?v=kCc8FmEb1nY

3. **"Attention Is All You Need"** — Article fondateur des Transformers
   Vaswani et al., 2017, arXiv:1706.03762

4. **3Blue1Brown - Neural Networks** — Visualisations pédagogiques
   https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi

5. **PokéAPI** — Source des noms de Pokémon (dataset d'entraînement)
   https://pokeapi.co/
   (c) Nintendo / Creatures Inc. / GAME FREAK inc. — usage éducatif uniquement

## 5. Règles anti-hallucination

1. **Chaque claim technique** dans les notebooks doit correspondre
   à une implémentation vérifiable dans le code ou dans les sources citées.

2. **Les analogies** (lancer au panier, filtre Instagram, salle de classe,
   chaîne de dominos) sont explicitement marquées comme des simplifications.

3. **Les chiffres** (nombre de paramètres, comparaisons avec GPT-4)
   doivent être sourcés ou calculés dans le code.

4. **Les simplifications** sont documentées : le tuto indique ce qui
   est omis (autograd, Adam, multi-couches, GPU, RLHF, etc.) et pourquoi.
   Le notebook 06 inclut des sections "En vrai..." détaillant les
   différences avec les vrais LLM.

## 6. Citations dans les notebooks

Chaque notebook doit inclure une cellule finale de citations avec :
- Les sources utilisées pour le contenu de cette leçon
- Les liens vers le code source de référence
- Les crédits pour les analogies ou visualisations empruntées

## 7. Pratiques pédagogiques

Les notebooks suivent des conventions documentées dans
`docs/PEDAGOGICAL_PRACTICES.md`, basées sur 7 sources de référence
(Capytale, EPFL, jupyter4edu, Callysto, ML for Kids, Kaggle Learn).

Contrôles appliqués :
- 18 exercices interactifs (4+3+3+2+3+3) avec variables modifiables
- Règle Callysto : max 4 cellules entre exercices
- Scaffolding progressif (niveaux 1 à 5)
- Rappel Jupyter + séparateurs visuels dans chaque notebook

## 8. Processus de vérification

1. Les notebooks sont exécutés automatiquement (smoke tests)
2. Les fonctions extraites sont testées unitairement
3. La revue de contenu vérifie les citations contre les sources
4. Tout nouveau contenu technique nécessite une source vérifiable
5. Audit pédagogique : conformité Callysto, exercices, séparateurs
