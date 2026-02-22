# Datasets - Référence complète

Ce document liste tous les datasets intégrés au projet et les datasets
découverts pour une extension future du mini-LLM.

## Vocabulaire actuel

Le mini-LLM utilise un vocabulaire de 27 tokens : `.` (début/fin) + `a-z`.
Les datasets marqués "compatible" fonctionnent directement avec ce vocabulaire.
Les autres nécessitent un vocabulaire étendu.

---

## Datasets intégrés

### 1. Prénoms INSEE

| Champ | Valeur |
|-------|--------|
| Fichier | `data/prenoms.txt` |
| Source | [INSEE - Fichier des prénoms depuis 1900](https://www.insee.fr/fr/statistiques/7633685) |
| Licence | Licence ouverte Etalab 2.0 |
| Taille | ~30 800 prénoms uniques (min 2 caractères) |
| Format | Un prénom par ligne, trié alphabétiquement |
| Nettoyage | Lowercase, accents supprimés (NFKD), filtré a-z, min 2 chars |
| Compatible vocab | Oui |

**Usage** : Dataset principal pour entraîner le mini-LLM à générer
des prénoms français lettre par lettre (notebooks 3-6). Le notebook 06
entraîne le modèle sur 10 000 prénoms avec rétropropagation analytique.

### 2. Dinosaures

| Champ | Valeur |
|-------|--------|
| Fichier | `data/dinosaures.txt` |
| Source | [dinos.txt - Dvelezs94](https://gist.github.com/Dvelezs94/24bfcc8ab6042613ab5d94275e2e395a) |
| Licence | Public domain (gist public) |
| Taille | ~1 524 noms uniques |
| Format | Un nom par ligne, trié alphabétiquement |
| Nettoyage | Lowercase, filtré a-z uniquement |
| Compatible vocab | Oui |

**Usage** : Dataset alternatif compact. Inspiré du cours de Karpathy
([makemore](https://github.com/karpathy/makemore)), idéal pour montrer
que le même modèle apprend des distributions différentes.

### 3. Haiku (usage futur)

| Champ | Valeur |
|-------|--------|
| Fichier | `data/haiku.csv` |
| Source | [haikurnn - docmarionum1](https://github.com/docmarionum1/haikurnn) |
| Licence | **Incertaine** (voir note ci-dessous) |
| Taille | 1 000 haiku (échantillon) |
| Format | CSV : line1, line2, line3, source |
| Compatible vocab | Non (espaces, ponctuation, majuscules) |

**Note licence** : Le plan initial prévoyait le dataset
[bfbarry/haiku-dataset](https://www.kaggle.com/datasets/bfbarry/haiku-dataset)
(CC0) sur Kaggle, mais le téléchargement Kaggle nécessite une authentification.
La source de substitution (haikurnn) collecte des haiku depuis des sites
publics (tempslibres, haikuhut, etc.) sans fichier LICENSE dans le repo.
Le statut juridique est donc incertain. Ce dataset est stocké uniquement
comme référence pour un usage futur et ne doit pas être redistribué
sans vérification préalable des droits.

**Usage futur** : Nécessite un vocabulaire étendu (caractères spéciaux,
espaces, ponctuation). Pourrait servir pour un notebook avancé sur
la génération de texte libre.

### 4. Pokémon (noms anglais)

| Champ | Valeur |
|-------|--------|
| Fichier | `data/pokemon.txt` |
| Source | [PokéAPI](https://pokeapi.co/) |
| Licence | **Noms (c) Nintendo / Creatures Inc. / GAME FREAK inc.** (voir note) |
| Taille | 1 009 noms de base uniques |
| Format | Un nom par ligne, trié alphabétiquement |
| Nettoyage | Noms de base uniquement (avant le premier tiret), lowercase, filtré a-z, min 2 chars |
| Compatible vocab | Oui |

**Note copyright** : Les noms Pokémon sont des marques déposées de
Nintendo / Creatures Inc. / GAME FREAK inc. Le fichier est inclus
dans ce projet à des fins strictement éducatives et non commerciales.
Il ne doit pas être redistribué dans un contexte commercial.

**Usage** : Dataset alternatif engageant pour le public cible (10-14 ans).
Noms inventés avec des patterns reconnaissables (suffixes, sonorités).
Longueur moyenne 7.5 caractères, compatible avec CONTEXT=8.

---

## Datasets compatibles char-level (extensions possibles)

Ces datasets sont compatibles avec le vocabulaire actuel (a-z) après
nettoyage, et pourraient être intégrés facilement.

### Communes de France

| Champ | Valeur |
|-------|--------|
| Source | [INSEE - Code officiel géographique](https://www.insee.fr/fr/information/2560452) |
| Licence | Licence ouverte Etalab 2.0 |
| Taille estimée | ~35 000 noms |
| Concept ML | Distribution plus complexe que les prénoms |
| Notes | Noms composés fréquents (saint-, le-, la-) à nettoyer |

### Mythologie grecque

| Champ | Valeur |
|-------|--------|
| Source | Listes Wikipédia (divinités, héros, créatures) |
| Licence | CC BY-SA 3.0 |
| Taille estimée | ~500 noms |
| Concept ML | Petit dataset, risque de surapprentissage |
| Notes | Noms romanisés, déjà en caractères latins |

### Minéraux et pierres

| Champ | Valeur |
|-------|--------|
| Source | [Mindat.org](https://www.mindat.org/) ou Wikidata |
| Licence | Variable (Wikidata : CC0) |
| Taille estimée | ~5 000 noms |
| Concept ML | Vocabulaire technique, suffixes récurrents (-ite, -ase) |
| Notes | Bonne illustration des patterns morphologiques |

---

## Autres datasets pour concepts ML avancés

Ces datasets nécessitent un vocabulaire étendu mais illustrent
des concepts ML intéressants pour de futurs notebooks.

### Fables de La Fontaine

| Champ | Valeur |
|-------|--------|
| Source | [Projet Gutenberg](https://www.gutenberg.org/ebooks/56327) |
| Licence | Domaine public |
| Taille estimée | ~240 fables, ~10 000 lignes |
| Concept ML | Génération de texte long, structure poétique |
| Notes | Texte en français classique, riche en vocabulaire |

### SMS Spam Collection

| Champ | Valeur |
|-------|--------|
| Source | [UCI ML Repository](https://archive.ics.uci.edu/ml/datasets/sms+spam+collection) |
| Licence | CC BY 4.0 |
| Taille | 5 574 SMS (747 spam, 4 827 ham) |
| Concept ML | Classification binaire, NLP de base |
| Notes | En anglais, introduction à la classification |

### Tatoeba (phrases bilingues)

| Champ | Valeur |
|-------|--------|
| Source | [Tatoeba](https://tatoeba.org/fr/downloads) |
| Licence | CC BY 2.0 FR |
| Taille | ~400 000 paires français-anglais |
| Concept ML | Traduction, séquence à séquence |
| Notes | Trop avancé pour le cours actuel |

### Proverbes français

| Champ | Valeur |
|-------|--------|
| Source | Collections Wikiquote / domaine public |
| Licence | Domaine public / CC BY-SA |
| Taille estimée | ~2 000 proverbes |
| Concept ML | Patterns syntaxiques récurrents |
| Notes | Nécessite vocab étendu (espaces, ponctuation) |

### Fromages AOC/AOP

| Champ | Valeur |
|-------|--------|
| Source | [data.gouv.fr - Fromages AOP](https://www.data.gouv.fr/) |
| Licence | Licence ouverte Etalab |
| Taille estimée | ~50 noms |
| Concept ML | Très petit dataset, démonstration du surapprentissage |
| Notes | Compatible a-z après nettoyage des accents |

### Trivia / Questions-Réponses

| Champ | Valeur |
|-------|--------|
| Source | [Open Trivia Database](https://opentdb.com/) |
| Licence | CC BY-SA 4.0 |
| Taille | ~4 000 questions |
| Concept ML | Question answering, compréhension de texte |
| Notes | En anglais, nécessite vocab complet |

---

## Audit qualité des données

Audit réalisé le 2026-02-21 sur les 3 datasets intégrés.

### Prénoms (30 806 entrées)

**Distribution des longueurs** : min 2, max 15, moyenne 6.2 caractères.
Pic de distribution à 5-6 caractères. Les 26 lettres initiales a-z
sont toutes représentées.

**Fréquence des caractères** : `a` domine (16.5%), suivi de `e` (10.8%),
`i` (9.3%), `n` (9.2%). Les lettres rares : `q` (0.1%), `x` (0.1%).

| Finding | Sévérité | Détail | Action |
|---------|----------|--------|--------|
| F-P1 : 53 prénoms de 2 chars | Mineur | `mc`, `md`, `de`, `le`, `la`... particules et abréviations. 0.17% du dataset. | Aucune. Bruit négligeable pour le training. |
| F-P2 : variantes orthographiques massives | Info | `aaron`/`aarone`/`aaronn`, 17 variantes `moham*`/`muham*`. | Aucune. Distribution réelle INSEE. Le modèle apprend la fréquence réelle des déclarations. |

**Verdict** : dataset propre, prêt pour l'entraînement.

### Dinosaures (1 524 entrées)

**Distribution des longueurs** : min 3, max 26, moyenne 12.0 caractères.
Pic de distribution à 12-13 caractères.

**Pattern dominant** : 46.3% des noms finissent par `saurus`, 4.2% par
`odon`, 3.2% par `raptor`. Le modèle apprendra ce biais morphologique
(réaliste).

| Finding | Sévérité | Détail | Action |
|---------|----------|--------|--------|
| F-D1 : 6 noms <= 4 chars | Info | `mei`, `zuul`, `anzu`, `haya`, `proa`, `tawa`. Vrais dinosaures. | Aucune. |
| F-D2 : 46% finissent par "saurus" | Info | Distribution réelle de la nomenclature. | Aucune. Pattern pédagogiquement intéressant. |

**Verdict** : dataset propre, prêt pour l'entraînement.

### Haiku (1 000 entrées)

**Distribution des longueurs** : line1 moyenne 14.3 chars, line2 19.8,
line3 15.2. Haiku complet moyen : 49.3 chars, max 79.

**Caractères utilisés** : 77 uniques. 24 caractères hors vocab actuel
(espace, ponctuation, chiffres, majuscules).

| Finding | Sévérité | Détail | Action |
|---------|----------|--------|--------|
| F-H1 : source unique "tempslibres" | Majeur | 100% des haiku proviennent d'une seule source. Biais de style et de thème probable. | Diversifier avec d'autres sources (Kaggle CC0, haikuhut) si usage futur. |
| F-H2 : 11 haiku avec octets Windows-1252 | Majeur | `\x92` (apostrophe courbe), `\x96`/`\x97` (tirets longs). Pas de l'UTF-8 valide. | Nettoyer ou exclure les 11 lignes corrompues avant tout usage. |
| F-H3 : 1 000 haiku = données insuffisantes | Majeur | ~49k chars de training. Ratio data/params < 5. Sous-apprentissage probable. | Augmenter à 10 000+ haiku minimum (Kaggle CC0 en propose 11k). |

**Verdict** : dataset **non prêt** pour l'entraînement. Stocké comme
référence pour un usage futur après correction des 3 findings majeurs.

---

## Analyse de gap : mini-LLM actuel vs haiku

Le mini-LLM actuel est conçu pour la génération char-level de mots
courts (prénoms, dinosaures). Générer des haiku nécessite des
modifications **structurelles** du modèle.

### 1. Vocabulaire (`vocab.py`)

- **Actuel** : 27 tokens (`.` + `a-z`)
- **Nécessaire** : ~52 tokens (+ espace, `'`, `-`, `,`, `;`, `:`,
  `!`, `?`, `~`, chiffres `0-9`)
- **Problème critique** : le `.` est actuellement le délimiteur de
  début/fin de séquence. Or le `.` apparaît **dans** les haiku
  (655 occurrences de `-`, 30 de `,`, etc.). Il faut un token `<EOS>`
  séparé ou un identifiant numérique dédié (ex: `id=0` pour fin
  de séquence, indépendant du point typographique).

### 2. Fenêtre de contexte (`core.py`)

- **Actuel** : ~8 (prénoms de 6 chars en moyenne)
- **Nécessaire** : ~80 (haiku de 49 chars en moyenne, max 79)
- **Impact** : self-attention est O(n²). Passer de context=8 à
  context=80 multiplie le calcul par **100x**.

### 3. Dimension d'embedding

- **Actuel** : suffisant pour 27 tokens et des séquences courtes
- **Nécessaire** : au moins 32 pour capturer les relations entre
  52 tokens sur des séquences longues
- **Impact combiné** : O(context² x embed_dim) passe de 512 à 204 800
  (**400x** plus de calcul par token)

### 4. Entraînement

Depuis la v1.3.0, le mini-LLM dispose d'un entraînement complet :

- **Loss function** : cross-entropy caractère par caractère
- **Backpropagation** : analytique (7 étapes, implémentation manuelle)
- **Optimizer** : SGD en ligne (update après chaque position)
- **Configuration** : EMBED_DIM=16, HIDDEN_DIM=32, ~2 800 paramètres
- **Données** : 10 000 prénoms INSEE, 3 epochs (~350s en Python pur)

Pour les haiku, les modifications structurelles listées ci-dessous
restent nécessaires.

### 5. Génération multi-ligne

- `generer_llm` produit actuellement un seul mot
- Un haiku = 3 lignes avec des retours à la ligne
- Il faut apprendre au modèle le concept de saut de ligne
  (token `\n` dans le vocabulaire étendu)

### 6. Données insuffisantes

- 1 000 haiku x 49 chars = ~49 000 exemples de bigrammes
- Pour ~10 000 paramètres minimum, ratio data/params < 5
- Règle empirique : il faut au moins 10x plus de données que de
  paramètres pour un apprentissage correct
- **Minimum requis** : 10 000+ haiku

### Résumé du gap

| Composant | Prénoms (actuel) | Haiku (nécessaire) | Facteur |
|-----------|------------------|---------------------|---------|
| Vocabulaire | 27 tokens | ~52 tokens | 2x |
| Contexte | 8 | 80 | 10x |
| Calcul attention | O(512) | O(204 800) | 400x |
| Entraînement | SGD en ligne (v1.3.0) | Adam + batching | optimisation |
| Données | 30k mots | 10k+ haiku | nouveau |
| Type de séquence | 1 mot | 3 lignes | nouveau |

### Recommandation

1. ~~**Court terme** : entraîner le modèle actuel sur les prénoms~~ **Fait** (v1.3.0).
2. **Moyen terme** : notebook dinosaures (même modèle, autre distribution).
   Projet de niveau 2 avec PyTorch pour lever les limitations Python pur.
3. **Long terme** : notebook avancé sur la génération de haiku avec
   10k+ données, vocabulaire étendu, et contexte long.

---

## Audit des temps de computation

Audit réalisé le 2026-02-22 sur les 6 notebooks.

### Temps d'exécution par notebook

| # | Notebook | Modèle | Params | Dataset | Temps | Entraîne ? |
|---|---------|--------|--------|---------|-------|------------|
| 1 | Deviner la suite | Bigramme (comptage) | 729 compteurs | 20 prénoms codés en dur | <50ms | Non (comptage pur) |
| 2 | Apprendre des erreurs | Bigramme NN | 729 poids | 20 prénoms codés en dur | ~2s | Oui (50 epochs) |
| 3 | La mémoire du modèle | Feed-forward + embeddings | 891 poids | 20 prénoms codés en dur | ~10-15s | Oui (100 epochs) |
| 4 | L'attention | Calcul manuel | 0 (pas de modèle) | "chat" (4 chars) | <1s | Non (conceptuel) |
| 5 | Mon premier LLM | Transformer complet | 2 832 poids | 15 prénoms codés en dur | ~500ms | Non (assemblage) |
| 6 | Entraîner le modèle | Transformer complet | 2 832 poids | 10 000 prénoms (fichier) | **~350s** | Oui (3 epochs) |

### Décision : pourquoi ne pas augmenter les notebooks 1-5

**L'interactivité est prioritaire sur la qualité du modèle.**

Les notebooks 1-5 s'exécutent en <15s chacun. Cette rapidité est une
feature pédagogique, pas une limitation :

1. **Feedback immédiat** : l'élève voit la loss baisser epoch par epoch
   en temps réel. Un entraînement de 5 minutes casserait ce retour visuel.
2. **Itération rapide** : l'élève peut modifier le code et relancer
   sans attendre. Essentiel pour le public cible (10-14 ans).
3. **Petit dataset = traçabilité** : avec 20 prénoms, l'élève peut
   vérifier mentalement que le modèle apprend les bons patterns.
4. **Plateau visible** : 50-100 epochs suffisent pour montrer la
   convergence. Plus d'epochs n'enseignent rien de nouveau.

Le notebook 06 est le seul avec un temps long (~350s). Ce temps est
exploité pédagogiquement : l'élève lit les sections "En vrai..." sur
GPU, Adam, RLHF et la comparaison avec GPT-4 pendant l'attente.

### Facteurs limitants en Python pur

| Opération | Python pur | NumPy | PyTorch GPU | Facteur |
|-----------|-----------|-------|-------------|---------|
| mat_vec (16x16) | ~250 mult/s | ~10M/s | ~1G/s | 1x / 40 000x / 4M x |
| Forward (1 token) | ~1ms | ~0.02ms | ~0.001ms | 1x / 50x / 1000x |
| 10k prénoms × 3 epochs | ~350s | ~7s | ~0.3s | 1x / 50x / 1000x |

Augmenter EMBED_DIM de 16 à 32 doublerait le temps d'entraînement
(~700s), dépassant le budget de 600s. Augmenter le dataset à 30k
prénoms triplerait le temps (~1050s). Les deux sont impossibles
sans changer de stack technique.

### Conclusion

Le cours actuel est **dimensionné au maximum de Python pur** dans un
budget temps raisonnable. Pour aller plus loin (plus de données, plus
de paramètres, meilleure génération), il faut un projet de niveau 2
avec PyTorch.

---

## Projet de niveau 2 : au-delà de Python pur

Le cours actuel enseigne le "quoi" (l'algorithme). Un projet de
niveau 2 enseignerait le "comment aller vite" (l'ingénierie).

### Ce que le projet actuel ne peut pas faire

| Limitation | Cause | Impact |
|------------|-------|--------|
| ~2 800 paramètres max | Python pur trop lent | Patterns courts seulement |
| 10k prénoms max | Budget temps 600s | Ne peut pas utiliser les 30k |
| 1 couche transformer | Plus de couches = plus de calcul | Capacité limitée |
| 1 tête d'attention | EMBED_DIM=16 trop petit pour split | Perspective unique |
| Pas de LayerNorm | Ajouterait de la complexité | Instabilité sur gros modèles |
| Pas de Dropout | Ajouterait de la complexité | Surapprentissage possible |
| SGD basique | Adam trop complexe à implémenter | Convergence lente |
| Vocab 27 tokens | Pas de texte libre | Mots courts a-z uniquement |

### Ce que PyTorch apporterait

| Composant | Python pur (actuel) | PyTorch (niveau 2) |
|-----------|--------------------|--------------------|
| Autograd | 80 lignes de `backward_llm()` | `loss.backward()` (1 ligne) |
| Calcul | Boucles `for` | Tenseurs vectorisés (50x) |
| GPU | Impossible | CUDA (1000x supplémentaire) |
| Optimizer | SGD en ligne | Adam avec lr decay |
| Architecture | 1 couche, 1 tête, ~2 800 params | 4+ couches, 4 têtes, ~100k params |
| Contexte | 8 caractères | 128+ caractères |
| Vocabulaire | 27 tokens (a-z + .) | 52+ tokens (texte libre) |
| Datasets | Prénoms, dinosaures | + haiku, fables, proverbes |
| Entraînement | ~350s pour 10k mots | ~10s pour 30k mots |

### Prérequis pour le niveau 2

- Avoir terminé les 6 notebooks du cours actuel
- Connaître NumPy (tableaux, opérations vectorisées)
- Installer PyTorch (`pip install torch`)

### Contenu envisagé

1. **Traduction du mini-LLM en PyTorch** : même architecture, même
   résultat, mais en 50 lignes au lieu de 300. L'élève voit que
   PyTorch fait exactement ce qu'il a codé à la main.
2. **Scaling up** : 4 couches, 4 têtes, EMBED_DIM=64, entraînement
   sur 30k prénoms en 10 secondes. Comparaison qualitative avant/après.
3. **Vocabulaire étendu** : espaces, ponctuation, majuscules. Génération
   de haiku ou de proverbes.
4. **GPU** : même code, `model.to("cuda")`, 1000x plus rapide.
5. **nanoGPT** : passage au [nanoGPT de Karpathy](https://github.com/karpathy/nanoGPT),
   version production du même algorithme.

### Relation entre les deux projets

```
Tuto LLM (ce projet)          Projet niveau 2
─────────────────────          ─────────────────
Python pur, 0 dépendance  →   PyTorch + CUDA
Comprendre l'algorithme    →   Obtenir des résultats
~2 800 paramètres          →   ~100 000+ paramètres
10-14 ans, débutant        →   Lycée/fac, connaît NumPy
"Quoi"                     →   "Comment aller vite"
```

Le principe fondateur — *"This file is the complete algorithm.
Everything else is just efficiency."* — reste intact : le projet
actuel enseigne l'algorithme complet, le niveau 2 ajoute l'efficacité.

---

## Reproduction des datasets

Le script `scripts/build_datasets.py` télécharge les sources brutes
et produit les fichiers finaux. Il peut être relancé à tout moment
pour régénérer les datasets à l'identique :

```bash
python scripts/build_datasets.py
```

## Chargement des datasets

Utiliser les fonctions de `src/tuto_llm/data.py` :

```python
from tuto_llm.data import (
    charger_csv,
    charger_dataset,
    formater_training,
    nettoyer_mot,
    valider_vocab,
)

# Charger un dataset texte (un mot par ligne)
noms = charger_dataset("data/prenoms.txt")

# Charger un dataset CSV (haiku)
haiku = charger_csv("data/haiku.csv")  # -> list[dict]

# Nettoyer un mot avec accents
clean = nettoyer_mot("Éloïse")  # -> "eloise"

# Valider la compatibilité vocab (min 2 chars)
valides = valider_vocab(noms, min_len=2)

# Formater pour l'entraînement du mini-LLM
training = formater_training(valides)  # -> [".alice.", ".bob.", ...]
```
