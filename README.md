# Tuto LLM - Créer son mini-LLM (pour les 10-14 ans)

> Cours progressif pour comprendre et construire un modèle de langage,
> inspiré de [microgpt.py](https://gist.github.com/karpathy/8627fe009c40f57531cb18360106ce95) d'Andrej Karpathy.

## Qu'est-ce que microgpt.py ?

L'implémentation la plus minimaliste possible d'un GPT en Python pur,
**sans aucune dépendance** (pas de PyTorch, NumPy, ou quoi que ce soit).

Karpathy résume :

> *"This file is the complete algorithm. Everything else is just efficiency."*

C'est vrai : l'algorithme est complet. Mais le code brut suppose de maîtriser
des notions avancées. Voici ce qu'il contient, ce que ça veut dire en langage
simple, et ce que ce tuto fait pour rendre chaque notion accessible.

---

## Ce que le code suppose -- et comment ce tuto le traduit

### 1. Les dérivées et la chaîne de dérivation

**Dans le code** : microgpt.py implémente un système d'"autograd" -- chaque
opération mathématique enregistre comment elle a été calculée, puis le programme
remonte toute la chaîne en sens inverse pour savoir "de combien chaque nombre
a contribué à l'erreur". C'est du calcul différentiel (programme de Terminale/Prépa).

**Traduction simple** : Imagine que tu rates un lancer au panier. Tu sais que
la balle est allée trop à droite. Tu corriges un petit peu à gauche au prochain
essai. Le "de combien corriger" c'est le gradient. La "chaîne de dérivation"
c'est le fait de remonter chaque étape du lancer (angle du bras, force, position)
pour savoir laquelle corriger.

**Dans le tuto** : La leçon 2 utilise directement cette analogie. On calcule la
correction (le gradient) de façon simplifiée, sans jamais écrire une dérivée.
L'élève voit la loss baisser et comprend le principe sans les maths.

---

### 2. Les multiplications matricielles

**Dans le code** : Quasiment toute l'intelligence du modèle passe par des
multiplications de matrices -- des grilles de nombres multipliées entre elles.
C'est de l'algèbre linéaire (programme de fac/école d'ingénieur).

**Traduction simple** : Une matrice c'est un "filtre" qui transforme une liste
de nombres en une autre liste de nombres. Comme un filtre Instagram qui
transforme les couleurs d'une photo : les pixels entrent, le filtre fait
ses calculs, de nouveaux pixels sortent. Ici les "pixels" ce sont les nombres
qui représentent les lettres.

**Dans le tuto** : Les leçons 3 et 5 font des multiplications matrice x vecteur
avec des boucles Python simples (`for i... for j...`). L'élève n'a pas besoin
de savoir ce qu'est une matrice -- il voit juste que des nombres entrent,
d'autres sortent, et ça donne des prédictions.

---

### 3. L'optimisation par descente de gradient

**Dans le code** : microgpt.py utilise l'optimiseur Adam, un algorithme avancé
qui ajuste les poids du modèle en tenant compte de la vitesse et de l'accélération
des corrections passées. Il inclut aussi un "learning rate decay" (la vitesse
de correction ralentit au fil du temps). C'est de l'optimisation numérique
(programme de Master/Doctorat).

**Traduction simple** : Au début de l'entraînement, le modèle fait des grosses
corrections parce qu'il est complètement perdu. Au fur et à mesure, il fait
des corrections de plus en plus fines, comme un sculpteur qui passe du marteau
au papier de verre. Adam, c'est un sculpteur intelligent qui se souvient de
ses gestes précédents pour mieux ajuster les suivants.

**Dans le tuto** : La leçon 2 utilise une descente de gradient basique avec un
seul paramètre (`vitesse`). Pas d'Adam, pas de decay -- juste "on corrige un
peu dans la bonne direction à chaque fois". L'élève voit que ça marche,
et c'est suffisant pour comprendre le principe.

---

### 4. Le softmax

**Dans le code** : La fonction softmax transforme des scores bruts (qui peuvent
être n'importe quel nombre, positif ou négatif) en probabilités (entre 0 et 1,
somme = 1). Elle utilise la fonction exponentielle, ce qui amplifie les
différences : un score un peu plus haut devient beaucoup plus probable.

**Traduction simple** : Imagine un vote. Chaque lettre a un score de popularité.
Le softmax c'est comme transformer ces scores en pourcentages : "la lettre 'e'
a 40% des voix, 'a' a 25%, etc." Les lettres avec un meilleur score raflent
une plus grosse part du gâteau.

**Dans le tuto** : On l'introduit dans la leçon 1 sans la nommer (on fait
juste "diviser par le total pour avoir des pourcentages"). Le vrai softmax
avec exponentielle apparaît dans la leçon 3, présenté comme "une façon plus
maligne de transformer des scores en probabilités".

---

### 5. Les embeddings

**Dans le code** : Chaque caractère est représenté par un vecteur de nombres
(par exemple 48 dimensions dans microgpt.py). Ces vecteurs sont appris
pendant l'entraînement. Deux lettres qui se comportent de façon similaire
finissent avec des vecteurs proches dans cet espace à 48 dimensions.

**Traduction simple** : Imagine que tu dois décrire chaque lettre de l'alphabet
avec 3 notes sur 10 : "fréquence à début de mot", "fréquence après une voyelle",
"fréquence en fin de mot". La lettre 'q' et la lettre 'x' auraient des notes
similaires (rares, positions spéciales). Ces notes, c'est l'embedding.
Sauf que le modèle choisit tout seul quelles "notes" utiliser -- et il en
utilise beaucoup plus que 3.

**Dans le tuto** : La leçon 3 commence avec des vecteurs de taille 8
(au lieu de 48). L'élève crée les embeddings, les voit changer pendant
l'entraînement, et comprend que le modèle "place" les lettres similaires
proches les unes des autres.

---

### 6. Le mécanisme d'attention

**Dans le code** : Le self-attention calcule pour chaque position un triplet
Query/Key/Value. La Query est comparée à toutes les Keys via un produit
scalaire, les scores passent par un softmax, puis les Values sont agrégées
en somme pondérée. Un masque causal empêche de regarder le futur.
Tout ça est répété sur 4 têtes en parallèle.

**Traduction simple** : Imagine une salle de classe. Chaque élève (= chaque
lettre) peut lever la main pour poser une question (Query). Les autres élèves
montrent une pancarte avec leur spécialité (Key). L'élève choisit à qui
demander en comparant sa question avec les pancartes. Puis il récupère
l'information (Value) de ceux qui correspondent le mieux. Le masque causal
c'est simple : tu ne peux poser de questions qu'aux élèves assis **devant toi**
-- pas à ceux derrière (le futur).

**Dans le tuto** : La leçon 4 décompose tout avec le mot "chat" comme exemple
concret. L'élève calcule les scores à la main, voit les poids d'attention,
et comprend pourquoi certaines lettres "comptent" plus que d'autres.

---

### 7. Ce que microgpt.py ne fait PAS

Même si l'algorithme est complet, ce script minimaliste omet volontairement :

| Fonctionnalité | Pourquoi c'est absent | Impact |
|---|---|---|
| **GPU / CUDA** | Python pur, pas de parallélisme | 1000x plus lent qu'avec PyTorch |
| **Tenseurs / Vectorisation** | Boucles for au lieu d'opérations matricielles batch | Chaque calcul se fait nombre par nombre |
| **Tokenizer BPE** | Utilise des caractères individuels | Ne peut pas apprendre des mots entiers |
| **Plusieurs couches** | 1 seule couche transformer | Capacité très limitée (patterns courts seulement) |
| **LayerNorm complet** | Utilise RMSNorm (plus simple) | Moins stable sur de gros modèles |
| **GeLU** | Utilise ReLU (plus simple) | Performances légèrement inférieures |
| **Dropout** | Pas de régularisation | Risque de sur-apprentissage sur de gros datasets |
| **RLHF / Fine-tuning** | Pas d'alignement humain | Ne peut pas "suivre des instructions" comme ChatGPT |
| **Fenêtre de contexte longue** | ~16-32 caractères | Ne peut pas "se souvenir" de phrases entières |
| **Inférence optimisée** | Pas de KV-cache, pas de quantization | Chaque token regénère tout le calcul |

**En résumé** : microgpt.py démontre le "quoi" (l'algorithme), pas le "comment
aller vite" (l'ingénierie). C'est exactement ce qui le rend idéal pour apprendre.

---

## Objectif du tuto

A la fin du cours, l'élève :

1. Comprend comment une IA "devine" le mot suivant
2. A construit son propre mini-modèle de langage en Python pur
3. Génère des prénoms ou des noms de dinosaures avec son modèle
4. Sait expliquer les mots "embedding", "attention", "loss" et "gradient"
5. Comprend ce qui différencie son mini-modèle de ChatGPT (l'échelle, pas l'algorithme)

## Prérequis

- Python 3.10+
- Savoir écrire des boucles et des fonctions en Python (niveau débutant)
- Aucune notion de maths avancées requise

## Installation

```bash
git clone <repo-url> && cd "tuto llm"
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate sur Windows
pip install -r requirements.txt
pip install -e .
```

Pour contribuer (hooks qualité) :

```bash
pre-commit install --hook-type pre-commit --hook-type commit-msg --hook-type pre-push
```

## Structure du cours

| # | Notebook | Concept clé | Analogie | Durée |
|---|---------|-------------|----------|-------|
| 1 | `01_deviner_la_suite.ipynb` | Probabilités, bigrammes | T9 / clavier prédictif | 30 min |
| 2 | `02_apprendre_des_erreurs.ipynb` | Loss, gradient, entraînement | Lancer au panier | 45 min |
| 3 | `03_la_memoire_du_modele.ipynb` | Embeddings, contexte, réseau | Notes sur 10 pour chaque lettre | 30 min |
| 4 | `04_lattention.ipynb` | Attention, Q/K/V, masque causal | Salle de classe | 45 min |
| 5 | `05_mon_premier_llm.ipynb` | Assemblage complet, génération | De 0 à GPT | 45 min |

## Lancer le cours

```bash
jupyter notebook
```

Puis ouvrir les notebooks dans `notebooks/` dans l'ordre.

## Structure du projet

```
notebooks/              # 5 leçons Jupyter (code inline pour pédagogie)
src/tuto_llm/           # Fonctions extraites pour tests unitaires
  core.py               # softmax, mat_vec, forward_llm, generer_llm...
  data.py               # charger_dataset, nettoyer_mot, valider_vocab, formater_training
  vocab.py              # VOCAB (27 tokens : '.' + a-z), char_to_id, id_to_char
data/                   # Datasets pour entraînement
  prenoms.txt           # ~30 800 prénoms français (INSEE, Etalab 2.0)
  dinosaures.txt        # ~1 524 noms de dinosaures
  haiku.csv             # 1 000 haiku (usage futur, vocab étendu requis)
tests/                  # 88 tests (42 core + 46 data), coverage 100%
scripts/build_datasets.py  # Pipeline reproductible de construction des datasets
docs/                   # Documentation ISO et gouvernance IA
  DATASETS.md           # Référence complète : 12 datasets documentés, audit qualité
  AI_POLICY.md          # Politique anti-hallucination (ISO 42001)
  ISO_STANDARDS_REFERENCE.md  # 6 normes ISO appliquées
```

Les **notebooks** contiennent le code inline pour la pédagogie.
Le dossier **src/** duplique les fonctions clés pour permettre les tests
unitaires. Les deux restent synchronisés.

## Datasets

| Dataset | Taille | Source | Usage |
|---------|--------|--------|-------|
| Prénoms INSEE | 30 806 | [INSEE](https://www.insee.fr/fr/statistiques/7633685) (Etalab 2.0) | Dataset principal, compatible vocab actuel |
| Dinosaures | 1 524 | [Dvelezs94](https://gist.github.com/Dvelezs94/24bfcc8ab6042613ab5d94275e2e395a) | Dataset alternatif compact |
| Haiku | 1 000 | [haikurnn](https://github.com/docmarionum1/haikurnn) | Usage futur (nécessite vocab étendu) |

Régénérer les datasets : `python scripts/build_datasets.py`

Voir [docs/DATASETS.md](docs/DATASETS.md) pour l'audit qualité complet
et les 9 autres datasets documentés pour extension future.

## Qualité

Le projet applique 6 normes ISO adaptées au contexte éducatif :

| Norme | Contrôle | Commande |
|-------|----------|----------|
| ISO 5055 | Qualité du code | `ruff check src/ && mypy src/` |
| ISO 25010 | Complexité <= 15 | Intégré dans ruff (C901) |
| ISO 29119 | Tests, coverage >= 70% | `PYTHONPATH=src pytest tests/ --cov=src --cov-fail-under=70` |
| ISO 27001 | Pas de secrets, pas de CVE | `gitleaks protect --staged && pip-audit` |
| ISO 12207 | Commits conventionnels | `cz check` (hook commit-msg) |
| ISO 42001 | Citations sources, anti-hallucination | Revue manuelle des notebooks |

Lancer tous les contrôles : `pre-commit run --all-files`

## Etat du projet (v1.2.0)

- 5 notebooks complets (probabilités, loss, embeddings, attention, LLM)
- 88 tests, 100% coverage sur `src/`
- 3 datasets intégrés, pipeline reproductible
- CI GitHub Actions (6 jobs parallèles)
- Pre-commit hooks (13 hooks, 3 stages)

**Prochaine étape** : le mini-LLM a actuellement des poids aléatoires.
L'ajout d'un notebook d'entraînement réel sur les prénoms permettra
de produire des poids appris et de générer des prénoms réalistes.

## Références

- [microgpt.py - Karpathy](https://gist.github.com/karpathy/8627fe009c40f57531cb18360106ce95) -- le script source
- [micrograd - Karpathy](https://github.com/karpathy/micrograd) -- autograd seul, encore plus minimal
- [nanoGPT - Karpathy](https://github.com/karpathy/nanoGPT) -- version PyTorch, entraînable pour de vrai
- [Vidéo "Let's build GPT"](https://www.youtube.com/watch?v=kCc8FmEb1nY) -- explication complète en 2h (anglais)
- ["Attention Is All You Need"](https://arxiv.org/abs/1706.03762) -- Vaswani et al., 2017
- [3Blue1Brown - Neural Networks](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi) -- visualisations pédagogiques
