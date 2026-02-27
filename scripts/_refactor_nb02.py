#!/usr/bin/env python3
"""Refactor NB02: Apprendre des erreurs — pedagogical overhaul."""

import json
import re


def md(source):
    return {"cell_type": "markdown", "metadata": {}, "source": source}


def code(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source,
    }


with open("notebooks/02_apprendre_des_erreurs.ipynb", encoding="utf-8") as f:
    nb = json.load(f)

original_cell1 = "".join(
    nb["cells"][1]["source"]
    if isinstance(nb["cells"][1]["source"], list)
    else [nb["cells"][1]["source"]]
)
verifier_match = re.search(
    r"(def verifier\(.*?\n(?:(?:    .*|)\n)*)", original_cell1, re.MULTILINE
)
exercice_match = re.search(
    r"(def exercice\(.*?\n(?:(?:    .*|)\n)*)", original_cell1, re.MULTILINE
)
verifier_code = verifier_match.group(1).rstrip("\n") if verifier_match else ""
exercice_code = exercice_match.group(1).rstrip("\n") if exercice_match else ""

cells = []

# CELL: Intro (markdown)
cells.append(
    md(
        "> **Rappel** : clique sur une cellule grise, puis **Shift + Entree** pour l'executer.\n"
        "> Execute les cellules **dans l'ordre** de haut en bas.\n"
        "\n"
        "La cellule suivante prepare les outils. **Tu n'as pas besoin de la lire**\n"
        "\\u2014 execute-la simplement avec Shift+Entree.\n"
        "\n"
        "---\n"
        "\n"
        "# Lecon 2 : Apprendre de ses erreurs\n"
        "\n"
        "## Le secret de l'IA : se tromper, corriger, recommencer\n"
        "\n"
        "Imagine que tu apprends a lancer une balle dans un panier :\n"
        "1. Tu lances -> tu rates a droite\n"
        "2. Tu corriges un peu a gauche\n"
        "3. Tu relances -> plus pres !\n"
        "4. Tu continues jusqu'a marquer\n"
        "\n"
        "L'IA fait **exactement** pareil. Elle fait une prediction, regarde si c'est\n"
        "bon, et ajuste. Ca s'appelle **l'entrainement**."
    )
)

# CELL: Vocabulaire (markdown)
cells.append(
    md(
        "> **Vocabulaire de cette lecon**\n"
        "> - **loss** : l'erreur du modele (plus c'est bas, mieux c'est)\n"
        "> - **gradient** : la direction de correction (de combien ajuster)\n"
        "> - **epoch** : un passage complet sur toutes les donnees\n"
        "> - **entrainement** (*training*) : le processus d'apprentissage par repetition"
    )
)

# CELL: Infrastructure (code)
infra = (
    "# ============================================================\n"
    "# Cellule d'initialisation \\u2014 execute sans lire (Shift+Entree)\n"
    "# ============================================================\n"
    "\n"
    "import uuid\n"
    "\n"
    "from IPython.display import HTML, display\n"
    "\n"
    "_exercices_faits = set()\n"
    "_NB_TOTAL = 3\n"
    "\n"
    "\n" + verifier_code + "\n"
    "\n"
    "\n" + exercice_code + "\n"
    "\n"
    "\n"
    # afficher_evolution_loss — animated SVG path
    'def afficher_evolution_loss(pertes, titre="Courbe de loss"):\n'
    '    """Courbe de loss animee (la ligne se dessine + hover = valeur)."""\n'
    "    if not pertes:\n"
    "        return\n"
    "    uid = uuid.uuid4().hex[:8]\n"
    "    n = len(pertes)\n"
    "    max_loss = max(pertes)\n"
    "    min_loss = min(pertes)\n"
    "    # Dimensions du SVG\n"
    "    w, h, pad = 500, 160, 30\n"
    "    pw = w - 2 * pad  # largeur zone de dessin\n"
    "    ph = h - 2 * pad  # hauteur zone de dessin\n"
    "    # Construire le path SVG\n"
    "    points = []\n"
    '    circles = ""\n'
    "    for i, loss in enumerate(pertes):\n"
    "        x = pad + (i / max(n - 1, 1)) * pw\n"
    "        y = pad + (1 - (loss - min_loss) / max(max_loss - min_loss, 1e-6)) * ph\n"
    '        points.append(f"{x:.1f},{y:.1f}")\n'
    "        circles += (\n"
    '            f\'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="#1565c0" opacity="0" \'\n'
    "            f'style=\"transition:opacity 0.2s\"><title>Epoch {i}: {loss:.3f}</title></circle>'\n"
    "        )\n"
    '    path_d = "M" + " L".join(points)\n'
    "    path_len = n * 20  # approximation\n"
    "    # Axes\n"
    "    axes = (\n"
    '        f\'<line x1="{pad}" y1="{pad}" x2="{pad}" y2="{h-pad}" stroke="#ccc" stroke-width="1"/>\'\n'
    '        f\'<line x1="{pad}" y1="{h-pad}" x2="{w-pad}" y2="{h-pad}" stroke="#ccc" stroke-width="1"/>\'\n'
    '        f\'<text x="{pad-5}" y="{pad+5}" text-anchor="end" font-size="10" fill="#999">{max_loss:.2f}</text>\'\n'
    '        f\'<text x="{pad-5}" y="{h-pad+4}" text-anchor="end" font-size="10" fill="#999">{min_loss:.2f}</text>\'\n'
    '        f\'<text x="{pad}" y="{h-pad+16}" font-size="10" fill="#999">0</text>\'\n'
    '        f\'<text x="{w-pad}" y="{h-pad+16}" text-anchor="end" font-size="10" fill="#999">{n-1}</text>\'\n'
    "    )\n"
    "    display(HTML(\n"
    "        f'<!-- tuto-viz -->'\n"
    "        f'<div style=\"margin:8px 0\"><b>{titre}</b>'\n"
    '        f\'<svg id="lc{uid}" width="{w}" height="{h}" style="margin-top:4px;display:block;background:#fafafa;border-radius:4px">\'\n'
    "        f'{axes}'\n"
    '        f\'<path d="{path_d}" fill="none" stroke="#1565c0" stroke-width="2" \'\n'
    '        f\'stroke-dasharray="{path_len}" stroke-dashoffset="{path_len}" \'\n'
    "        f'style=\"animation:draw{uid} 1.5s ease forwards\"/>'\n"
    "        f'{circles}'\n"
    "        f'</svg>'\n"
    "        f'<style>@keyframes draw{uid}{{to{{stroke-dashoffset:0}}}}</style>'\n"
    "        f'<script>(function(){{'\n"
    "        f'var svg=document.getElementById(\"lc{uid}\");'\n"
    "        f'svg.addEventListener(\"mouseover\",function(e){{'\n"
    '        f\'var c=e.target.closest("circle");if(c)c.setAttribute("opacity","1")}});\'\n'
    "        f'svg.addEventListener(\"mouseout\",function(e){{'\n"
    '        f\'var c=e.target.closest("circle");if(c)c.setAttribute("opacity","0")}})\'\n'
    "        f'}})();</script>'\n"
    "        f'<div style=\"color:#555;font-size:0.85em;margin-top:4px\">'\n"
    "        f'Survole les points pour voir la valeur exacte</div></div>'\n"
    "    ))\n"
    "\n"
    "\n"
    'print("Outils de visualisation charges !")'
)
cells.append(code(infra))

# CELL: Etape 1 — mesurer l'erreur (markdown)
cells.append(
    md(
        "---\n"
        "## Etape 1 : Mesurer l'erreur (la loss)\n"
        "\n"
        "D'abord, il faut un moyen de dire **a quel point** le modele s'est trompe.\n"
        "On appelle ca la **loss** (perte en anglais).\n"
        "\n"
        "- Loss haute = le modele se trompe beaucoup\n"
        "- Loss basse = le modele devine bien\n"
        "\n"
        "Voyons comment ca marche avec un exemple :"
    )
)

# CELL: Loss computation (code)
cells.append(
    code(
        "import math\n"
        "\n"
        "# Imaginons que le modele predit les probabilites suivantes\n"
        "# pour la lettre qui suit 'p' dans 'pikachu' :\n"
        "prediction = {\n"
        '    "i": 0.6,   # 60% -> bonne reponse !\n'
        '    "a": 0.2,   # 20%\n'
        '    "e": 0.15,  # 15%\n'
        '    "o": 0.05,  # 5%\n'
        "}\n"
        "\n"
        "# La bonne reponse est 'i'\n"
        'bonne_reponse = "i"\n'
        "\n"
        "# La loss = -log(probabilite de la bonne reponse)\n"
        "# Si le modele avait dit 100% pour 'i' : loss = 0 (parfait !)\n"
        "# Si le modele avait dit 1% pour 'i' : loss = 4.6 (enorme !)\n"
        "loss = -math.log(prediction[bonne_reponse])\n"
        "print(\n"
        "    f\"Le modele donnait {prediction[bonne_reponse]:.0%} de chance a '{bonne_reponse}'\"\n"
        ")\n"
        'print(f"Loss = {loss:.2f}")\n'
        "print()\n"
        "\n"
        "# Comparons avec une mauvaise prediction\n"
        'mauvaise_prediction = {"i": 0.05, "a": 0.7, "e": 0.2, "o": 0.05}\n'
        "loss_mauvaise = -math.log(mauvaise_prediction[bonne_reponse])\n"
        "print(\n"
        "    f\"Si le modele n'avait donne que {mauvaise_prediction[bonne_reponse]:.0%} a '{bonne_reponse}'...\"\n"
        ")\n"
        'print(f"Loss = {loss_mauvaise:.2f}  (beaucoup plus haut = beaucoup plus faux)")'
    )
)

# CELL: MD before exercise 1
cells.append(md("A toi d'experimenter avec la loss :"))

# CELL: Exercise 1 — loss (code)
cells.append(
    code(
        "exercice(\n"
        "    1,\n"
        '    "Joue avec la perte",\n'
        '    "Change <code>ma_prediction</code> ci-dessous (essaie 0.9 ou 0.01), puis <b>Shift + Entree</b>.",\n'
        '    "Plus ta prediction est loin de la bonne reponse, plus la loss monte.",\n'
        ")\n"
        "\n"
        "# \u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557\n"
        "# \u2551  A TOI DE JOUER !                    \u2551\n"
        "# \u2560\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2563\n"
        "\n"
        "ma_prediction = 0.6  # <-- Change cette valeur ! Essaie 0.9 ou 0.01\n"
        "\n"
        "# \u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d\n"
        "\n"
        "ma_loss = -math.log(ma_prediction)\n"
        'print(f"Si le modele donne {ma_prediction:.0%} de chance a la bonne reponse :")\n'
        'print(f"  Loss = {ma_loss:.2f}")\n'
        "if ma_prediction > 0.8:\n"
        '    print("  -> Tres bien ! Le modele est confiant et a raison.")\n'
        "elif ma_prediction < 0.1:\n"
        '    print("  -> Enorme loss ! Le modele s\'est beaucoup trompe.")\n'
        "else:\n"
        '    print("  -> Moyen. Le modele peut encore s\'ameliorer.")\n'
        "\n"
        "verifier(\n"
        "    1,\n"
        "    ma_prediction != 0.6,\n"
        '    f"Bien joue ! Avec {ma_prediction:.0%}, la loss est {ma_loss:.2f}.",\n'
        '    "Change ma_prediction pour une autre valeur, par exemple 0.9 ou 0.01.",\n'
        ")"
    )
)

# CELL: MD — Etape 2 : Les poids du modele
cells.append(
    md(
        "---\n"
        "## Etape 2 : Les poids du modele\n"
        "\n"
        'Un modele = une collection de **nombres** (les "poids").\n'
        "Ces nombres determinent les predictions. **Entrainer = trouver les bons nombres.**\n"
        "\n"
        "On va creer une grille 27x27 (26 lettres + le point) ou chaque case\n"
        "contient un score. Au debut, les scores sont aleatoires :"
    )
)

# CELL: Weights setup (code)
cells.append(
    code(
        "import math\n"
        "import random\n"
        "\n"
        "# Notre alphabet : 26 lettres + le point (debut/fin)\n"
        'alphabet = list("abcdefghijklmnopqrstuvwxyz.")\n'
        'print(f"Alphabet : {len(alphabet)} symboles")\n'
        "\n"
        '# Scores aleatoires (les "poids" du modele)\n'
        "random.seed(42)\n"
        "poids = {}\n"
        "for a in alphabet:\n"
        "    poids[a] = {}\n"
        "    for b in alphabet:\n"
        "        poids[a][b] = random.uniform(-1, 1)  # nombre entre -1 et 1\n"
        "\n"
        'print(f"Nombre de poids : {len(alphabet)} x {len(alphabet)} = {len(alphabet)**2}")\n'
        "\n"
        "\n"
        "def calculer_probas(poids, lettre):\n"
        '    """Transforme les scores en probabilites (softmax)."""\n'
        "    scores = poids[lettre]\n"
        "    # L'exponentielle rend tous les scores positifs\n"
        "    exps = {b: math.exp(scores[b]) for b in scores}\n"
        "    total = sum(exps.values())  # on divise par le total\n"
        "    return {b: exps[b] / total for b in scores}\n"
        "\n"
        "\n"
        "# Au debut, les probas sont quasi uniformes (le modele devine au hasard)\n"
        'p = calculer_probas(poids, ".")\n'
        "lettres_debut = sorted(p.items(), key=lambda x: -x[1])[:5]\n"
        "print()\n"
        'print("Au debut, le modele pense que les Pokemon commencent par :")\n'
        "for lettre, prob in lettres_debut:\n"
        "    print(f\"  '{lettre}' : {prob:.1%}\")\n"
        "print(\"\\n  -> C'est n'importe quoi ! Il faut l'entrainer.\")"
    )
)

# CELL: MD — Etape 3 : Entrainement
cells.append(
    md(
        "---\n"
        "## Etape 3 : Entrainement\n"
        "\n"
        "L'algorithme est simple :\n"
        "1. Prendre un nom de Pokemon d'entrainement\n"
        "2. Le modele fait sa prediction\n"
        "3. On calcule la loss (l'erreur)\n"
        "4. On **ajuste les poids** pour reduire la loss\n"
        "5. Recommencer\n"
        "\n"
        "L'etape 4 s'appelle la **descente de gradient**. C'est comme ajuster ton\n"
        "tir au panier un petit peu a chaque essai.\n"
        "\n"
        "L'entrainement prend ~2-3 secondes :"
    )
)

# CELL: Training loop (code)
cells.append(
    code(
        "# (c) Nintendo / Creatures Inc. / GAME FREAK inc. -- usage educatif\n"
        "# Les 20 Pokemon d'entrainement\n"
        "pokemons = [\n"
        '    "arcanin", "bulbizarre", "carapuce", "dracaufeu", "ectoplasma",\n'
        '    "evoli", "felinferno", "gardevoir", "goupix", "lokhlass",\n'
        '    "lucario", "metamorph", "mewtwo", "noctali", "pikachu",\n'
        '    "rondoudou", "ronflex", "salameche", "togepi", "voltali",\n'
        "]\n"
        "\n"
        "# Parametres d'entrainement\n"
        "vitesse = 0.1    # de combien on ajuste a chaque fois\n"
        "nb_epochs = 50   # nombre de passages sur les donnees\n"
        "\n"
        'print("Entrainement (~2-3 secondes)...")\n'
        "print()\n"
        "\n"
        "_historique_loss = []  # pour la courbe\n"
        "\n"
        "for epoch in range(nb_epochs):\n"
        "    loss_totale = 0\n"
        "    nb = 0\n"
        "\n"
        "    for pokemon in pokemons:\n"
        '        mot = "." + pokemon + "."  # ex: ".pikachu."\n'
        "        for i in range(len(mot) - 1):\n"
        "            lettre = mot[i]      # lettre courante\n"
        "            cible = mot[i + 1]   # lettre a predire\n"
        "\n"
        "            # 1. Prediction : probas pour chaque lettre suivante\n"
        "            probas = calculer_probas(poids, lettre)\n"
        "\n"
        "            # 2. Loss : a quel point on s'est trompe\n"
        "            loss_totale += -math.log(probas[cible] + 1e-10)\n"
        "            nb += 1\n"
        "\n"
        "            # 3. Ajuster les poids (gradient simplifie)\n"
        "            for b in alphabet:\n"
        "                if b == cible:\n"
        "                    # Bonne reponse : augmenter son score\n"
        "                    poids[lettre][b] += vitesse * (1 - probas[b])\n"
        "                else:\n"
        "                    # Mauvaises reponses : baisser leur score\n"
        "                    poids[lettre][b] -= vitesse * probas[b]\n"
        "\n"
        "    _historique_loss.append(loss_totale / nb)  # loss moyenne\n"
        "\n"
        "    if epoch % 10 == 0:\n"
        '        print(f"  Epoch {epoch:2d} | Loss moyenne : {loss_totale / nb:.3f}")\n'
        "\n"
        'print(f"  Epoch {epoch:2d} | Loss moyenne : {loss_totale / nb:.3f}")\n'
        "print()\n"
        'print("La loss baisse = le modele s\'ameliore !")\n'
        "\n"
        "# Courbe de loss animee\n"
        "afficher_evolution_loss(\n"
        '    _historique_loss, titre="Evolution de la loss pendant l\'entrainement"\n'
        ")"
    )
)

# CELL: MD — observation after training
cells.append(
    md(
        "**La loss a baisse ! Qu'est-ce que ca veut dire ?**\n"
        "\n"
        "Au debut, la loss etait haute (le modele devinait au hasard).\n"
        "A la fin, elle est beaucoup plus basse (le modele a appris les\n"
        "paires de lettres frequentes dans les noms de Pokemon).\n"
        "\n"
        "---"
    )
)

# CELL: Exercise 2 — compare speeds (code)
cells.append(
    code(
        "exercice(\n"
        "    2,\n"
        '    "Compare les vitesses",\n'
        '    "Change <code>vitesse_test</code> ci-dessous (essaie 0.01, 0.1, 0.5, 2.0).",\n'
        '    "Une vitesse trop grande fait exploser la loss, trop petite la fait stagner.",\n'
        ")\n"
        "\n"
        "# \u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557\n"
        "# \u2551  A TOI DE JOUER !                    \u2551\n"
        "# \u2560\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2563\n"
        "\n"
        "vitesse_test = 0.5  # <-- Change cette valeur ! Essaie 0.01, 0.1, 0.5, 2.0\n"
        "\n"
        "# \u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d\n"
        "\n"
        "# On repart de zero avec des poids aleatoires\n"
        "random.seed(123)\n"
        "poids_test = {}\n"
        "for a in alphabet:\n"
        "    poids_test[a] = {}\n"
        "    for b in alphabet:\n"
        "        poids_test[a][b] = random.uniform(-1, 1)\n"
        "\n"
        "# Mini-entrainement de 5 epochs avec cette vitesse\n"
        "for epoch in range(5):\n"
        "    loss_t = 0\n"
        "    nb_t = 0\n"
        "    for pokemon in pokemons:\n"
        '        mot = "." + pokemon + "."\n'
        "        for i in range(len(mot) - 1):\n"
        "            probas_t = calculer_probas(poids_test, mot[i])\n"
        "            loss_t += -math.log(probas_t[mot[i + 1]] + 1e-10)\n"
        "            nb_t += 1\n"
        "            for b in alphabet:\n"
        "                if b == mot[i + 1]:\n"
        "                    poids_test[mot[i]][b] += vitesse_test * (1 - probas_t[b])\n"
        "                else:\n"
        "                    poids_test[mot[i]][b] -= vitesse_test * probas_t[b]\n"
        '    print(f"  Epoch {epoch} | vitesse={vitesse_test} | Loss : {loss_t / nb_t:.3f}")\n'
        "\n"
        "verifier(\n"
        "    2,\n"
        "    vitesse_test != 0.5,\n"
        '    f"Bien ! Tu as teste la vitesse {vitesse_test}.",\n'
        '    "Change vitesse_test pour une autre valeur, par exemple 0.01 ou 2.0.",\n'
        ")"
    )
)

# CELL: MD — what the model learned
cells.append(
    md(
        "---\n"
        "## Que sait le modele maintenant ?\n"
        "\n"
        "Voyons si l'entrainement a porte ses fruits :"
    )
)

# CELL: Analysis (code)
cells.append(
    code(
        "# Apres entrainement, quelles lettres commencent les noms ?\n"
        'p = calculer_probas(poids, ".")\n'
        "lettres_debut = sorted(p.items(), key=lambda x: -x[1])[:5]\n"
        'print("Apres entrainement, les Pokemon commencent par :")\n'
        "for lettre, prob in lettres_debut:\n"
        "    print(f\"  '{lettre}' : {prob:.1%}\")\n"
        "print()\n"
        'print("C\'est plus logique ! (c, m, g, e, r sont des debuts courants)")'
    )
)

# CELL: MD — generation
cells.append(
    md(
        "### Generons des noms de Pokemon !\n"
        "\n"
        "Le modele peut maintenant inventer des noms en se basant\n"
        "sur ce qu'il a appris :"
    )
)

# CELL: Generation function + demo (code)
cells.append(
    code(
        "def generer(poids, n=10):\n"
        '    """Genere n noms de Pokemon avec le modele entraine."""\n'
        "    resultats = []\n"
        "    for _ in range(n):\n"
        '        pokemon = ""\n'
        '        lettre = "."\n'
        "        for _ in range(20):  # max 20 lettres\n"
        "            p = calculer_probas(poids, lettre)\n"
        "            choix = list(p.keys())    # lettres possibles\n"
        "            probs = list(p.values())  # leurs probabilites\n"
        "            lettre = random.choices(choix, weights=probs, k=1)[0]\n"
        '            if lettre == ".":  # fin du nom\n'
        "                break\n"
        "            pokemon += lettre\n"
        "        if pokemon:\n"
        "            resultats.append(pokemon.capitalize())\n"
        "    return resultats\n"
        "\n"
        "\n"
        'print("Noms de Pokemon inventes apres entrainement :")\n'
        "for p in generer(poids, 10):\n"
        '    print(f"  {p}")'
    )
)

# CELL: Coup de pouce (markdown — NC-01)
cells.append(
    md(
        "> **Coup de pouce** (si tu es bloque)\n"
        ">\n"
        "> Rappel : `generer(poids, 50)` genere 50 noms.\n"
        "> Change juste le nombre dans les parentheses !"
    )
)

# CELL: Exercise 3 — generate (code)
cells.append(
    code(
        "exercice(\n"
        "    3,\n"
        '    "Genere des Pokemon",\n'
        '    "Change <code>nombre</code> ci-dessous (essaie 50).",\n'
        '    "Certains noms vont ressembler a de vrais Pokemon !",\n'
        ")\n"
        "\n"
        "# \u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557\n"
        "# \u2551  A TOI DE JOUER !                    \u2551\n"
        "# \u2560\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2563\n"
        "\n"
        "nombre = 10  # <-- Mets 50 ici !\n"
        "\n"
        "# \u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d\n"
        "\n"
        'print(f"Generation de {nombre} Pokemon :")\n'
        "print()\n"
        "for i, nom in enumerate(generer(poids, nombre)):\n"
        '    print(f"  {i + 1}. {nom}")\n'
        "\n"
        "verifier(\n"
        "    3,\n"
        "    nombre != 10,\n"
        '    f"Genial ! Tu as genere {nombre} Pokemon.",\n'
        '    "Change nombre pour une autre valeur, par exemple 50.",\n'
        ")"
    )
)

# CELL: MD — comparison with lesson 1
cells.append(
    md(
        "**Compare avec la lecon 1 : les noms sont-ils meilleurs ?**\n"
        "\n"
        "Dans la lecon 1, on comptait simplement les paires. Ici, le modele\n"
        "a **appris** par lui-meme les meilleures probabilites en reduisant la loss.\n"
        "Le resultat est similaire, mais la methode est celle de toutes les IA modernes !\n"
        "\n"
        "---"
    )
)

# CELL: Defi (markdown — NC-09)
cells.append(
    md(
        "> **Defi** (pour aller plus loin)\n"
        ">\n"
        "> Ecris un code qui entraine avec `vitesse=0.001` puis `vitesse=0.5`.\n"
        "> Laquelle est meilleure ? Pourquoi ?"
    )
)

# CELL: Conclusion (markdown)
cells.append(
    md(
        "## Ce qu'on a appris\n"
        "\n"
        "- La **loss** mesure a quel point le modele se trompe\n"
        "- Les **poids** sont les nombres que le modele ajuste pour apprendre\n"
        "- L'**entrainement** = ajuster les poids pour reduire la loss, encore et encore\n"
        "- Meme un modele simple s'ameliore avec l'entrainement !\n"
        "\n"
        "### Limite\n"
        "\n"
        "Notre modele ne regarde encore que **1 lettre en arriere**.\n"
        "Dans la prochaine lecon, on va lui donner une **memoire** pour qu'il\n"
        "se souvienne de plusieurs lettres a la fois.\n"
        "\n"
        "---\n"
        "*Prochaine lecon : [03 - La memoire du modele](03_la_memoire_du_modele.ipynb)*"
    )
)

# CELL: Sources (markdown)
cells.append(
    md(
        "---\n"
        "\n"
        "### Sources (ISO 42001)\n"
        "\n"
        "- **Cross-entropy loss et descente de gradient** : [microgpt.py](https://gist.github.com/karpathy/8627fe009c40f57531cb18360106ce95) \\u2014 Andrej Karpathy, lignes implementant le backward pass\n"
        '- **Analogie du gradient comme correction** : [Video "Let\'s build GPT"](https://www.youtube.com/watch?v=kCc8FmEb1nY) \\u2014 Andrej Karpathy (2023)\n'
        "- **Visualisation de la descente de gradient** : [3Blue1Brown - Gradient descent](https://www.youtube.com/watch?v=IHZwWFHWa-w) \\u2014 Grant Sanderson\n"
        "- **Dataset Pokemon** : (c) Nintendo / Creatures Inc. / GAME FREAK inc., usage educatif. Source : [PokeAPI](https://pokeapi.co/)"
    )
)

nb["cells"] = cells
with open("notebooks/02_apprendre_des_erreurs.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"NB02 rebuilt: {len(cells)} cells (was 14)")
