# Audit pedagogique -- Tuto LLM (6 notebooks)

| Champ | Valeur |
|-------|--------|
| **Projet** | Tuto LLM -- Creer son mini-LLM (10-14 ans) |
| **Auditeur** | Professeur certifie Education nationale, Technologie et Sciences physiques, cycle 4 |
| **Qualifications** | 15 ans d'experience, certification PIX Edu (expert), referent numerique, membre GT academique IA |
| **Date** | 2026-02-27 |
| **Perimetre** | 6 notebooks Jupyter, documentation associee, conformite aux programmes cycle 4 |
| **Referentiels** | BO cycle 4 (R1), Socle commun (R2), CRCN/PIX (R3), Referentiels pedagogiques (R4), Cadre ethique IA (R5) |

---

## Sommaire

1. [Tableau de synthese](#1-tableau-de-synthese)
2. [Points forts (top 5)](#2-points-forts-top-5)
3. [Non-conformites](#3-non-conformites)
4. [Recommandations](#4-recommandations)
5. [Fiche sequence](#5-fiche-sequence--nb01-deviner-la-suite)
6. [Verdict final](#6-verdict-final)

---

## 1. Tableau de synthese

| Notebook | A. Curriculum | B. Accessibilite | C. Rigueur | D. Ingenierie | E. Ethique | F. Deploiement | Moy. |
|----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| NB01 -- Deviner la suite | 4 | 4 | 5 | 5 | 3 | 4 | **4.2** |
| NB02 -- Apprendre des erreurs | 4 | 4 | 4 | 5 | 3 | 4 | **4.0** |
| NB03 -- La memoire du modele | 4 | 3 | 5 | 4 | 3 | 3 | **3.7** |
| NB04 -- L'attention | 4 | 4 | 5 | 4 | 3 | 4 | **4.0** |
| NB05 -- Mon premier LLM | 5 | 3 | 5 | 5 | 4 | 4 | **4.3** |
| NB06 -- Entrainer le modele | 5 | 3 | 5 | 4 | 5 | 3 | **4.2** |
| **Moyenne** | **4.3** | **3.5** | **4.8** | **4.5** | **3.5** | **3.7** | **4.1** |

Echelle : 5=Exemplaire, 4=Conforme, 3=Acceptable, 2=Insuffisant, 1=Non conforme

### Commentaires par dimension

**A. Alignement curriculaire (4.3/5)** : Excellent ancrage dans CT 4.2 (algorithmique/codage) et D4 du socle (modelisation). La progression Bloom est bien respectee. Le lien avec les probabilites (Mathematiques cycle 4) est naturel. Le NB05 et NB06 atteignent le niveau "Creer" de la taxonomie.

**B. Accessibilite et inclusion (3.5/5)** : Le vocabulaire est globalement adapte, les analogies sont efficaces. Mais les NB03, NB05 et NB06 presentent une charge cognitive elevee (nombreux concepts nouveaux, code long). Aucune differenciation explicite n'est prevue. Le jargon anglais n'est pas systematiquement traduit des la premiere occurrence.

**C. Rigueur scientifique (4.8/5)** : Remarquable. Les explications sont scientifiquement correctes, les analogies explicitement marquees comme simplifications, les sources systematiquement citees (ISO 42001). La comparaison mini-LLM / ChatGPT est honnete et chiffree.

**D. Ingenierie pedagogique (4.5/5)** : Tres bonne application des patterns jupyter4edu et des conventions Callysto. Les bannieres exercice(), les delimiteurs MODIFIE ICI, les fonctions verifier() avec feedback couleur sont exemplaires. Les visualisations interactives (heatmap, barres SVG, courbe de loss, BertViz) sont pedagogiquement pertinentes.

**E. Esprit critique et ethique IA (3.5/5)** : Le NB06 excelle avec les sections "En vrai..." et le tableau comparatif. Mais les NB01-NB04 ne traitent pas l'esprit critique ni les limites societales de l'IA. La question des biais n'est abordee nulle part.

**F. Deploiement en contexte scolaire (3.7/5)** : Compatible JupyterLite et Colab (badges). Mais le NB06 (~3 min d'entrainement) est problematique pour une seance de 45 min. Pas de guide enseignant, pas de grille d'evaluation formelle. Le NB03 (~15s d'entrainement) est a la limite pour un public impatient.

---

## 2. Points forts (top 5)

### PF-1. Unicite du positionnement pedagogique

**Referentiel** : R4 (Benchmark PEDAGOGICAL_PRACTICES.md, Section 6)

Aucun projet existant ne combine toutes les caracteristiques de Tuto LLM : LLM complet (embeddings + attention + entrainement) en Python pur (0 dependance), pour les 10-14 ans, en francais, avec une progression pedagogique documentee. La documentation PEDAGOGICAL_PRACTICES.md benchmarke 12 projets similaires et demontre ce positionnement unique. Dans le contexte du module IA obligatoire en 4e (rentree 2025), cette ressource comble un manque reel.

### PF-2. Progression pedagogique exemplaire (scaffolding)

**Referentiel** : R4 (jupyter4edu "Scaffolding", EPFL "Progression", Bloom)

La progression sur 6 notebooks suit une logique impeccable :
- NB01 : compter (probabilites) -- niveau Bloom "Comprendre"
- NB02 : ajuster (loss, gradient) -- niveau "Appliquer"
- NB03 : memoriser (embeddings, contexte) -- niveau "Appliquer"
- NB04 : focaliser (attention, Q/K/V) -- niveau "Analyser"
- NB05 : assembler (LLM complet) -- niveau "Evaluer"
- NB06 : entrainer (retropropagation) -- niveau "Creer"

Chaque notebook construit sur les precedents. La meme liste de 20 Pokemon est reutilisee de NB01 a NB05, assurant la continuite.

### PF-3. Bannieres exercice() et feedback verifier()

**Referentiel** : R4 (Capytale, EPFL "Feedback immediat", jupyter4edu "Target Practice")

Chaque exercice est encadre par :
- Une banniere HTML bleue (`exercice(N, titre, consigne, observation)`) avec le titre, la consigne, et "Ce que tu vas voir"
- Des delimiteurs visuels Unicode (boites `A TOI DE JOUER !`)
- Une fonction `verifier()` avec feedback colore (vert = reussi, ambre = aide)
- Un compteur de progression (carres verts/blancs + ratio N/total)
- Un bandeau de felicitation quand tous les exercices sont termines

Cette systematique sur les 18 exercices (4+3+3+2+3+3) est conforme aux standards Capytale et jupyter4edu. Le feedback est immediat (EPFL cle 3) et positif.

### PF-4. Analogies pedagogiques ancrees dans le quotidien

**Referentiel** : R4 (ML for Kids "Vocabulaire adapte", py-edu-fr "Analogie avant le code")

Les analogies choisies sont remarquables pour le public cible :
- **NB01** : T9 / clavier predictif (experience quotidienne des eleves)
- **NB02** : Lancer au panier (correction progressive)
- **NB03** : Carte d'identite numerique pour chaque lettre (embeddings)
- **NB04** : Salle de classe (Q = question, K = pancarte, V = info)
- **NB05** : Filtre qui transforme des pixels (matrice)
- **NB06** : Chaine de dominos (retropropagation)

Chaque analogie est introduite AVANT le code (conforme py-edu-fr) et explicitement marquee comme simplification (conforme ISO 42001).

### PF-5. Visualisations interactives sans dependance

**Referentiel** : R4 (PEDAGOGICAL_PRACTICES.md Section 7.1), R3 (CRCN 5.2)

16 visualisations HTML/SVG/JS implementees via `display(HTML(...))` sans aucune dependance externe :
- Heatmap interactive des bigrammes avec survol (NB01)
- Barres de probabilites animees SVG (NB01-NB06)
- Courbe de loss animee avec points hover (NB02, NB06)
- Scatter 2D des embeddings avec legende voyelles/consonnes (NB03)
- BertViz-style attention avec lignes d'opacite variable (NB04, NB05)
- Masque causal interactif cliquable (NB04)
- Schema d'architecture avec connexions residuelles (NB05)
- Slider temperature en temps reel (NB05)
- Animation de generation lettre par lettre (NB01, NB05, NB06)

Compatibles JupyterLite, 0 installation. Chaque visualisation est marquee `<!-- tuto-viz -->` pour les tests automatises ISO 29119.

---

## 3. Non-conformites

### [NC-01] Absence de differenciation pedagogique

**Referentiel** : R1 (BO cycle 4 : "Permettre a chaque eleve de progresser a son rythme"), R4 (Callysto : attention ~10 min)
**Notebook(s)** : Tous (NB01-NB06)
**Constat** : Aucun mecanisme de differenciation n'est prevu. Tous les eleves suivent le meme parcours lineaire. Pas de cellules "Pour aller plus loin" pour les eleves rapides, pas de cellules d'aide supplementaire pour les eleves en difficulte. Les 18 exercices sont tous de niveau comparable au sein de chaque notebook (principalement "Modifier une valeur").
**Impact** : Dans une classe de 30 eleves heterogenes (typique REP/REP+), les eleves rapides terminent en 15 min et s'ennuient, les eleves en difficulte restent bloques sans alternative. L'attention des 10-12 ans chute apres 10 min sur la meme activite.
**Recommandation** : Ajouter dans chaque notebook : (a) 1-2 cellules "Defi" optionnelles de niveau Bloom "Creer" pour les rapides, (b) des cellules "Coup de pouce" avec des indices supplementaires, (c) des variantes simplifiees des exercices. Utiliser des cellules markdown conditionnelles ("Si tu es bloque, lis ceci").
**Priorite** : MAJEUR

---

### [NC-02] Charge cognitive excessive dans NB03 et NB06

**Referentiel** : R4 (Callysto : max 4 cellules entre exercices), R1 (BO : adaptation au rythme)
**Notebook(s)** : NB03 (cellules 10-17 : 8 cellules entre exercice 2 et exercice 3), NB06 (cellules 16-22 : 7 cellules entre exercice 1 et exercice 2)
**Constat** :
- NB03 : entre l'exercice 2 (cell 9) et l'exercice 3 (cell 23), il y a 13 cellules de code et markdown comprenant l'initialisation du reseau, le forward pass, le softmax, l'entrainement complet (100 epochs), la visualisation des embeddings, et la generation. C'est un bloc massif sans interaction.
- NB06 : entre l'exercice 1 (cell 15) et l'exercice 2 (cell 22), il y a 6 cellules dont la retropropagation (~80 lignes de code) et l'entrainement (~3 min). L'eleve est passif pendant une longue duree.
**Impact** : Decrochage des eleves de 10-12 ans apres 3-4 cellules sans interaction (regle Callysto). Le NB03 viole cette regle de facon significative. Le NB06 est a la limite mais le temps d'attente de l'entrainement (~3 min) aggrave le probleme.
**Recommandation** : (a) NB03 : ajouter un exercice intermediaire entre l'entrainement et la generation (ex: "Avant de generer, observe la loss : a-t-elle baisse ? Ecris ta reponse"). (b) NB06 : exploiter le temps d'entrainement avec un exercice de lecture active ("Pendant l'entrainement, lis la section 'En vrai...' et reponds a cette question"). (c) Decouper les blocs de code longs en sous-cellules avec des print() intermediaires.
**Priorite** : MAJEUR

---

### [NC-03] Jargon anglais non systematiquement traduit a la premiere occurrence

**Referentiel** : R4 (py-edu-fr : variables en francais, ML for Kids : vocabulaire adapte), R2 (Socle D1 : langages)
**Notebook(s)** : NB01 (cell 9 : "bigrammes" introduit sans definition claire), NB02 (cell 2 : "loss" utilise avant d'etre defini), NB03 (cell 2 : "embeddings" utilise dans le titre avant explication), NB04 (cell 2 : "Query", "Key", "Value" en anglais), NB05 (cell 3 : "forward pass", "EMBED_DIM", "HIDDEN_DIM", "NUM_HEADS"), NB06 (cell 16 : "backpropagation", "backward", "cache", "SGD")
**Constat** : De nombreux termes techniques anglais sont utilises dans le code et les explications. Certains sont traduits dans le texte markdown mais pas systematiquement. Le terme "loss" est utilise 47 fois dans les notebooks sans jamais etre traduit par "perte" ou "erreur" de facon systematique. Les noms de variables sont en anglais dans le code (`EMBED_DIM`, `HIDDEN_DIM`, `forward`, `backward`, `cache`). Le terme "softmax" n'est jamais traduit ni decompose etymologiquement.
**Impact** : Pour un eleve de 5e (10-11 ans) qui ne parle pas anglais, l'accumulation de termes non traduits cree une barriere d'entree. L'eleve peut executer le code sans comprendre les noms de fonctions et variables.
**Recommandation** : (a) A chaque premiere occurrence d'un terme anglais, ajouter la traduction entre parentheses : "la loss (l'erreur)", "le forward pass (la passe avant : on avance dans le calcul)". (b) Creer un glossaire dans une cellule markdown en debut de chaque notebook (ou un glossaire global). (c) Les noms de constantes comme `EMBED_DIM` sont acceptables (convention Python) mais doivent etre expliques dans un commentaire a la premiere occurrence.
**Priorite** : MAJEUR

---

### [NC-04] Absence de traitement des biais et de l'esprit critique IA

**Referentiel** : R2 (Socle D3 : esprit critique, D5 : impact societal), R5 (Vademecum IA DGESCO 2024), R3 (CRCN 4.2)
**Notebook(s)** : NB01-NB04 (absence totale), NB05-NB06 (traitement partiel)
**Constat** : La question des biais n'est abordee dans aucun notebook. Le dataset Pokemon est presente comme neutre alors qu'il contient des biais (dominance de certaines sonorites, noms inventes par une entreprise japonaise, adaptations culturelles). Les sections "En vrai..." du NB06 traitent bien la comparaison d'echelle et les limites techniques, mais pas :
- Les biais dans les donnees d'entrainement (un LLM entraine sur Internet reproduit les biais d'Internet)
- Les risques de desinformation (l'IA "invente" sans comprendre)
- L'impact environnemental (GPT-4 : 25 000 GPU pendant des mois)
- L'impact sur l'emploi
Le NB05 cell 29 compare les parametres mais pas les implications societales.
**Impact** : L'eleve termine le cours en sachant construire un mini-LLM mais sans posture critique face a l'IA generative. Or le socle commun D3 exige la formation de l'esprit critique, et le vademecum IA DGESCO 2024 insiste sur l'education a la posture critique face aux IA generatives.
**Recommandation** : (a) Ajouter dans NB01 une cellule "Attention : notre modele ne comprend rien, il imite" apres la generation. (b) Ajouter dans NB06 une section "Les limites et les risques de l'IA" couvrant biais, hallucinations, environnement. (c) Ajouter 1 exercice de reflexion (pas de code) : "Le modele genere 'Pikachien'. Est-ce un vrai Pokemon ? Comment savoir ? Peut-on faire confiance a l'IA ?"
**Priorite** : MAJEUR

---

### [NC-05] Absence de guide enseignant et de grille d'evaluation

**Referentiel** : R1 (BO : evaluation des competences), R4 (Capytale : support enseignant)
**Notebook(s)** : Transversal
**Constat** : Le projet ne contient aucun document a destination des enseignants :
- Pas de fiche de preparation (objectifs, prerequis, deroulement, evaluation)
- Pas de grille d'evaluation des competences (CT 4.2, D1, D2, D4)
- Pas de corrige des exercices
- Pas de guide d'installation pour un college (proxy, pare-feu, JupyterLite)
- Pas de scenarios d'erreur et leurs solutions (erreur Shift+Entree, cellule sautee, kernel bloque)
La fonction `verifier()` est un feedback immediat mais pas une evaluation formelle.
**Impact** : Un enseignant non specialiste IA (cas majoritaire en college) ne peut pas deployer ces notebooks sans un investissement personnel important. L'evaluation des competences acquises repose entierement sur l'observation directe, sans trace exploitable.
**Recommandation** : (a) Creer un document `docs/GUIDE_ENSEIGNANT.md` avec les 6 fiches de sequence (voir section 5 pour un exemple). (b) Creer une grille d'evaluation par competence alignee sur le socle commun. (c) Ajouter une FAQ "problemes courants en classe" (kernel mort, cellule sautee, erreur Python).
**Priorite** : MAJEUR

---

### [NC-06] Le NB06 depasse la duree d'une seance de 45 minutes

**Referentiel** : R1 (BO : "seance" = 45 min ou 1h30 quinzaine), R4 (Callysto : attention limitee)
**Notebook(s)** : NB06
**Constat** : Le NB06 contient 31 cellules avec un entrainement de ~1-3 minutes (cell 20), une retropropagation de ~80 lignes (cell 18), 3 exercices, et des sections "En vrai..." (cells 23-24). Le temps realiste pour un eleve de 3e est :
- Lecture + execution des cellules d'initialisation : ~5 min
- Exercice 1 (generation avant entrainement) : ~5 min
- Lecture retropropagation + entrainement : ~10 min (dont ~3 min d'attente)
- Exercice 2 (observation) : ~3 min
- Sections "En vrai..." : ~5 min
- Generation apres entrainement : ~5 min
- Exercice 3 (exploration) : ~5 min
- Resume + sources : ~3 min
Total estime : ~41 min sans compter les aleas (questions, problemes techniques, relecture). Avec un public de 10-14 ans et les aleas de classe, cela depasse systematiquement les 45 min.
**Impact** : L'enseignant devra couper la seance en deux ou supprimer des parties. Sans guide, il ne saura pas ou couper.
**Recommandation** : (a) Prevoir un decoupage explicite en 2 demi-seances : "Partie A : le backward (cellules 1-18)" et "Partie B : l'entrainement et la generation (cellules 19-30)". (b) Marquer les sections "En vrai..." comme optionnelles ("Pour aller plus loin, si tu as le temps"). (c) Documenter ce decoupage dans le guide enseignant.
**Priorite** : MINEUR

---

### [NC-07] Cellule d'initialisation opaque et intimidante

**Referentiel** : R4 (jupyter4edu "Shift-Enter for the Win"), R4 (Callysto "Titre clair en haut")
**Notebook(s)** : Tous (NB01-NB06)
**Constat** : Chaque notebook commence par une cellule d'initialisation de 80-200 lignes de code Python (cell 1 dans tous les notebooks) contenant les fonctions `verifier()`, `exercice()`, et les fonctions de visualisation. L'instruction est "execute sans lire (Shift+Entree)". Pour un eleve de 10 ans qui decouvre Jupyter, cette premiere cellule massive de code inconnu peut etre intimidante. Le texte "execute sans lire" va a l'encontre de la posture de comprehension promeue par le cours.
**Impact** : Risque de decrochage des la premiere cellule. L'eleve peut se sentir submerge par du code incomprehensible avant meme de commencer.
**Recommandation** : (a) Reduire visuellement la cellule d'initialisation en la collapsant si possible (metadata JupyterLab `collapsed: true`). (b) Ajouter une ligne de commentaire plus rassurante : "# Cette cellule prepare les outils. Tu n'as pas besoin de la comprendre pour le moment. Execute-la simplement." (c) Deplacer l'explication "Comment ca marche ?" AVANT la cellule d'initialisation dans les notebooks ou ce n'est pas deja le cas.
**Priorite** : MINEUR

---

### [NC-08] Accessibilite numerique limitee (daltonisme, contraste)

**Referentiel** : R2 (Socle : accessibilite), R5 (RGAA)
**Notebook(s)** : NB01-NB06 (toutes les visualisations)
**Constat** : Les visualisations utilisent un code couleur bleu (#1565c0) / vert (#28a745, #d4edda) / rouge (#e53935) / ambre (#ffc107, #fff3cd) sans alternative textuelle systematique. Le scatter 2D des embeddings (NB03) distingue voyelles (rouge) et consonnes (bleu) uniquement par la couleur. Les bannieres de feedback (vert = reussi, ambre = aide) reposent sur la couleur pour communiquer le resultat. Les heatmaps utilisent l'opacite comme seul indicateur de valeur.
**Impact** : Un eleve daltonien (8% des garcons, soit 1-2 par classe) ne peut pas distinguer voyelles/consonnes dans le scatter NB03, ni interpreter facilement le feedback des exercices.
**Recommandation** : (a) Ajouter des indicateurs textuels en complement de la couleur : icone "V"/"C" dans le scatter, texte "Bravo !" / "Essaie encore" lisible meme sans la couleur. (b) Utiliser des motifs differents (pointilles, hachures) en plus des couleurs dans les graphiques. (c) Verifier le contraste avec un outil WCAG (les textes #555 sur fond blanc sont a la limite du ratio 4.5:1).
**Priorite** : MINEUR

---

### [NC-09] Exercices majoritairement de niveau "Modifier" (Bloom 3)

**Referentiel** : R4 (Kaggle Learn : difficulte croissante), R1 (BO : "Creer, concevoir")
**Notebook(s)** : NB01-NB06
**Constat** : Sur les 18 exercices, la majorite demande de changer une variable et observer l'effet (niveau Bloom "Appliquer"). Detail :
- NB01 : Ex1 = Completer ("u"), Ex2 = Completer (pokemons[-1]), Ex3 = Modifier (ma_lettre), Ex4 = Modifier (nombre)
- NB02 : Ex1 = Modifier (ma_prediction), Ex2 = Modifier (vitesse_test), Ex3 = Modifier (nombre)
- NB03 : Ex1 = Modifier (EMBED_DIM_test), Ex2 = Modifier (context_test), Ex3 = Modifier (nombre)
- NB04 : Ex1 = Modifier (ma_lettre), Ex2 = Modifier (mon_mot)
- NB05 : Ex1 = Modifier (EMBED_DIM_test), Ex2 = Modifier (mon_debut), Ex3 = Modifier (ma_temperature)
- NB06 : Ex1 = Modifier (ma_temperature), Ex2 = Observer, Ex3 = Modifier (ma_temperature + mon_debut)

15/18 exercices = "Change la variable X et observe". Seuls les exercices NB01-Ex1 ("quelle lettre suit Q ?") et NB01-Ex2 (pokemons[-1] / len) demandent une reflexion. Aucun exercice de niveau "Creer" (ecrire une fonction, concevoir un test).
**Impact** : L'eleve developpe la competence "Executer/Observer" mais pas "Concevoir/Creer". Le niveau taxonomique reste bas pour des 3e. La repetitivite peut lasser les eleves rapides.
**Recommandation** : (a) Ajouter 1 exercice de niveau "Creer" par notebook a partir du NB03 (ex: "Ecris une fonction qui compte les noms generes de plus de 6 lettres"). (b) Ajouter des exercices de reflexion sans code (ex: "Pourquoi la loss ne descend jamais a 0 ?"). (c) Varier les types d'exercices : QCM, vrai/faux, exercice a trous, exercice de debug.
**Priorite** : MINEUR

---

### [NC-10] Propriete intellectuelle : copyright Nintendo insuffisamment signale dans les notebooks

**Referentiel** : R5 (Propriete intellectuelle, RGPD)
**Notebook(s)** : NB01-NB06
**Constat** : Les noms de Pokemon sont des marques deposees de Nintendo / Creatures Inc. / GAME FREAK inc. Le fichier `data/pokemon.txt` contient un commentaire de copyright et le `DATASETS.md` documente la licence. Cependant, dans les notebooks eux-memes, le copyright n'est mentionne que dans la cellule finale "Sources (ISO 42001)" en petits caracteres. La liste de 20 Pokemon en dur dans NB01-NB05 (cell 5 de NB01, cell 9 de NB02, etc.) n'a aucune mention de copyright a cote. Le NB06 cell 3 contient ~1000 noms de Pokemon inline avec un commentaire de copyright en debut de cellule -- c'est le seul notebook a le faire correctement a proximite des donnees.
**Impact** : En contexte scolaire, l'enseignant pourrait etre interroge sur le droit d'utiliser ces noms. La mention en fin de notebook est facile a rater.
**Recommandation** : (a) Ajouter un commentaire `# (c) Nintendo -- usage educatif` a cote de la liste des 20 Pokemon dans les NB01-NB05. (b) C'est deja fait dans le NB06 cell 3 -- generaliser cette pratique.
**Priorite** : MINEUR

---

## 4. Recommandations

### Priorite BLOQUANTE

Aucune non-conformite bloquante. Le projet est deployable sous reserve des corrections MAJEURES ci-dessous.

### Priorite MAJEURE

| # | Recommandation | NC | Effort | Impact |
|---|---------------|:---:|:---:|:---:|
| R1 | Ajouter des mecanismes de differenciation (cellules "Defi" et "Coup de pouce") | NC-01 | M | Fort |
| R2 | Reduire les blocs sans exercice (max 4 cellules) dans NB03 et NB06 | NC-02 | S | Fort |
| R3 | Traduire systematiquement le jargon anglais + creer un glossaire | NC-03 | S | Moyen |
| R4 | Ajouter 1 section ethique/biais/limites dans NB01 et NB06 | NC-04 | M | Fort |
| R5 | Creer un guide enseignant avec fiches de sequence et grille d'evaluation | NC-05 | L | Fort |

### Priorite MINEURE

| # | Recommandation | NC | Effort | Impact |
|---|---------------|:---:|:---:|:---:|
| R6 | Prevoir un decoupage du NB06 en 2 demi-seances | NC-06 | S | Moyen |
| R7 | Rendre la cellule d'initialisation moins intimidante | NC-07 | S | Moyen |
| R8 | Ameliorer l'accessibilite des visualisations (daltonisme, contraste) | NC-08 | M | Moyen |
| R9 | Varier les niveaux taxonomiques des exercices (ajouter "Creer") | NC-09 | M | Moyen |
| R10 | Generaliser la mention copyright Nintendo pres des donnees | NC-10 | S | Faible |

Effort : S = 1-2h, M = demi-journee, L = 1-2 jours

---

## 5. Fiche sequence -- NB01 "Deviner la suite"

### Informations generales

| Champ | Valeur |
|-------|--------|
| **Niveau** | 4eme ou 3eme (cycle 4) |
| **Discipline** | Technologie (CT 4.2) ou Mathematiques (probabilites) |
| **Place dans la progression** | Seance 1/6 d'une sequence "Decouvrir l'IA generative" |
| **Duree** | 45 minutes (1 seance) |
| **Effectif** | Classe entiere ou demi-groupe (ideal : 15-18 eleves) |
| **Salle** | Salle informatique avec navigateur web (JupyterLite ou Colab) |
| **Prerequis materiel** | 1 poste par eleve, navigateur recents (Chrome/Firefox/Edge) |

### Objectifs

**Savoirs** :
- Savoir qu'un modele de langage predit la suite en se basant sur des probabilites (CT 4.2)
- Savoir qu'une probabilite est un nombre entre 0 et 1 qui mesure une chance (Mathematiques)

**Savoir-faire** :
- Savoir executer un notebook Jupyter (Shift+Entree) (CRCN 3.4)
- Savoir lire et modifier une variable Python (CRCN 3.4)
- Savoir interpreter un tableau de probabilites (Mathematiques)

**Competences du socle** :
- D1.3 : Comprendre et utiliser les langages mathematiques et informatiques
- D2 : Cooperer et utiliser des outils numeriques pour apprendre
- D4 : Concevoir et modeliser un systeme simple

### Prerequis eleves

- Savoir utiliser un navigateur web
- Connaitre les bases de Python : variables, print(), listes (peut etre acquis en amont via Scratch -> Python)
- Notion intuitive de "probabilite" (frequence, chance)

### Deroulement

| Temps | Phase | Activite professeur | Activite eleve | Differenciation |
|:---:|---|---|---|---|
| 0-5 min | **Accroche** | Projeter un clavier de telephone avec suggestion de mots. "Comment le telephone devine-t-il ?" | Reponses orales, discussion collective | -- |
| 5-10 min | **Mise en route** | Distribuer le lien JupyterLite/Colab. Montrer au videoprojecteur : "Cliquez sur la premiere cellule grise, puis Shift+Entree". | Ouvrir le notebook. Executer la cellule d'initialisation (cell 0-1). | Aide individuelle pour les eleves qui ne trouvent pas le notebook |
| 10-15 min | **Exercice 1** : Quelle lettre suit Q ? | Circuler, verifier que tous ont reussi le premier exercice. | Lire la cell 2, executer cell 3, repondre "u". Observer le feedback vert. | Eleves rapides : "Essaie avec d'autres lettres dans ta tete" |
| 15-20 min | **Exercice 2** : Explorer la liste | Rappel : `pokemons[-1]` = dernier element, `len()` = longueur. | Executer cells 4-7, completer les deux variables. | Coup de pouce : ecrire au tableau `pokemons[-1]` et `len("bulbizarre")` |
| 20-30 min | **Decouverte** : Bigrammes et heatmap | Expliquer au videoprojecteur : "On compte quelle lettre suit quelle autre". Montrer la heatmap. | Executer cells 8-9. Observer la heatmap. Exercice 3 : changer `ma_lettre`. | Eleves rapides : "Trouve la paire la plus frequente dans la heatmap" |
| 30-40 min | **Generation** : Inventer des Pokemon | "Maintenant, on utilise les probabilites pour generer des noms." | Executer cells 12-15. Observer les noms generes. Exercice 4 : generer 50 noms. | Eleves en difficulte : aide pour changer `nombre`. Eleves rapides : "Quel est le meilleur nom ? Pourquoi ?" |
| 40-45 min | **Bilan** | Synthese au tableau : "Le modele ne regarde qu'1 lettre en arriere. C'est une limite." | Lire cells 18-19 ("Ce qu'on a appris"). | -- |

### Evaluation formative

| Critere | Observable | Niveau 1 (fragile) | Niveau 2 (satisfaisant) | Niveau 3 (expert) |
|---------|-----------|---|---|---|
| Executer un notebook | Shift+Entree sur toutes les cellules | Execute avec aide | Execute seul dans l'ordre | Execute et re-execute pour experimenter |
| Modifier une variable | Exercices 3 et 4 | Ne modifie pas ou erreur de syntaxe | Modifie la valeur et observe | Modifie et commente le resultat |
| Interpreter les probabilites | Lecture de la heatmap | Ne comprend pas les pourcentages | Lit les probabilites correctement | Explique pourquoi certaines paires sont frequentes |
| Esprit critique | Discussion sur les noms generes | Accepte tous les noms comme "bons" | Distingue les noms "credibles" des "mauvais" | Explique la limite du modele (1 seule lettre) |

### Prolongements

- **Seance suivante** : NB02 -- Apprendre de ses erreurs (la loss et le gradient)
- **Lien Mathematiques** : reprendre les probabilites du NB01 dans le cours de probabilites (lancer de de -> distribution de frequences -> probabilite)
- **Lien EMC** : debat "Peut-on faire confiance a une IA qui invente des mots ?"
- **EPI possible** : "L'IA et la creation" (Technologie + Francais + Arts plastiques) -- generer des noms puis creer les creatures correspondantes

---

## 6. Verdict final

### Le projet est-il deployable en college en l'etat ?

**Reponse : OUI, sous reserve de 3 actions prioritaires.**

Le projet Tuto LLM est une ressource pedagogique remarquable qui comble un manque reel dans le paysage educatif francais. Sa rigueur scientifique (4.8/5), son ingenierie pedagogique (4.5/5) et son alignement curriculaire (4.3/5) sont exemplaires. Le positionnement unique (LLM complet, Python pur, 10-14 ans, francais) en fait une ressource sans equivalent.

Cependant, pour un deploiement en contexte scolaire reel (classe heterogene de 25-30 eleves, enseignant non specialiste IA, contrainte de 45 min par seance), trois actions sont prioritaires :

### Les 3 actions prioritaires avant deploiement

**1. Creer un guide enseignant (effort : L, impact : fort)**
Sans guide, seuls les enseignants deja a l'aise avec Python et l'IA pourront deployer ces notebooks. Le guide doit contenir : 6 fiches de sequence (une par notebook), une grille d'evaluation par competences du socle, un corrige des 18 exercices, une FAQ technique (installation, problemes courants), et un scenario de decoupage du NB06 en 2 seances.

**2. Ajouter une dimension ethique/critique (effort : M, impact : fort)**
Le socle commun D3 et le vademecum IA DGESCO 2024 exigent la formation de l'esprit critique face a l'IA. Ajouter dans NB01 une cellule "Le modele ne comprend rien, il imite" et dans NB06 une section "Limites et risques" couvrant biais, hallucinations, et impact environnemental. Ajouter au moins 1 exercice de reflexion (pas de code) par sequence de 2 notebooks.

**3. Prevoir la differenciation (effort : M, impact : fort)**
Ajouter des cellules "Defi" pour les eleves rapides et des "Coups de pouce" pour les eleves en difficulte. Reduire les blocs sans exercice a 4 cellules maximum (regle Callysto). Cela concerne principalement NB03 (13 cellules sans interaction) et NB06 (7 cellules + 3 min d'attente).

### Synthese

| Critere | Evaluation |
|---------|-----------|
| Qualite scientifique | Exemplaire -- rien a corriger |
| Qualite pedagogique (ingenierie) | Tres bonne -- bannieres, exercices, visualisations |
| Qualite pedagogique (differenciation) | Insuffisante -- parcours unique pour tous |
| Dimension ethique/critique | Partielle -- present dans NB06 mais absent des NB01-NB04 |
| Deployabilite par un non-specialiste | Insuffisante -- pas de guide enseignant |
| Compatibilite technique | Bonne -- JupyterLite, Colab, 0 dependance |
| Alignement BO cycle 4 | Bon -- CT 4.2, D1, D2, D4 couverts |
| Conformite CRCN/PIX | Bonne -- 1.3, 3.4, 5.2 couverts |

**Note globale : 4.1/5 -- Conforme avec reserves.**

Le projet est pret pour un deploiement pilote (1-2 classes avec enseignant volontaire et a l'aise en Python). Pour un deploiement generalise (formation academique, distribution via Capytale), les 3 actions prioritaires sont necessaires.

---

*Rapport realise le 2026-02-27 par un professeur certifie de l'Education nationale.*
*Referentiels : BO cycle 4, Socle commun, CRCN/PIX, Capytale, EPFL, jupyter4edu, Callysto, Vademecum IA DGESCO 2024.*
