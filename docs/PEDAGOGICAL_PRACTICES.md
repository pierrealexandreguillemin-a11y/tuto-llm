# Pratiques pedagogiques pour notebooks Jupyter (10-14 ans)

| Champ | Valeur |
|-------|--------|
| **Projet** | Tuto LLM -- Creer son mini-LLM (10-14 ans) |
| **Norme** | ISO/IEC 42001:2023 (Gouvernance IA) |
| **Version** | v1.5.0 |
| **Date** | 2026-02-23 |
| **Auteur** | Recherche documentaire assistee par Claude (Anthropic) |
| **Statut** | Actif -- mis a jour a chaque evolution pedagogique |

## Instructions LLM

Ce document est concu pour etre lu par des LLM assistant le projet.
Pour une recherche rapide, utiliser les sections numerotees ci-dessous.

**Recherche par besoin** :
- "Quelle convention pour X ?" -> Section 2 (Sources) + Section 3 (Conventions)
- "Comment structurer un notebook ?" -> Section 3.1 (Structure)
- "Quel projet ressemble a Tuto LLM ?" -> Section 5 (Benchmark)
- "Comment ameliorer les notebooks ?" -> Section 7 (Phase actuelle)
- "Quoi utiliser pour la phase 2 ?" -> Section 8 (Phase 2 PyTorch)
- "Pourquoi on ne fait pas X ?" -> Section 4 (Ce qu'on ne fait PAS)

**Contrainte cle** : tout ajout aux notebooks doit respecter la
contrainte "zero dependance" (Python stdlib + `IPython.display` uniquement).
Voir Section 4 pour les justifications des rejets.

---

## Sommaire

1. [Objectif du document](#1-objectif-du-document)
2. [Sources de reference](#2-sources-de-reference) (7 sources)
3. [Conventions appliquees a Tuto LLM](#3-conventions-appliquees-a-tuto-llm)
   - 3.1 Structure de chaque notebook
   - 3.2 Regles de redaction
   - 3.3 Progression des exercices (scaffolding)
   - 3.4 Marqueurs visuels
4. [Ce que Tuto LLM ne fait PAS](#4-ce-que-tuto-llm-ne-fait-pas-et-pourquoi)
5. [Benchmark des projets similaires](#5-benchmark-des-projets-similaires)
   - 5.1 Projets "LLM from scratch"
   - 5.2 Projets educatifs IA pour enfants/ados
   - 5.3 Cadre institutionnel francais
   - 5.4 Ressources pedagogiques complementaires
6. [Positionnement unique de Tuto LLM](#6-positionnement-unique-de-tuto-llm)
7. [Projets utiles pour la phase actuelle (v1.5.0)](#7-projets-utiles-pour-ameliorer-la-phase-actuelle-v150)
   - 7.1 Visualisation sans dependances
   - 7.2 Validation des exercices
   - 7.3 Gamification legere
   - 7.4 Distribution et accessibilite
   - 7.5 Projets educatifs francais complementaires
8. [Projets utiles pour la phase 2 (PyTorch)](#8-projets-utiles-pour-la-phase-2-transition-vers-pytorch)
   - 8.1 Traduire en PyTorch
   - 8.2 Monter en echelle
   - 8.3 Vocabulaire etendu
   - 8.4 Support GPU
   - 8.5 Transition vers nanoGPT
   - 8.6 Ressources transversales
9. [References](#9-references) (41 sources)

---

## 1. Objectif du document

Recherche documentaire realisee le 2026-02-23 pour le projet Tuto LLM.
Synthese des conventions et bonnes pratiques identifiees dans les projets
de reference ciblant le meme public (colleges, ateliers decouverte IA).
Benchmark des projets similaires et inventaire des outils d'amelioration.

---

## 2. Sources de reference

### 1. Capytale (Education nationale, France)

[Capytale](https://capytale2.ac-paris.fr/) est la plateforme officielle
de l'Education nationale pour les notebooks Python au college et lycee.
~80 000 utilisateurs/semaine.

**Conventions identifiees** :

- **Cellules de consigne en markdown** : l'enseignant redige les
  instructions dans des cellules markdown non editables, l'eleve
  ecrit dans des cellules code separees.
- **Protection des cellules** : les cellules de cours sont verrouillees
  (`"editable": false` dans les metadonnees). L'eleve ne peut modifier
  que les cellules d'exercice.
- **Progression sequentielle** : les cellules sont executees de haut
  en bas. Sauter une cellule casse l'execution.
- **Activites de type "completer le code"** : code a trous avec
  commentaires `# A COMPLETER` ou `# VOTRE CODE ICI`.

### 2. EPFL - Les 4 cles de la pedagogie (Suisse)

Recherche en sciences de l'education de l'EPFL, appliquee aux cours
de programmation pour debutants.

**Les 4 cles** :

| Cle | Description | Application notebooks |
|-----|-------------|----------------------|
| **Progression** | Du simple au complexe, une notion a la fois | 6 lecons progressives, chaque concept construit sur le precedent |
| **Resolution de problemes** | L'eleve fait, pas seulement lit | Exercices avec cellules vides a completer |
| **Feedback immediat** | L'eleve voit le resultat tout de suite | Shift+Entree affiche le resultat instantanement |
| **Objectifs visibles** | L'eleve sait ou il va | Chaque notebook annonce ce qu'on va apprendre |

### 3. jupyter4edu - Catalogue de 23 patterns (UC Berkeley)

Le projet [jupyter4edu](https://jupyter4edu.github.io/jupyter-edu-book/)
de UC Berkeley documente 23 patterns pedagogiques pour Jupyter.

**Patterns les plus pertinents pour Tuto LLM** :

| Pattern | Description | Application |
|---------|-------------|-------------|
| **Shift-Enter for the Win** | La premiere cellule doit etre executable immediatement, sans prerequis. L'eleve apprend le geste Shift+Entree des la premiere interaction. | Cellule d'accueil avec instructions + premier `print()` |
| **Fill in the Blanks** | Code a trous : la structure est donnee, l'eleve complete les parties manquantes. Reduit l'angoisse de la page blanche. | `# --- EXERCICE : Ecris ton code ici ---` |
| **Target Practice** | L'eleve voit le resultat attendu avant de coder. Il sait a quoi son code doit aboutir. | "Execute la cellule pour verifier tes reponses" |
| **Tweak Twiddle Frob** | L'eleve modifie une valeur dans du code fonctionnel et observe l'effet. Pas de creation ex nihilo. | `nombre = 10  # <-- Mets 50 ici !` |
| **Narrative Arc** | Le notebook raconte une histoire avec debut, milieu, fin. Pas une collection de cellules decousues. | Progression : compter -> probabilites -> generer |
| **Scaffolding** | Structure fournie, complexite progressive. Les premieres cellules sont entierement donnees, les dernieres demandent plus d'autonomie. | Exercice 1 = executer, Exercice 4 = modifier |

### 4. py-edu-fr - Conventions Python pedagogique (France)

Conventions emergentes de la communaute Python educative francaise
(NSI, ISN, SNT, ateliers decouverte).

**Conventions identifiees** :

- **Variables en francais** : `compteur`, `lettre`, `prenom` plutot
  que `counter`, `letter`, `name`. Le public ne parle pas anglais.
- **Commentaires explicatifs** : chaque bloc de code est commente
  en francais, expliquant le "pourquoi" pas seulement le "quoi".
- **`print()` genereux** : afficher les resultats intermediaires
  pour que l'eleve voie ce qui se passe a chaque etape.
- **Pas de one-liners** : privilegier la lisibilite sur la concision.
  `for i in range(10): print(i)` plutot que des comprehensions.
- **Analogies avant le code** : chaque concept est introduit par
  une analogie du quotidien avant toute ligne de code.

### 5. Callysto (Canada)

[Callysto](https://www.callysto.ca/) -- programme canadien de
notebooks educatifs pour les 10-18 ans, finance par Cybera et PIMS.

**Conventions identifiees** :

- **Titre clair en haut** : chaque notebook commence par un titre
  et un paragraphe d'objectif ("Dans ce notebook, tu vas...").
- **Emojis et visuels** : utilises avec parcimonie pour attirer
  l'attention sur les points importants.
- **Sections courtes** : maximum 3-4 cellules entre deux exercices.
  L'attention des 10-14 ans est limitee (~10 minutes par bloc).
- **Cellules de validation** : apres un exercice, une cellule
  "verifie ta reponse" donne un feedback immediat.

### 6. ML for Kids (Royaume-Uni)

[ML for Kids](https://machinelearningforkids.co.uk/) -- plateforme
d'initiation au machine learning pour les 8-14 ans, par Dale Lane (IBM).

**Conventions identifiees** :

- **Vocabulaire adapte** : eviter le jargon technique. "Le modele
  devine" plutot que "inference probabiliste".
- **Resultats tangibles** : chaque lecon produit quelque chose de
  visible et amusant (un nom genere, un dessin, un jeu).
- **Pas de prerequis mathematiques** : les maths sont cachees
  derriere des analogies. L'eleve ne voit jamais une formule.

### 7. Kaggle Learn (international)

[Kaggle Learn](https://www.kaggle.com/learn) -- micro-cours
interactifs sur la data science et le ML.

**Conventions identifiees** :

- **Exercices a difficulte croissante** : chaque lecon a 3-5
  exercices, du plus simple au plus ouvert.
- **Code de demarrage fourni** : l'eleve ne part jamais d'une
  cellule vide. Il y a toujours du code a modifier ou completer.
- **Indices progressifs** : un bouton "indice" revele une aide
  avant la solution complete.

---

## 3. Conventions appliquees a Tuto LLM

Synthese des conventions retenues pour les 6 notebooks du projet,
basee sur l'analyse des sources ci-dessus.

### 3.1 Structure de chaque notebook

```
[Cellule 0]  Titre + accueil + mode d'emploi Jupyter
             "Comment ca marche ? 1. Clique... 2. Shift+Entree..."

[Cellule 1]  Introduction du concept (markdown)
             Analogie du quotidien, vocabulaire simple

[Cellule 2]  Code de demonstration
             L'eleve execute, observe le resultat

[Cellule 3]  Exercice explicite (markdown)
             "A toi de jouer ! (Exercice N)"

[Cellule 4]  Cellule code vide/editable
             "# --- EXERCICE N : Ecris ton code ici ---"

  ... (repetition du cycle demonstration/exercice) ...

[Avant-derniere]  Resume "Ce qu'on a appris"
                  3-4 bullet points, lien vers lecon suivante

[Derniere]  Sources (ISO 42001)
            Citations, copyright, references
```

### 3.2 Regles de redaction

| Regle | Justification | Source |
|-------|---------------|--------|
| **Cellule d'accueil** avec mode d'emploi Jupyter | L'eleve n'a peut-etre jamais vu un notebook | jupyter4edu "Shift-Enter for the Win" |
| **Separateurs `---`** entre sections | Repere visuel dans le flot de cellules | Callysto, Capytale |
| **"A toi de jouer !"** en titre d'exercice | Marqueur explicite, pas de confusion cours/exercice | Capytale, EPFL "Resolution de problemes" |
| **Cellules code vides** pour les exercices | L'eleve sait ou ecrire | jupyter4edu "Fill in the Blanks" |
| **Commentaire `# <-- Change cette valeur !`** | Guide l'oeil vers le point d'action | jupyter4edu "Tweak Twiddle Frob" |
| **`print()` apres chaque etape** | Feedback visuel immediat | EPFL "Feedback immediat", py-edu-fr |
| **Variables en francais** | Public francophone de 10-14 ans | py-edu-fr |
| **Analogie avant le code** | Ancrage dans le concret | ML for Kids, EPFL "Progression" |
| **Maximum 4 cellules entre exercices** | Attention limitee (~10 min par bloc) | Callysto |
| **Difficulte croissante des exercices** | Du "execute" au "modifie" au "cree" | Kaggle Learn, jupyter4edu "Scaffolding" |
| **Resume en fin de notebook** | L'eleve sait ce qu'il a appris | EPFL "Objectifs visibles" |
| **Sources citees** | Transparence, anti-hallucination | ISO 42001, AI_POLICY.md |

### 3.3 Progression des exercices (scaffolding)

La difficulte des exercices progresse au sein de chaque notebook :

| Niveau | Type | Exemple | Pattern jupyter4edu |
|--------|------|---------|---------------------|
| 1 | **Executer** | "Execute la cellule pour voir le resultat" | Shift-Enter for the Win |
| 2 | **Observer** | "Que remarques-tu dans le resultat ?" | Target Practice |
| 3 | **Modifier** | "Change le nombre 10 en 50" | Tweak Twiddle Frob |
| 4 | **Completer** | "Ecris le code pour afficher le dernier element" | Fill in the Blanks |
| 5 | **Creer** | "Invente ta propre fonction" | (notebooks avances uniquement) |

Les notebooks 01-03 vont du niveau 1 au niveau 4.
Les notebooks 04-06 atteignent le niveau 5 pour certains exercices.

### 3.4 Marqueurs visuels dans les cellules

**Markdown (cours)** :
```markdown
---
## Titre de section

Explication avec **mots cles en gras** et analogie.
```

**Markdown (exercice)** :
```markdown
---
### A toi de jouer ! (Exercice N)

Consigne claire en 1-3 lignes. Indice entre backticks : `code`.
```

**Code (demonstration)** :
```python
# Execute cette cellule pour ... (Shift + Entree)
resultat = calcul()
print(f"Le resultat est : {resultat}")
```

**Code (exercice editable)** :
```python
# --- EXERCICE N : Ecris ton code ici, puis Shift + Entree ---

# Consigne 1 :


# Consigne 2 :

```

**Code (valeur a modifier)** :
```python
# --- EXERCICE N : Change la valeur, puis Shift + Entree ---
ma_variable = 10  # <-- Change cette valeur !

print(f"Resultat avec {ma_variable} : ...")
```

---

## 4. Ce que Tuto LLM ne fait PAS (et pourquoi)

| Pratique | Raison du rejet |
|----------|-----------------|
| **Protection de cellules** (`"editable": false`) | Non supporte par JupyterLite. Capytale le fait mais on n'utilise pas Capytale. |
| **Auto-grading** (nbgrader) | Trop complexe pour un atelier decouverte. Pas de serveur pour la correction. |
| **Widgets interactifs** (ipywidgets) | Dependance externe, incompatible avec la contrainte zero-install stdlib. |
| **Emojis dans le code** | Distraction. Reserves aux titres markdown si necessaire. |
| **Indices masquables** (bouton "hint") | Pas de support HTML interactif fiable dans JupyterLite. Indices donnes directement dans la consigne. |
| **Tests automatiques dans les cellules** | Ajoute du bruit visuel. Le `print()` suffit comme feedback pour ce public. |

---

## 5. Benchmark des projets similaires

Recherche realisee le 2026-02-23. Aucun projet existant ne combine
toutes les caracteristiques de Tuto LLM. Voici le paysage identifie.

### 5.1 Projets "LLM from scratch" (meme niche technique)

| Projet | Auteur | Approche | Public | Difference avec Tuto LLM |
|--------|--------|----------|--------|--------------------------|
| [microgpt.py](http://karpathy.github.io/2026/02/12/microgpt/) | A. Karpathy | 243 lignes Python pur, 0 dep., GPT complet (autograd, Adam, attention) | Developpeurs avances | **Source d'inspiration directe**. Code brut sans progression pedagogique. |
| [makemore](https://github.com/karpathy/makemore) | A. Karpathy | Char-level LM, progression bigram -> MLP -> Transformer, PyTorch | Developpeurs debutants ML | Serie video pedagogique mais necessite PyTorch, cible des adultes. |
| [TinyGPT](https://github.com/isaacperez/tinygpt) | Isaac Perez | GPT complet Python pur, 0 dep., autograd inclus | Developpeurs curieux | Proche techniquement mais pas de notebooks, pas de progression, Python 3.12+. |
| [LLMs from Scratch](https://github.com/rasbt/LLMs-from-scratch) | S. Raschka (Manning) | Livre + notebooks, GPT-2 complet pas-a-pas, PyTorch | Etudiants/ingenieurs | Tres pedagogique mais niveau universite, PyTorch obligatoire, en anglais. |
| [GPT in 60 lines of NumPy](https://jaykmody.com/blog/gpt-from-scratch/) | Jay Mody | Blog + code, GPT minimal avec NumPy | Developpeurs | NumPy requis, pas de notebooks interactifs, public adulte. |
| [minGPT](https://github.com/karpathy/minGPT) | A. Karpathy | ~300 lignes PyTorch, implementation propre et lisible | Developpeurs ML | PyTorch obligatoire, pas de progression pedagogique. |

### 5.2 Projets educatifs IA pour enfants/ados (meme public cible)

| Projet | Pays | Approche | Age | Difference avec Tuto LLM |
|--------|------|----------|-----|--------------------------|
| [ML for Kids](https://machinelearningforkids.co.uk/) | UK (IBM) | Interface web, Scratch/Python, classification | 8-14 ans | Pas de LLM, classification seulement. Interface graphique, pas de code "from scratch". |
| [Callysto](https://www.callysto.ca/) | Canada | Notebooks Jupyter, maths et data science | 10-18 ans | Pas d'IA generative, focus data/stats. Bonne reference pedagogique. |
| [Magic Makers](https://www.magicmakers.fr/products/decouvre-lintelligence-artificielle-collegiens) | France | Ateliers en groupe (10 max), Python + IA | Collegiens | Ateliers payants en presentiel, pas open-source, pas de LLM from scratch. |
| [Digi Activity](https://www.digi-activity.com/stage-atelier/stage-initiation-intelligence-artificielle) | France | Stages Python + IA, initiation coding | Ados | Stages payants, pas de contenu LLM specifique. |
| [Code.org AI](https://code.org/) | USA | Curriculum auto-guide IA, gratuit, en ligne | K-12 | Pas de code Python, approche visuelle/blocks. Pas de LLM. |
| [AI4K12](https://ai4k12.org/) | USA (AAAI) | Framework "5 Big Ideas in AI", guidelines K-12 | K-12 | Cadre theorique, pas de code ni notebooks. Reference pour le design pedagogique. |

### 5.3 Cadre institutionnel francais (contexte rentree 2025)

| Initiative | Details |
|-----------|---------|
| [Pix - Module IA obligatoire](https://www.1jeune1solution.gouv.fr/articles/formation-intelligence-artificielle-ecoles-france-2025) | Rentree 2025 : micro-formation IA obligatoire pour les 4e et 2nde via Pix. |
| [Cadre ministeriel IA en education](https://www.education.gouv.fr/publication-du-cadre-d-usage-de-l-intelligence-artificielle-en-education-450652) | Publication du cadre d'usage officiel de l'IA en education par le Ministere. |
| [Reseau Canope - IA en classe](https://www.reseau-canope.fr/ia-en-classe) | Ressources et formations pour les enseignants sur l'IA en classe. |
| [Capytale](https://capytale2.ac-paris.fr/) | Plateforme officielle de notebooks Python pour l'Education nationale (~80k utilisateurs/semaine). |

### 5.4 Ressources pedagogiques complementaires

| Ressource | Type | Pertinence |
|-----------|------|------------|
| [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) | Blog (Jay Alammar) | Visualisations du Transformer, public adulte. Reference pour les schemas. |
| [3Blue1Brown - Neural Networks](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi) | Videos YouTube | Animations pedagogiques de reference, deja cite dans Tuto LLM. |
| [Exploring LLMs through interactive Python activities](https://arxiv.org/html/2501.05577v1) | Article academique | Activites interactives Python pour decouvrir les LLM (Word2Vec, GPT-2). Public universitaire. |
| [Hugging Face LLM Course](https://huggingface.co/learn/llm-course/chapter1/1) | Cours en ligne | Cours complet sur les LLM avec l'ecosysteme HF. Niveau avance. |

---

## 6. Positionnement unique de Tuto LLM

Aucun projet identifie ne combine **tous** ces criteres :

| Critere | Tuto LLM | microgpt | makemore | LLMs from Scratch | ML for Kids | Callysto |
|---------|----------|----------|----------|-------------------|-------------|----------|
| Python pur (0 dep.) | **Oui** | Oui | Non (PyTorch) | Non (PyTorch) | Non | Non |
| Public 10-14 ans | **Oui** | Non | Non | Non | Oui | Oui |
| LLM complet (attention) | **Oui** | Oui | Oui | Oui | Non | Non |
| Notebooks progressifs | **Oui** | Non | Non | Oui | Non | Oui |
| En francais | **Oui** | Non | Non | Non | Non | Non |
| Analogies adaptees | **Oui** | Non | Partiellement | Oui | Oui | Oui |
| Exercices interactifs | **Oui** | Non | Non | Oui | Oui | Oui |
| Open-source gratuit | **Oui** | Oui | Oui | Non (livre) | Oui | Oui |

**Creneau occupe** : Tuto LLM est le seul projet qui enseigne la
construction complete d'un LLM (embeddings, attention, entrainement)
a un public jeune (10-14 ans), en francais, en Python pur, avec une
progression pedagogique documentee.

Les projets "from scratch" (microgpt, TinyGPT, LLMs from Scratch)
visent des adultes techniques. Les projets educatifs pour enfants
(ML for Kids, Callysto, Code.org) s'arretent a la classification
ou a la data science sans aborder les LLM.

Le contexte institutionnel francais (module Pix obligatoire en 4e,
cadre ministeriel IA) cree une opportunite pour des ressources
comme Tuto LLM qui vont au-dela de la sensibilisation et permettent
aux eleves de comprendre le fonctionnement interne de l'IA generative.

---

## 7. Projets utiles pour ameliorer la phase actuelle (v1.5.0)

Recherche realisee le 2026-02-23. Projets et outils pouvant enrichir
les 6 notebooks existants sans rompre la contrainte "zero dependances".

### 7.1 Visualisation sans dependances

Le module `IPython.display` (natif dans JupyterLite) permet d'afficher
du HTML, SVG et CSS directement dans les cellules de sortie. C'est la
solution la plus adaptee pour Tuto LLM.

| Outil | Description | Usage possible | Compatibilite |
|-------|-------------|----------------|---------------|
| [IPython.display + HTML/SVG](https://ipython.readthedocs.io/en/stable/api/generated/IPython.display.html) | Affichage HTML/SVG genere en Python pur | Heatmaps d'attention, courbes de loss, schemas de reseau | Natif JupyterLite, 0 dep. |
| [asciichartpy](https://github.com/kroitor/asciichart) | Graphiques ASCII, ~150 lignes, 0 dep. | Courbes de loss en texte ASCII (aspect "retro" amusant) | Pur Python, copiable dans le notebook |
| [BertViz](https://github.com/jessevig/bertviz) (technique) | Lignes colorees reliant tokens, opacite = poids d'attention | Reimplementable en SVG pur Python pour 27 tokens | Technique transposable, pas la lib elle-meme |
| [TrAVis](https://github.com/ayaka14732/TrAVis) | Visualiseur d'attention dans le navigateur via Pyodide + d3.js | Preuve que ca marche dans Pyodide/JupyterLite | Architecture directement applicable |

**Recommandation** : generer des tableaux HTML avec cellules colorees
(opacite CSS proportionnelle aux poids) via `display(HTML(...))`. Pour
27 tokens et des matrices 8x8, le HTML est plus lisible que matplotlib.

**Etat d'implementation (v1.5.0)** : 16 visualisations HTML implementees
via 7 fonctions `afficher_*` uniques (12 definitions dans les notebooks) :

| Fonction | Notebooks | Appels | Description |
|----------|-----------|--------|-------------|
| `afficher_heatmap` | NB01 | 1 | Heatmap d'attention (tableau HTML colore) |
| `afficher_barres` | NB01, NB03, NB05, NB06 | 6 | Barres horizontales de probabilites |
| `afficher_evolution_loss` | NB02, NB06 | 2 | Evolution de la loss (barres par epoch) |
| `afficher_embeddings` | NB03 | 1 | Vecteurs d'embedding (tableau colore) |
| `afficher_attention` | NB04, NB05 | 4 | Poids d'attention (barres horizontales) |
| `afficher_masque_causal` | NB04 | 2 | Masque causal (grille coloree) |
| `afficher_architecture` | NB05 | 1 | Schema de reseau avec connexions residuelles |

Toutes les visualisations sont marquees `<!-- tuto-viz -->` pour la
detection automatisee par les tests ISO 29119.

**Reste a explorer** : BertViz-style SVG (lignes reliant tokens avec
opacite proportionnelle aux poids d'attention), asciichartpy pour les
courbes de loss en mode retro.

### 7.2 Validation des exercices

| Outil | Description | Usage possible | Compatibilite |
|-------|-------------|----------------|---------------|
| **Pattern hash `hashlib`** | Hasher la reponse correcte (SHA-256), l'eleve soumet, on compare les hashs | Valider des reponses numeriques/textuelles sans reveler la solution | 100% stdlib Python |
| [nbautoeval](https://github.com/parmentelat/nbautoeval) | Framework leger d'exercices auto-evalues (cree pour le MOOC Python FUN) | Feedback vert/rouge instantane sur les 18 exercices | A tester via micropip dans JupyterLite |
| [JupyterQuiz](https://github.com/jmshea/jupyterquiz) | QCM interactifs en HTML/JS, questions en JSON | Questions de comprehension entre les exercices de code | A tester dans JupyterLite |
| **Fonctions `assert` + HTML** | `assert` avec messages personnalises + feedback HTML via IPython.display | Le plus simple : feedback visuel vert/rouge sans dependance | 100% compatible |

**Recommandation** : combiner `assert` + feedback HTML pour les exercices
de code, et le pattern hash pour les exercices de reflexion. Zero dependance.

### 7.3 Gamification legere

| Outil | Description | Usage possible | Compatibilite |
|-------|-------------|----------------|---------------|
| **Confetti JS inline** | Animation confetti via `display(HTML('<script>...</script>'))` | Celebrer la reussite d'un exercice | JS inline dans JupyterLite (a tester) |
| **Badges HTML/CSS maison** | Badges colores avec compteur de progression | "3/18 exercices termines", badge dore | 100% compatible, pur HTML |
| [Gamifying JupyterLab](https://link.springer.com/chapter/10.1007/978-3-031-22124-8_32) | Article de recherche (RWTH Aachen) | Points, badges, composants de progression | Inspiration conceptuelle |

**Recommandation** : un simple compteur de progression en HTML et des
messages encourageants suffisent pour les 10-14 ans. Eviter la
surcharge de gamification qui diluerait le contenu pedagogique.

### 7.4 Distribution et accessibilite

| Outil | Description | Usage possible | Compatibilite |
|-------|-------------|----------------|---------------|
| [Basthon](https://basthon.fr/) | Fork francais de JupyterLite pour l'Education nationale | Hebergement alternatif, execution 100% navigateur | Compatible (meme base Pyodide) |
| [Capytale](https://capytale2.ac-paris.fr/) | Plateforme officielle EN, basee sur Basthon, ~80k utilisateurs/semaine | Distribution directe aux enseignants et eleves francais | Compatible (Basthon/Pyodide) |
| **Theme CSS adapte** | Variables CSS JupyterLab pour polices plus grandes (16px+), contraste eleve | Reduire la charge cognitive chez les 10-14 ans | Pur CSS, sans dependance |

### 7.5 Projets educatifs francais complementaires

| Projet | Description | Interet |
|--------|-------------|---------|
| [La Scientotheque - Ressources IA](https://lascientotheque.github.io/ressources-ia/) | 6 activites IA pour les 10+ ans (association belge francophone) | Inspiration pour fiches pedagogiques et decoupage en activites |
| [Class'Code IAI](https://www.fun-mooc.fr/en/courses/lintelligence-artificielle-avec-intelligence/) | MOOC citoyen Inria, 7 a 107 ans, pedagogie active | Format en 4 phases : questionner, experimenter, decouvrir, debattre |
| [ENS Lyon - Entrainez votre premiere IA](https://culturesciencesphysique.ens-lyon.fr/ressource/IA-Bernet-2.xml) | Tutoriel interactif francais, zero install, IA educative | Meme esprit que Tuto LLM mais avec scikit-learn |
| [Pixees / NSI-SNT](https://pixees.fr/) | Ressources pedagogiques informatique au lycee | Ecosysteme naturel pour referencer Tuto LLM |
| [Jupyter4kids](https://github.com/collin1021/jupyter4kids) | Notebooks qui enseignent Python aux enfants | Reference pour le ton et le ratio texte/code |

---

## 8. Projets utiles pour la phase 2 (transition vers PyTorch)

Recherche realisee le 2026-02-23. La phase 2, documentee dans
`docs/DATASETS.md`, vise la transition de Python pur vers PyTorch
avec montee en echelle, vocabulaire etendu et support GPU.

### 8.1 Traduire le mini-LLM en PyTorch (~50 lignes)

| Projet | Description | Pertinence |
|--------|-------------|------------|
| [educational-transformer](https://github.com/ZSvedic/educational-transformer) | Transformer educatif PyTorch, commente, s'entraine en ~2s sur MacBook M1 | **Destination ideale.** Temps d'entrainement de ~2s = exactement l'objectif. |
| [picoGPT](https://github.com/jaymody/picoGPT) | GPT-2 en ~60 lignes NumPy, inference avec vrais poids | Pont intermediaire Python pur -> PyTorch. Valide l'objectif ~50 lignes. |
| [microGPT_webEdu](https://github.com/tanpuekai/microGPT_webEdu) | Interface web interactive pour microGPT de Karpathy | Inspiration pour comparaison visuelle Python pur vs PyTorch. |

**Trajectoire recommandee** : microGPT (Python pur, point de depart)
-> picoGPT (NumPy, pont intermediaire) -> educational-transformer
(PyTorch, destination).

### 8.2 Monter en echelle (4 couches, 4 tetes, 30k noms)

| Projet | Description | Pertinence |
|--------|-------------|------------|
| [makemore](https://github.com/karpathy/makemore) | Char-level LM, 32k noms, progression bigram -> Transformer | **Le plus directement aligne.** Dataset 32k noms, meme format. |
| [Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html) | 7 videos, de backprop a GPT, serie makemore (parties 1-5) | Reference pedagogique pour enseigner la progression. |
| [Char_Transformer_Language_Model](https://github.com/Lior-Baruch/Char_Transformer_Language_Model) | Transformer caractere PyTorch, configurable, entraine sur Shakespeare | Architecture 4 couches / 4 tetes parametrable. |
| [microformer](https://github.com/moorebrett0/microformer) | Transformer minimal PyTorch, inspire nanoGPT, modules separes | Template de structure de projet (config, data, model, train). |

### 8.3 Vocabulaire etendu (haiku, proverbes)

| Projet | Description | Pertinence |
|--------|-------------|------------|
| [haikoo](https://github.com/zkg/haikoo) | GPT-2 fine-tune sur haiku, mecanismes de controle syllabique | **Directement pertinent.** Dataset de haiku + gestion contraintes poetiques. |
| [haikurnn](https://github.com/docmarionum1/haikurnn) | RNN pour haiku avec comptage syllabique en entree | Approche de contrainte structurelle transposable au Transformer. |
| [poem_generation](https://github.com/michaelarman/poem_generation) | Comparaison LSTM / VAE / Transformer pour generation poetique | Datasets de poesie + comparaison d'architectures. |
| [Tutoriel PyTorch NLP From Scratch](https://docs.pytorch.org/tutorials/intermediate/char_rnn_generation_tutorial.html) | Generation de noms char-level, gestion des accents et caracteres speciaux | Reference officielle pour vocabulaire etendu en PyTorch. |

### 8.4 Support GPU

| Projet | Description | Pertinence |
|--------|-------------|------------|
| [nanoGPT](https://github.com/karpathy/nanoGPT) (detection auto CPU/GPU) | `device = "cuda" if torch.cuda.is_available() else "cpu"` | Pattern standard a enseigner. |
| [PyTorch en une heure](https://sebastianraschka.com/teaching/pytorch-1h/) | Cours condense tenseurs -> modele -> GPU (Sebastian Raschka) | Format condense ideal pour la transition. |
| [PyTorch Lightning](https://github.com/Lightning-AI/pytorch-lightning) | Abstraction `Trainer(accelerator="gpu")` | Etape "apres Phase 2" pour les avances. |

### 8.5 Transition vers nanoGPT

| Projet | Description | Pertinence |
|--------|-------------|------------|
| [build-nanogpt](https://github.com/karpathy/build-nanogpt) | Reproduction pas-a-pas de nanoGPT, commits Git sequentiels + video | **Outil pedagogique ideal.** "Notre mini-LLM + 1 feature par commit = nanoGPT." |
| [nanoGPT](https://github.com/karpathy/nanoGPT) | ~600 lignes PyTorch, reproduit GPT-2 (124M params) | Destination finale de la Phase 2. |
| [ng-video-lecture](https://github.com/karpathy/ng-video-lecture) | Fichier unique hackable accompagnant la video-lecture nanoGPT | Format "un fichier" ideal pour la salle de classe. |
| [nanochat](https://github.com/karpathy/nanochat) | Successeur de nanoGPT (~8k lignes), entraine un LLM pour ~100$ | Etape "apres nanoGPT" pour les plus avances. |
| [litGPT](https://github.com/Lightning-AI/litgpt) | 20+ LLM from scratch, sans abstractions, controle total | Reference production, au-dela du cadre educatif. |

### 8.6 Ressources transversales Phase 2

| Projet | Description | Pertinence |
|--------|-------------|------------|
| [Tutoriel officiel PyTorch nn.Transformer](https://docs.pytorch.org/tutorials/beginner/transformer_tutorial.html) | Language modeling avec nn.TransformerEncoder | Reference officielle pour les composants PyTorch. |
| [mini_llm](https://github.com/Arezkiiiii/mini_llm) | LLM from scratch en PyTorch via notebooks Jupyter interactifs | Format notebook ideal pour l'enseignement. |
| [Notes Zero-to-Hero](https://github.com/chizkidd/Karpathy-Neural-Networks-Zero-to-Hero) | Notes detaillees + notebooks pour chaque video Karpathy | Materiel de reference pret a l'emploi. |
| [Mini-cours 10 jours](https://machinelearningmastery.com/building-transformer-models-from-scratch-with-pytorch-10-day-mini-course/) | Transformer de zero en PyTorch, 1 composant par lecon | Structure pedagogique de reference pour organiser la Phase 2. |

### 8.7 Synthese Phase 2 : trajectoire pedagogique recommandee

```
Phase 1 (actuel)              Phase 2 (PyTorch)
────────────────              ──────────────────
microGPT Python pur      ->   educational-transformer (PyTorch ~50 lignes)
20 Pokemon, 1k inline    ->   makemore (32k noms, meme format)
vocab 27 tokens           ->   haikoo/haikurnn (vocab etendu, haiku)
CPU Python boucles for   ->   nanoGPT (GPU, detection auto CPU/CUDA)
"Quoi" (algorithme)       ->   build-nanogpt (commit par commit vers nanoGPT)
```

---

## 9. References

### 9.1 Sources pedagogiques (conventions des notebooks)

1. **Capytale** -- Plateforme de l'Education nationale :
   https://capytale2.ac-paris.fr/

2. **EPFL - 4 cles de la pedagogie** :
   https://www.epfl.ch/education/educational-initiatives/

3. **jupyter4edu - Teaching and Learning with Jupyter** :
   https://jupyter4edu.github.io/jupyter-edu-book/

4. **Callysto - Computational Thinking for K-12** :
   https://www.callysto.ca/

5. **ML for Kids** -- Dale Lane, IBM :
   https://machinelearningforkids.co.uk/

6. **Kaggle Learn** -- Micro-cours interactifs :
   https://www.kaggle.com/learn

7. **py-edu-fr** -- Communaute Python educative francaise :
   conventions observees dans les manuels NSI/SNT (Bordas, Hatier, Hachette)

### 9.2 Sources techniques (projets similaires)

8. **microgpt.py** -- Andrej Karpathy, 243 lignes Python pur :
   http://karpathy.github.io/2026/02/12/microgpt/

9. **makemore** -- Andrej Karpathy, char-level LM :
   https://github.com/karpathy/makemore

10. **minGPT** -- Andrej Karpathy, ~300 lignes PyTorch :
    https://github.com/karpathy/minGPT

11. **TinyGPT** -- Isaac Perez, GPT Python pur :
    https://github.com/isaacperez/tinygpt

12. **LLMs from Scratch** -- Sebastian Raschka (Manning) :
    https://github.com/rasbt/LLMs-from-scratch

13. **GPT in 60 lines of NumPy** -- Jay Mody :
    https://jaykmody.com/blog/gpt-from-scratch/

### 9.3 Sources institutionnelles (contexte francais)

14. **Module IA obligatoire rentree 2025** :
    https://www.1jeune1solution.gouv.fr/articles/formation-intelligence-artificielle-ecoles-france-2025

15. **Cadre ministeriel IA en education** :
    https://www.education.gouv.fr/publication-du-cadre-d-usage-de-l-intelligence-artificielle-en-education-450652

16. **Reseau Canope - IA en classe** :
    https://www.reseau-canope.fr/ia-en-classe

17. **AI4K12** -- AAAI, "5 Big Ideas in AI" :
    https://ai4k12.org/

### 9.4 Sources complementaires

18. **The Illustrated Transformer** -- Jay Alammar :
    https://jalammar.github.io/illustrated-transformer/

19. **Exploring LLMs through interactive Python activities** :
    https://arxiv.org/html/2501.05577v1

20. **Hugging Face LLM Course** :
    https://huggingface.co/learn/llm-course/chapter1/1

### 9.5 Sources pour ameliorer la phase actuelle

21. **Basthon** -- Fork JupyterLite pour l'Education nationale :
    https://basthon.fr/

22. **nbautoeval** -- Exercices auto-evalues (MOOC Python FUN) :
    https://github.com/parmentelat/nbautoeval

23. **JupyterQuiz** -- QCM interactifs pour Jupyter :
    https://github.com/jmshea/jupyterquiz

24. **asciichartpy** -- Graphiques ASCII, 0 dependance :
    https://github.com/kroitor/asciichart

25. **BertViz** -- Visualisation de l'attention (technique) :
    https://github.com/jessevig/bertviz

26. **TrAVis** -- Visualiseur d'attention dans le navigateur :
    https://github.com/ayaka14732/TrAVis

27. **La Scientotheque - Ressources IA** -- Association belge :
    https://lascientotheque.github.io/ressources-ia/

28. **Class'Code IAI** -- MOOC citoyen Inria :
    https://www.fun-mooc.fr/en/courses/lintelligence-artificielle-avec-intelligence/

29. **Gamifying JupyterLab** -- RWTH Aachen (Springer) :
    https://link.springer.com/chapter/10.1007/978-3-031-22124-8_32

### 9.6 Sources pour la phase 2 (PyTorch)

30. **educational-transformer** -- Transformer educatif PyTorch :
    https://github.com/ZSvedic/educational-transformer

31. **picoGPT** -- GPT-2 en ~60 lignes NumPy :
    https://github.com/jaymody/picoGPT

32. **build-nanogpt** -- nanoGPT pas-a-pas par commits :
    https://github.com/karpathy/build-nanogpt

33. **nanoGPT** -- ~600 lignes PyTorch, reproduit GPT-2 :
    https://github.com/karpathy/nanoGPT

34. **nanochat** -- Successeur de nanoGPT (~8k lignes) :
    https://github.com/karpathy/nanochat

35. **ng-video-lecture** -- Fichier unique accompagnant la video nanoGPT :
    https://github.com/karpathy/ng-video-lecture

36. **Neural Networks: Zero to Hero** -- Karpathy, 7 videos :
    https://karpathy.ai/zero-to-hero.html

37. **haikoo** -- GPT-2 fine-tune sur haiku :
    https://github.com/zkg/haikoo

38. **haikurnn** -- RNN + comptage syllabique pour haiku :
    https://github.com/docmarionum1/haikurnn

39. **mini_llm** -- LLM from scratch PyTorch, notebooks :
    https://github.com/Arezkiiiii/mini_llm

40. **PyTorch en une heure** -- Sebastian Raschka :
    https://sebastianraschka.com/teaching/pytorch-1h/

41. **litGPT** -- 20+ LLM from scratch, Lightning AI :
    https://github.com/Lightning-AI/litgpt
