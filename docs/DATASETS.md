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
des prénoms français lettre par lettre (notebooks 3-5).

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

### Pokémon (noms anglais)

| Champ | Valeur |
|-------|--------|
| Source | [PokéAPI](https://pokeapi.co/) |
| Licence | API publique |
| Taille estimée | ~1 000 noms |
| Concept ML | Noms inventés avec des patterns reconnaissables |
| Notes | Populaire auprès du public cible (10-14 ans) |

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

### 4. Entraînement (inexistant)

Le mini-LLM a actuellement des **poids aléatoires**. Même pour les
prénoms, il ne génère rien de cohérent. Il faut implémenter :

- **Loss function** : cross-entropy caractère par caractère
- **Backpropagation** : autograd (PyTorch) ou implémentation manuelle
- **Optimizer** : SGD au minimum, Adam pour une convergence plus rapide

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
| Entraînement | aucun | cross-entropy + SGD | nouveau |
| Données | 30k mots | 10k+ haiku | nouveau |
| Type de séquence | 1 mot | 3 lignes | nouveau |

### Recommandation

1. **Court terme** : entraîner le modèle actuel sur les prénoms
   (vocabulaire déjà compatible, 30k exemples, tâche simple).
2. **Moyen terme** : étendre le vocabulaire, augmenter le contexte,
   implémenter l'entraînement dans un notebook dédié.
3. **Long terme** : notebook avancé sur la génération de haiku avec
   10k+ données, vocabulaire étendu, et contexte long.

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
