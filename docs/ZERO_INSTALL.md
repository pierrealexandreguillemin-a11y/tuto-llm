# Solutions zero-install pour les notebooks

Ce document recense les solutions permettant d'exécuter les notebooks
du cours **sans installation locale** (pas de venv, pas de pip, pas de
terminal). L'objectif : un lien cliquable et c'est parti.

## Contexte technique

Les 6 notebooks n'utilisent que la **bibliothèque standard Python**
(`math`, `random`, `collections`, `time`). Aucune dépendance externe
n'est requise pour l'exécution. Cette contrainte ouvre la porte aux
solutions 100% navigateur.

---

## Solution recommandee : JupyterLite sur GitHub Pages

[JupyterLite](https://jupyterlite.readthedocs.io/) compile CPython en
WebAssembly via [Pyodide](https://pyodide.org/) et tourne **entierement
dans le navigateur**. Aucun serveur de calcul, aucun compte utilisateur.

### Pourquoi c'est la solution ideale

| Critere | Verdict |
|---------|---------|
| Installation | Aucune -- un lien URL suffit |
| Compte requis | **Non** -- zero compte, zero mot de passe |
| Age (10-14 ans) | Aucune restriction, aucun consentement parental |
| Gratuit | Oui (GitHub Pages = gratuit pour repos publics) |
| stdlib Python | `math`, `random`, `collections`, `time` : tout fonctionne |
| Hors-ligne | Oui, apres la 1re visite (Service Worker) |
| Vie privee | Aucune donnee envoyee a un serveur |
| Maintenance | Zero serveur a gerer, zero cout |

### Mise en place

1. Forker le [template jupyterlite/demo](https://github.com/jupyterlite/demo)
2. Placer les 6 `.ipynb` dans le dossier `content/`
3. Commit sur `main` : GitHub Actions build et deploie automatiquement
4. URL finale : `https://<user>.github.io/<repo>/`

### Point d'attention : notebook 06

Le notebook 06 entraine un modele sur ~1 000 Pokemon (dataset inline,
pas de fichier externe) pendant ~190s en CPython natif. En WebAssembly
(Pyodide), les performances sont **2-5x plus lentes** (~400-950s).

Solutions possibles :

- Reduire le nombre d'epochs (10 -> 3) pour accelerer
- Ajouter une cellule de configuration `MODE = "en_ligne"` / `"local"`
  qui ajuste automatiquement les parametres

---

## Solution secondaire : Google Colab

[Google Colab](https://colab.research.google.com/) execute les notebooks
sur les serveurs de Google. Utile pour les eleves et enseignants qui
disposent deja d'un compte Google.

### Avantages

- Interface soignee, fiable, performante
- Execution CPython native (pas de ralentissement WASM)
- Integration GitHub directe via URL

### Limites

| Critere | Verdict |
|---------|---------|
| Compte requis | **Oui** -- compte Google obligatoire |
| Age (10-14 ans) | Partiel -- les enfants <13 ans necessitent un compte supervise via [Family Link](https://families.google.com/familylink/) |
| Fonctionnalites IA | Reservees aux 18+ |
| Hors-ligne | Non |

### Integration

Ajouter un badge "Open in Colab" dans le README et dans chaque notebook :

```markdown
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/<user>/<repo>/blob/main/notebooks/<notebook>.ipynb)
```

---

## Solution tertiaire : Binder

[Binder](https://mybinder.org/) lance un environnement Jupyter temporaire
depuis un repo GitHub. Aucun compte requis.

### Avantages

- Zero compte, zero inscription
- Lance directement depuis une URL GitHub
- Environnement CPython complet

### Limites

| Critere | Verdict |
|---------|---------|
| Fiabilite | **Fragile** -- projet benevole, financement precaire |
| Demarrage a froid | 1-5 minutes de construction Docker |
| Session | Deconnexion apres 10 min d'inactivite, max 6h |
| Hors-ligne | Non |
| Perennite | Aucune garantie de disponibilite a long terme |

### Integration

Badge dans le README :

```markdown
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/<user>/<repo>/main?labpath=notebooks)
```

---

## Piste bonus : Basthon

[Basthon](https://notebook.basthon.fr/) est un notebook Python en ligne
base sur Pyodide, utilise par l'Education nationale francaise
(~80 000 utilisateurs/semaine). Interface en francais, zero compte,
zero installation.

| Critere | Verdict |
|---------|---------|
| Zero install | Oui |
| Compte requis | Non |
| Age | Aucune restriction |
| Gratuit | Oui |
| Hors-ligne | Oui (apres 1er chargement) |
| Pre-chargement notebooks | Non -- il faut ouvrir/importer chaque fichier manuellement |

Pertinent si le public cible est dans le systeme scolaire francais
et utilise deja [Capytale](https://capytale2.ac-paris.fr/).

---

## Autres solutions evaluees (non retenues)

| Solution | Raison du rejet |
|----------|-----------------|
| **Kaggle Notebooks** | Compte Google requis, consentement parental, interface data-scientist inadaptee aux enfants |
| **GitHub Codespaces** | Age minimum 13 ans (COPPA), interface VS Code trop complexe pour le public cible |
| **VS Code for the Web** | Ne peut pas executer de code sans backend externe |
| **Replit** | Age minimum 13 ans, Jupyter n'est pas un citoyen de premiere classe, credits limites |
| **CoCalc** | Compte email requis, tier gratuit tres limite (pas d'internet, timeout court) |
| **marimo WASM** | Format `.py` proprietaire, incompatible avec `.ipynb` sans conversion |

---

## Comparatif synthetique

| Solution | Zero install | Sans compte | OK 10-14 | Gratuit | Hors-ligne | Fiabilite |
|----------|:---:|:---:|:---:|:---:|:---:|---|
| **JupyterLite** | oui | **oui** | **oui** | oui | oui | Bonne |
| **Google Colab** | oui | non | partiel | oui | non | Excellente |
| **Binder** | oui | **oui** | **oui** | oui | non | Fragile |
| **Basthon** | oui | **oui** | **oui** | oui | oui | Bonne |

---

## Strategie recommandee : multi-canal

1. **Canal principal** -- JupyterLite sur GitHub Pages :
   un lien dans le README, l'enfant clique et code.

2. **Canal secondaire** -- Badges "Open in Colab" :
   pour les eleves/enseignants avec un compte Google.

3. **Canal de secours** -- Binder :
   pour les ateliers ponctuels ou la friction zero est prioritaire
   sur la fiabilite.

4. **Installation locale** (optionnel, pour contributeurs) :
   venv + `pip install -r requirements.txt` comme documente
   dans [CONTRIBUTING.md](../CONTRIBUTING.md).
