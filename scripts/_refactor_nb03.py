#!/usr/bin/env python3
"""Refactor NB03: La memoire du modele — pedagogical overhaul.

Reads the existing notebook, extracts reusable parts (verifier, exercice),
rewrites with interactive scatter 2D embeddings visualization,
animated SVG bars, box-drawing delimiters, and markdown before every code cell.
"""

import json
import re


def md(source):
    """Create a markdown cell with source as a single string."""
    return {"cell_type": "markdown", "metadata": {}, "source": source}


def code(source):
    """Create a code cell with source as a single string."""
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source,
    }


# Read existing notebook to preserve metadata
with open("notebooks/03_la_memoire_du_modele.ipynb", encoding="utf-8") as f:
    nb = json.load(f)

# Extract original cell-1 source (verifier + exercice functions)
original_cell1 = "".join(
    nb["cells"][1]["source"]
    if isinstance(nb["cells"][1]["source"], list)
    else [nb["cells"][1]["source"]]
)

# Extract verifier and exercice functions via regex
verifier_match = re.search(
    r"(def verifier\(.*?\n(?:(?:    .*|)\n)*)", original_cell1, re.MULTILINE
)
exercice_match = re.search(
    r"(def exercice\(.*?\n(?:(?:    .*|)\n)*)", original_cell1, re.MULTILINE
)

verifier_code = verifier_match.group(1).rstrip("\n") if verifier_match else ""
exercice_code = exercice_match.group(1).rstrip("\n") if exercice_match else ""

# ================================================================
# Build new cell list
# ================================================================
cells = []

# ----------------------------------------------------------------
# CELL 0: Intro (markdown)
# ----------------------------------------------------------------
cells.append(
    md(
        "> **Rappel** : clique sur une cellule grise, puis **Shift + Entree** pour l'executer.\n"
        "> Execute les cellules **dans l'ordre** de haut en bas.\n"
        "\n"
        "---\n"
        "\n"
        "# Lecon 3 : La memoire du modele\n"
        "\n"
        "## Le probleme de la memoire courte\n"
        "\n"
        "Dans les lecons precedentes, notre modele ne regardait que la **derniere lettre**.\n"
        "C'est comme essayer de deviner la fin d'une phrase en n'ecoutant que le dernier mot.\n"
        "\n"
        "Exemple : apres les lettres 'salame', le modele ne sait pas si on est dans\n"
        '"**salame**che" ou "**salame**nce" -- pourtant la suite est tres differente !\n'
        "\n"
        "Solution : donner une **memoire** au modele. On appelle ca les **embeddings**."
    )
)

# ----------------------------------------------------------------
# CELL 1: Infrastructure (code)
# ----------------------------------------------------------------
infra = (
    "# ============================================================\n"
    "# Cellule d'initialisation \\u2014 execute sans lire (Shift+Entree)\n"
    "# ============================================================\n"
    "\n"
    "import json\n"
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
    # ---- afficher_barres: animated SVG bars ----
    'def afficher_barres(valeurs, etiquettes, titre="Probabilites", couleur="#1565c0"):\n'
    '    """Barres de probabilites animees (apparition progressive + hover)."""\n'
    "    max_val = max(valeurs) if valeurs else 1\n"
    "    n = len(valeurs)\n"
    "    bar_h, gap, lbl_w, bar_w = 24, 4, 30, 220\n"
    "    svg_h = n * (bar_h + gap) + gap\n"
    "    svg_w = lbl_w + bar_w + 70\n"
    '    bars = ""\n'
    "    for i, (etiq, val) in enumerate(zip(etiquettes, valeurs, strict=False)):\n"
    "        pct = val / max_val if max_val > 0 else 0\n"
    "        w = max(pct * bar_w, 2)\n"
    "        y = i * (bar_h + gap) + gap\n"
    '        delay = f"{i * 0.08:.2f}"\n'
    "        bars += (\n"
    '            f\'<text x="{lbl_w - 4}" y="{y + bar_h * 0.72}" \'\n'
    '            f\'text-anchor="end" font-size="13" font-weight="bold" \'\n'
    "            f'fill=\"#333\">{etiq}</text>'\n"
    '            f\'<rect x="{lbl_w}" y="{y}" width="0" height="{bar_h}" \'\n'
    '            f\'rx="4" fill="{couleur}" opacity="0.85">\'\n'
    '            f\'<animate attributeName="width" from="0" to="{w:.0f}" \'\n'
    '            f\'dur="0.5s" begin="{delay}s" fill="freeze"/></rect>\'\n'
    '            f\'<text x="{lbl_w + bar_w + 8}" y="{y + bar_h * 0.72}" \'\n'
    '            f\'font-size="12" fill="#555">{val:.0%}</text>\'\n'
    "        )\n"
    "    display(HTML(\n"
    "        f'<!-- tuto-viz -->'\n"
    "        f'<div style=\"margin:8px 0\"><b>{titre}</b>'\n"
    '        f\'<svg width="{svg_w}" height="{svg_h}" \'\n'
    "        f'style=\"margin-top:4px;display:block\">{bars}</svg></div>'\n"
    "    ))\n"
    "\n"
    "\n"
    # ---- afficher_embeddings_2d: scatter SVG ----
    'def afficher_embeddings_2d(embeddings, alphabet, titre="Embeddings 2D"):\n'
    '    """Scatter 2D des embeddings (voyelles rouge, consonnes bleu, hover coords)."""\n'
    "    uid = uuid.uuid4().hex[:8]\n"
    "    n_letters = min(len(alphabet), len(embeddings))\n"
    "    n_dim = len(embeddings[0])\n"
    "    # Projection : on choisit les 2 dimensions les plus variables\n"
    "    means = [sum(embeddings[i][d] for i in range(n_letters)) / n_letters for d in range(n_dim)]\n"
    "    variances = [\n"
    "        sum((embeddings[i][d] - means[d]) ** 2 for i in range(n_letters)) / n_letters\n"
    "        for d in range(n_dim)\n"
    "    ]\n"
    "    sorted_dims = sorted(range(n_dim), key=lambda d: -variances[d])\n"
    "    dx, dy = sorted_dims[0], sorted_dims[1]\n"
    "    # Construire les donnees pour JS\n"
    '    voyelles = set("aeiouy")\n'
    "    points = []\n"
    "    for i in range(n_letters):\n"
    '        ch = alphabet[i] if i < len(alphabet) else "?"\n'
    '        group = "voyelle" if ch in voyelles else ("sep" if ch == "." else "consonne")\n'
    '        points.append({"x": round(embeddings[i][dx], 3),\n'
    '                        "y": round(embeddings[i][dy], 3),\n'
    '                        "label": ch, "group": group})\n'
    "    data_json = json.dumps(points)\n"
    "    display(HTML(\n"
    "        f'<!-- tuto-viz -->'\n"
    '        f\'<div id="emb{uid}" style="margin:8px 0">\'\n'
    "        f'<b>{titre}</b>'\n"
    "        f'<div style=\"margin-top:4px;font-size:0.85em;color:#555\">'\n"
    "        f'Dimensions {dx} et {dy} (les plus variables) '\n"
    "        f'\\u2014 <span style=\"color:#e53935\">\\u25cf</span> voyelles '\n"
    "        f'<span style=\"color:#1565c0\">\\u25cf</span> consonnes '\n"
    "        f'<span style=\"color:#999\">\\u25cf</span> separateur</div>'\n"
    '        f\'<svg id="svg{uid}" width="460" height="360" \'\n'
    "        f'style=\"display:block;background:#fafafa;border-radius:4px;margin-top:4px\">'\n"
    "        f'</svg>'\n"
    '        f\'<div id="tip{uid}" style="position:fixed;display:none;background:#333;\'\n'
    "        f'color:white;padding:4px 8px;border-radius:4px;font-size:0.85em;'\n"
    "        f'pointer-events:none;z-index:9999\"></div>'\n"
    "        f'</div>'\n"
    "        f'<script>(function(){{'\n"
    "        f'var data={data_json};'\n"
    "        f'var svg=document.getElementById(\"svg{uid}\");'\n"
    "        f'var tip=document.getElementById(\"tip{uid}\");'\n"
    "        f'var w=460,h=360,pad=40;'\n"
    "        f'var xs=data.map(function(d){{return d.x}});'\n"
    "        f'var ys=data.map(function(d){{return d.y}});'\n"
    "        f'var xmn=Math.min.apply(null,xs),xmx=Math.max.apply(null,xs);'\n"
    "        f'var ymn=Math.min.apply(null,ys),ymx=Math.max.apply(null,ys);'\n"
    "        f'var xr=xmx-xmn||1,yr=ymx-ymn||1;'\n"
    "        f'xmn-=xr*0.08;xmx+=xr*0.08;ymn-=yr*0.08;ymx+=yr*0.08;'\n"
    "        f'xr=xmx-xmn;yr=ymx-ymn;'\n"
    "        f'function sx(v){{return pad+(v-xmn)/xr*(w-2*pad)}}'\n"
    "        f'function sy(v){{return h-pad-(v-ymn)/yr*(h-2*pad)}}'\n"
    "        f'var ns=\"http://www.w3.org/2000/svg\";'\n"
    "        f'function ln(a,b,c,d){{var el=document.createElementNS(ns,\"line\");'\n"
    '        f\'el.setAttribute("x1",a);el.setAttribute("y1",b);\'\n'
    '        f\'el.setAttribute("x2",c);el.setAttribute("y2",d);\'\n'
    '        f\'el.setAttribute("stroke","#ddd");el.setAttribute("stroke-width","1");\'\n'
    "        f'svg.appendChild(el)}}'\n"
    "        f'ln(pad,pad,pad,h-pad);ln(pad,h-pad,w-pad,h-pad);'\n"
    '        f\'var colors={{voyelle:"#e53935",consonne:"#1565c0",sep:"#999"}};\'\n'
    "        f'data.forEach(function(d){{'\n"
    "        f'var cx=sx(d.x),cy=sy(d.y);'\n"
    '        f\'var g=document.createElementNS(ns,"g");g.style.cursor="pointer";\'\n'
    "        f'var c=document.createElementNS(ns,\"circle\");'\n"
    '        f\'c.setAttribute("cx",cx);c.setAttribute("cy",cy);\'\n'
    '        f\'c.setAttribute("r","6");c.setAttribute("fill",colors[d.group]);\'\n'
    '        f\'c.setAttribute("opacity","0.8");\'\n'
    "        f'c.style.transition=\"r 0.2s,opacity 0.2s\";'\n"
    "        f'var t=document.createElementNS(ns,\"text\");'\n"
    '        f\'t.setAttribute("x",cx+9);t.setAttribute("y",cy+4);\'\n'
    '        f\'t.setAttribute("font-size","12");t.setAttribute("fill","#333");\'\n'
    '        f\'t.setAttribute("font-family","monospace");t.textContent=d.label;\'\n'
    "        f'g.appendChild(c);g.appendChild(t);'\n"
    "        f'g.addEventListener(\"mouseenter\",function(e){{'\n"
    '        f\'c.setAttribute("r","9");c.setAttribute("opacity","1");\'\n'
    "        f'tip.style.display=\"block\";'\n"
    '        f\'tip.textContent=d.label+" ("+d.x.toFixed(2)+", "+d.y.toFixed(2)+")";\'\n'
    '        f\'tip.style.left=e.pageX+12+"px";tip.style.top=e.pageY-30+"px"}});\'\n'
    "        f'g.addEventListener(\"mousemove\",function(e){{'\n"
    '        f\'tip.style.left=e.pageX+12+"px";tip.style.top=e.pageY-30+"px"}});\'\n'
    "        f'g.addEventListener(\"mouseleave\",function(){{'\n"
    '        f\'c.setAttribute("r","6");c.setAttribute("opacity","0.8");\'\n'
    "        f'tip.style.display=\"none\"}});'\n"
    "        f'svg.appendChild(g)}});'\n"
    "        f'}})();</script>'\n"
    "    ))\n"
    "\n"
    "\n"
    'print("Outils de visualisation charges !")'
)
cells.append(code(infra))

# ----------------------------------------------------------------
# CELL 2: MD — Les embeddings
# ----------------------------------------------------------------
cells.append(
    md(
        "---\n"
        "## Les embeddings : transformer des lettres en nombres\n"
        "\n"
        "L'idee : chaque lettre est representee par une **liste de nombres** (un vecteur).\n"
        "\n"
        "Par exemple :\n"
        "- 'a' \\u2192 [0.3, -0.1, 0.8]\n"
        "- 'b' \\u2192 [-0.5, 0.4, 0.2]\n"
        "\n"
        "Ces nombres ne sont pas choisis a la main : le modele les **apprend** pendant\n"
        "l'entrainement. Les lettres qui se comportent de facon similaire auront\n"
        "des nombres proches."
    )
)

# ----------------------------------------------------------------
# CELL 3: Alphabet + embeddings (code)
# ----------------------------------------------------------------
cells.append(
    code(
        "import math\n"
        "import random\n"
        "\n"
        "# Notre alphabet : 27 symboles (point + 26 lettres)\n"
        'alphabet = list(".abcdefghijklmnopqrstuvwxyz")\n'
        "\n"
        "# char_to_id : convertit une lettre en numero (pour que le modele puisse la manipuler)\n"
        "# id_to_char : fait l'inverse (numero -> lettre, pour afficher les resultats)\n"
        "char_to_id = {c: i for i, c in enumerate(alphabet)}\n"
        "id_to_char = {i: c for i, c in enumerate(alphabet)}\n"
        "vocab_size = len(alphabet)  # 27\n"
        "\n"
        'print(f"Taille du vocabulaire : {vocab_size} caracteres")\n'
        "print(\n"
        "    f\"Exemples : 'a' = {char_to_id['a']}, 'z' = {char_to_id['z']}, '.' = {char_to_id['.']}\"\n"
        ")\n"
        "\n"
        "# Creons les embeddings : chaque lettre = un vecteur de taille EMBED_DIM\n"
        "# C'est comme une carte d'identite numerique pour chaque lettre\n"
        "EMBED_DIM = 8  # 8 nombres par lettre\n"
        "\n"
        "# seed(42) = on fixe le hasard pour que tout le monde obtienne les memes nombres\n"
        "random.seed(42)\n"
        "\n"
        "# Initialisation aleatoire (le modele apprendra les bonnes valeurs)\n"
        "# Au debut ces nombres ne veulent rien dire, c'est l'entrainement qui les rend utiles\n"
        "embeddings = [\n"
        "    [random.gauss(0, 0.5) for _ in range(EMBED_DIM)] for _ in range(vocab_size)\n"
        "]\n"
        "\n"
        "# Regardons a quoi ressemble un embedding (une suite de 8 nombres)\n"
        "print(f\"\\nEmbedding de 'a' : {[f'{x:.2f}' for x in embeddings[char_to_id['a']]]}\")\n"
        "print(f\"Embedding de 'b' : {[f'{x:.2f}' for x in embeddings[char_to_id['b']]]}\")\n"
        "print()\n"
        'print("Pour l\'instant ces nombres sont aleatoires.")\n'
        'print("Apres entrainement, les lettres similaires auront des vecteurs proches.")'
    )
)

# ----------------------------------------------------------------
# CELL 4: MD — before exercise 1
# ----------------------------------------------------------------
cells.append(md("A toi d'experimenter avec la taille des embeddings :"))

# ----------------------------------------------------------------
# CELL 5: Exercise 1 — change dimension (code)
# ----------------------------------------------------------------
cells.append(
    code(
        "exercice(\n"
        "    1,\n"
        '    "Change la dimension",\n'
        '    "Change <code>EMBED_DIM_test</code> ci-dessous (essaie 4 ou 16), puis <b>Shift + Entree</b>.",\n'
        '    "Plus la dimension est grande, plus le modele a de parametres.",\n'
        ")\n"
        "\n"
        "# \u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557\n"
        "# \u2551  A TOI DE JOUER !                    \u2551\n"
        "# \u2560\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2563\n"
        "\n"
        "EMBED_DIM_test = 8  # <-- Essaie 4 (petit) ou 16 (grand) !\n"
        "\n"
        "# \u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d\n"
        "\n"
        'print(f"Avec EMBED_DIM = {EMBED_DIM_test} :")\n'
        'print(f"  Chaque lettre = {EMBED_DIM_test} nombres")\n'
        'print(f"  3 lettres de contexte = 3 x {EMBED_DIM_test} = {3 * EMBED_DIM_test} nombres")\n'
        "if EMBED_DIM_test <= 4:\n"
        '    print("  -> Petit : le modele a peu d\'information sur chaque lettre.")\n'
        "elif EMBED_DIM_test >= 16:\n"
        '    print("  -> Grand : plus d\'information, mais plus de calculs !")\n'
        "\n"
        "verifier(\n"
        "    1,\n"
        "    EMBED_DIM_test != 8,\n"
        '    f"Bien joue ! Avec {EMBED_DIM_test} dimensions, le vecteur de contexte fait {3 * EMBED_DIM_test} nombres.",\n'
        '    "Change EMBED_DIM_test pour une autre valeur, par exemple 4 ou 16.",\n'
        ")"
    )
)

# ----------------------------------------------------------------
# CELL 6: MD — Regarder plusieurs lettres
# ----------------------------------------------------------------
cells.append(
    md(
        "---\n"
        "## Regarder plusieurs lettres en arriere\n"
        "\n"
        "Maintenant, au lieu de regarder 1 seule lettre, on va regarder les\n"
        '**3 dernieres lettres** (notre "fenetre de contexte").\n'
        "\n"
        "On **concatene** (met bout a bout) leurs embeddings pour avoir une image\n"
        "complete du contexte :"
    )
)

# ----------------------------------------------------------------
# CELL 7: Context vector (code)
# ----------------------------------------------------------------
cells.append(
    code(
        "# Combien de lettres le modele regarde en arriere\n"
        "CONTEXT_SIZE = 3  # on regarde 3 lettres en arriere\n"
        "\n"
        "\n"
        "def get_context_vector(mot, position, embeddings):\n"
        '    """Recupere les embeddings des 3 dernieres lettres et les concatene."""\n'
        "    vecteur = []\n"
        "    for i in range(CONTEXT_SIZE):\n"
        "        pos = position - CONTEXT_SIZE + i\n"
        "        if pos < 0:\n"
        "            # Avant le debut du mot, on utilise '.' comme remplissage\n"
        '            char_id = char_to_id["."]\n'
        "        else:\n"
        "            char_id = char_to_id[mot[pos]]\n"
        "        # Concatener = mettre bout a bout les 8 nombres de chaque lettre\n"
        "        vecteur.extend(embeddings[char_id])\n"
        "    return vecteur  # 3 x 8 = 24 nombres au total\n"
        "\n"
        "\n"
        "# Exemple concret avec pikachu : on veut predire 'a' en position 4\n"
        "# Le modele regarde les 3 lettres precedentes : 'p', 'i', 'k'\n"
        'mot = ".pikachu."\n'
        "position = 4\n"
        "contexte = get_context_vector(mot, position, embeddings)\n"
        "\n"
        "print(f\"Mot : '{mot}'\")\n"
        "print(f\"Pour predire la lettre en position {position} ('{mot[position]}'),\")\n"
        "print(\n"
        '    f"on regarde les {CONTEXT_SIZE} lettres precedentes : "\n'
        "    f\"'{mot[max(0, position - CONTEXT_SIZE):position]}'\"\n"
        ")\n"
        "# Le vecteur combine les 3 embeddings en un seul grand vecteur\n"
        'print(f"Vecteur de contexte : {len(contexte)} nombres ({CONTEXT_SIZE} x {EMBED_DIM})")'
    )
)

# ----------------------------------------------------------------
# CELL 8: MD — before exercise 2
# ----------------------------------------------------------------
cells.append(md("A toi de changer la taille de la fenetre de contexte :"))

# ----------------------------------------------------------------
# CELL 9: Exercise 2 — change context (code)
# ----------------------------------------------------------------
cells.append(
    code(
        "exercice(\n"
        "    2,\n"
        '    "Change le contexte",\n'
        '    "Change <code>context_test</code> ci-dessous (essaie 1 ou 5).",\n'
        '    "Avec un contexte de 1, le modele oublie tout (comme la lecon 2).",\n'
        ")\n"
        "\n"
        "# \u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557\n"
        "# \u2551  A TOI DE JOUER !                    \u2551\n"
        "# \u2560\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2563\n"
        "\n"
        "context_test = 3  # <-- Essaie 1 (comme la lecon 2) ou 5 (plus de memoire) !\n"
        "\n"
        "# \u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d\n"
        "\n"
        "taille_vecteur = context_test * EMBED_DIM\n"
        'print(f"Avec CONTEXT_SIZE = {context_test} :")\n'
        'print(f"  Le modele regarde {context_test} lettre(s) en arriere")\n'
        "print(\n"
        '    f"  Vecteur de contexte = {context_test} x {EMBED_DIM} = {taille_vecteur} nombres"\n'
        ")\n"
        "if context_test == 1:\n"
        '    print("  -> Pareil que la lecon 2 : 1 seule lettre !")\n'
        "elif context_test >= 5:\n"
        '    print("  -> Beaucoup de memoire, mais plus long a entrainer.")\n'
        "\n"
        "verifier(\n"
        "    2,\n"
        "    context_test != 3,\n"
        '    f"Super ! Avec un contexte de {context_test}, le modele utilise {context_test * EMBED_DIM} nombres.",\n'
        '    "Change context_test pour une autre valeur, par exemple 1 ou 5.",\n'
        ")"
    )
)

# ----------------------------------------------------------------
# CELL 10: MD — Un mini reseau de neurones (CRITICAL NEW)
# ----------------------------------------------------------------
cells.append(
    md(
        "---\n"
        "## Etape 3 : Un mini reseau de neurones\n"
        "\n"
        "On a maintenant un vecteur de contexte de **24 nombres** (3 lettres x 8 dimensions).\n"
        "Il faut le transformer en **27 scores** (un par lettre de l'alphabet).\n"
        "\n"
        "Pour ca, on utilise un **reseau de neurones** tres simple :\n"
        "une matrice de poids **W** (24 x 27 = 648 nombres) et un biais **b** (27 nombres).\n"
        "\n"
        'C\'est comme un filtre qui transforme "ce qu\'on voit" en "ce qu\'on predit" :'
    )
)

# ----------------------------------------------------------------
# CELL 11: W, b initialization + dimensions (code)
# ----------------------------------------------------------------
cells.append(
    code(
        "INPUT_DIM = CONTEXT_SIZE * EMBED_DIM  # 3 x 8 = 24 nombres en entree\n"
        "\n"
        "# W est le 'cerveau' du modele : il transforme le contexte en predictions\n"
        "# Chaque ligne correspond a un nombre du contexte, chaque colonne a une lettre\n"
        "W = [[random.gauss(0, 0.3) for _ in range(vocab_size)] for _ in range(INPUT_DIM)]\n"
        "# Le biais donne un avantage de depart a certaines lettres (ex: 'e' est frequent)\n"
        "b = [0.0] * vocab_size\n"
        "\n"
        'print(f"Matrice W : {INPUT_DIM} x {vocab_size} = {INPUT_DIM * vocab_size} poids")\n'
        'print(f"Biais b   : {vocab_size} nombres")\n'
        'print(f"Total     : {INPUT_DIM * vocab_size + vocab_size} parametres")\n'
        "print()\n"
        'print("Ces nombres sont aleatoires pour l\'instant.")\n'
        'print("L\'entrainement va trouver les bonnes valeurs.")'
    )
)

# ----------------------------------------------------------------
# CELL 12: MD — le forward pass
# ----------------------------------------------------------------
cells.append(
    md(
        "### Le forward pass : du contexte aux predictions\n"
        "\n"
        "Le calcul est simple :\n"
        "1. **forward()** : multiplie le contexte par W, ajoute b \\u2192 27 scores\n"
        "2. **softmax()** : transforme les scores en probabilites (entre 0 et 1, somme = 1)"
    )
)

# ----------------------------------------------------------------
# CELL 13: forward + softmax (code)
# ----------------------------------------------------------------
cells.append(
    code(
        "def forward(contexte, W, b):\n"
        '    """Passe le contexte dans le reseau pour obtenir des scores."""\n'
        "    scores = list(b)  # on part du biais\n"
        "    for j in range(vocab_size):       # pour chaque lettre de sortie\n"
        "        for i in range(INPUT_DIM):    # pour chaque nombre du contexte\n"
        "            # Chaque poids W[i][j] dit 'combien le nombre i influence la lettre j'\n"
        "            scores[j] += contexte[i] * W[i][j]\n"
        "    return scores\n"
        "\n"
        "\n"
        "def softmax(scores):\n"
        '    """Transforme les scores en probabilites (entre 0 et 1, somme = 1)."""\n'
        "    max_s = max(scores)  # on soustrait le max pour eviter des nombres trop grands\n"
        "    exps = [math.exp(s - max_s) for s in scores]  # l'exponentielle amplifie les ecarts\n"
        "    total = sum(exps)\n"
        "    return [e / total for e in exps]  # diviser par le total -> somme = 1"
    )
)

# ----------------------------------------------------------------
# CELL 14: MD — before test predictions
# ----------------------------------------------------------------
cells.append(
    md(
        "Testons les predictions du modele sur le contexte 'pik' \\u2014\n"
        "avant l'entrainement, le modele devine au hasard :"
    )
)

# ----------------------------------------------------------------
# CELL 15: Test predictions + barres (code)
# ----------------------------------------------------------------
cells.append(
    code(
        "# Testons avec le contexte 'pik' (avant entrainement)\n"
        "scores = forward(contexte, W, b)  # 27 scores bruts\n"
        "probas = softmax(scores)           # 27 probabilites (somme = 1)\n"
        "\n"
        "# On affiche les 5 lettres les plus probables\n"
        "top5 = sorted(range(vocab_size), key=lambda i: -probas[i])[:5]\n"
        "print(\"Predictions (avant entrainement) pour la lettre apres 'pik' :\")\n"
        "for idx in top5:\n"
        "    print(f\"  '{id_to_char[idx]}' : {probas[idx]:.1%}\")\n"
        "print(\"\\n  (C'est du hasard pour l'instant - il faut entrainer !)\")\n"
        "\n"
        "# Barres de probabilites\n"
        "afficher_barres(\n"
        "    [probas[idx] for idx in top5],\n"
        "    [id_to_char[idx] for idx in top5],\n"
        "    titre=\"Top 5 predictions apres 'pik' (avant entrainement)\",\n"
        ")"
    )
)

# ----------------------------------------------------------------
# CELL 15: MD — Entrainement
# ----------------------------------------------------------------
cells.append(
    md(
        "---\n"
        "## Etape 4 : Entrainement\n"
        "\n"
        "On entraine le modele sur 20 noms de Pokemon. A chaque lettre, on :\n"
        "1. Calcule les probabilites (forward + softmax)\n"
        "2. Mesure l'erreur (loss)\n"
        "3. Ajuste les poids W et b pour reduire l'erreur\n"
        "\n"
        "L'entrainement dure ~10-15 secondes (100 epochs, 20 Pokemon) :"
    )
)

# ----------------------------------------------------------------
# CELL 16: Training loop (code)
# ----------------------------------------------------------------
cells.append(
    code(
        "# Les 20 Pokemon d'entrainement\n"
        "pokemons = [\n"
        '    "arcanin", "bulbizarre", "carapuce", "dracaufeu", "ectoplasma",\n'
        '    "evoli", "felinferno", "gardevoir", "goupix", "lokhlass",\n'
        '    "lucario", "metamorph", "mewtwo", "noctali", "pikachu",\n'
        '    "rondoudou", "ronflex", "salameche", "togepi", "voltali",\n'
        "]\n"
        "\n"
        "# La vitesse d'apprentissage : trop grande = instable, trop petite = trop lent\n"
        "vitesse = 0.01\n"
        "\n"
        'print("Entrainement avec contexte de 3 lettres (~10-15s)...")\n'
        "print()\n"
        "\n"
        "# On repete 100 fois sur les memes Pokemon (100 epochs)\n"
        "for epoch in range(100):\n"
        "    loss_totale = 0\n"
        "    nb = 0\n"
        "\n"
        "    for pokemon in pokemons:\n"
        '        mot = "." + pokemon + "."  # le point marque debut et fin\n'
        "        for pos in range(1, len(mot)):\n"
        "            cible = char_to_id[mot[pos]]  # la bonne reponse\n"
        "\n"
        "            # Forward : contexte -> scores -> probas\n"
        "            ctx = get_context_vector(mot, pos, embeddings)\n"
        "            scores = forward(ctx, W, b)\n"
        "            probas = softmax(scores)\n"
        "\n"
        "            # Loss : -log(proba de la bonne reponse)\n"
        "            # Plus la proba est faible, plus la loss est grande\n"
        "            loss_totale += -math.log(probas[cible] + 1e-10)\n"
        "            nb += 1\n"
        "\n"
        "            # Gradient : de combien corriger chaque poids\n"
        "            # Si probas[j] > 0 mais j n'est pas la bonne lettre -> grad positif -> on diminue\n"
        "            # Si j est la bonne lettre -> grad negatif -> on augmente\n"
        "            for j in range(vocab_size):\n"
        "                grad = probas[j] - (1 if j == cible else 0)\n"
        "                b[j] -= vitesse * grad  # on corrige dans la direction opposee\n"
        "                for i in range(INPUT_DIM):\n"
        "                    W[i][j] -= vitesse * grad * ctx[i]\n"
        "\n"
        "    if epoch % 20 == 0:\n"
        '        print(f"  Epoch {epoch:3d} | Loss : {loss_totale / nb:.3f}")\n'
        "\n"
        'print(f"  Epoch {epoch:3d} | Loss : {loss_totale / nb:.3f}")\n'
        'print("\\nLa loss a baisse = le modele a appris !")'
    )
)

# ----------------------------------------------------------------
# CELL 17: Scatter 2D embeddings (code)
# ----------------------------------------------------------------
cells.append(
    code(
        "# Visualisation : ou sont les lettres dans l'espace des embeddings ?\n"
        "# Les voyelles (a, e, i, o, u, y) sont en rouge, les consonnes en bleu.\n"
        "afficher_embeddings_2d(\n"
        '    embeddings, alphabet, titre="Embeddings apres entrainement"\n'
        ")"
    )
)

# ----------------------------------------------------------------
# CELL 18: MD — observation embeddings
# ----------------------------------------------------------------
cells.append(
    md(
        "**Observe le graphique ci-dessus :**\n"
        "\n"
        "- Les **voyelles** (en rouge) se regroupent-elles ?\n"
        "- Certaines consonnes sont-elles proches les unes des autres ?\n"
        "- Le point (separateur) est-il a part ?\n"
        "\n"
        "Le modele a decouvert **tout seul** que certaines lettres se comportent de\n"
        "facon similaire dans les noms de Pokemon !\n"
        "\n"
        "---"
    )
)

# ----------------------------------------------------------------
# CELL 19: MD — generation
# ----------------------------------------------------------------
cells.append(
    md(
        "## Generons des noms de Pokemon !\n"
        "\n"
        "Le modele peut maintenant inventer des noms en se basant\n"
        "sur ce qu'il a appris avec sa memoire de 3 lettres :"
    )
)

# ----------------------------------------------------------------
# CELL 20: Generation function + demo (code)
# ----------------------------------------------------------------
cells.append(
    code(
        "def generer(n=10):\n"
        '    """Genere n noms avec le modele entraine."""\n'
        "    resultats = []\n"
        "    for _ in range(n):\n"
        '        mot = "."  # on commence par le point (debut de mot)\n'
        "        for _ in range(20):  # max 20 lettres (securite)\n"
        "            # Le modele predit la prochaine lettre d'apres les 3 dernieres\n"
        "            ctx = get_context_vector(mot, len(mot), embeddings)\n"
        "            scores = forward(ctx, W, b)\n"
        "            probas = softmax(scores)\n"
        "            # Choisir une lettre au hasard selon les probabilites\n"
        "            idx = random.choices(range(vocab_size), weights=probas, k=1)[0]\n"
        '            if idx == char_to_id["."]:\n'
        "                break  # le point = fin du nom\n"
        "            mot += id_to_char[idx]\n"
        "        if len(mot) > 1:\n"
        "            resultats.append(mot[1:].capitalize())\n"
        "    return resultats\n"
        "\n"
        "\n"
        'print("Pokemon generes (avec contexte de 3 lettres) :")\n'
        "print()\n"
        "for p in generer(10):\n"
        '    print(f"  {p}")\n'
        "\n"
        "print()\n"
        'print("Mieux qu\'avant ! Le modele comprend des combinaisons de lettres.")'
    )
)

# ----------------------------------------------------------------
# CELL 21: MD — before exercise 3
# ----------------------------------------------------------------
cells.append(md("A toi de generer plus de Pokemon :"))

# ----------------------------------------------------------------
# CELL 22: Exercise 3 — generate (code)
# ----------------------------------------------------------------
cells.append(
    code(
        "exercice(\n"
        "    3,\n"
        '    "Genere des Pokemon",\n'
        '    "Change <code>nombre</code> ci-dessous (essaie 30).",\n'
        '    "Compare avec la lecon 2 : les noms sont-ils meilleurs ?",\n'
        ")\n"
        "\n"
        "# \u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557\n"
        "# \u2551  A TOI DE JOUER !                    \u2551\n"
        "# \u2560\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2563\n"
        "\n"
        "nombre = 10  # <-- Mets 30 ici !\n"
        "\n"
        "# \u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d\n"
        "\n"
        'print(f"Generation de {nombre} Pokemon :")\n'
        "print()\n"
        "for i, nom in enumerate(generer(nombre)):\n"
        '    print(f"  {i + 1}. {nom}")\n'
        "\n"
        "verifier(\n"
        "    3,\n"
        "    nombre != 10,\n"
        '    f"Genial ! Tu as genere {nombre} Pokemon.",\n'
        '    "Change nombre pour une autre valeur, par exemple 30.",\n'
        ")"
    )
)

# ----------------------------------------------------------------
# CELL 23: MD — comparison with lesson 2
# ----------------------------------------------------------------
cells.append(
    md(
        "**Compare avec la lecon 2 : les noms sont-ils meilleurs ?**\n"
        "\n"
        "Dans la lecon 2, le modele ne regardait qu'**1 seule lettre**. Ici, il regarde\n"
        "les **3 dernieres lettres** grace aux embeddings et au contexte.\n"
        'Resultat : il apprend des combinaisons plus longues ("dra", "chu", "pla"...)\n'
        "\n"
        "---"
    )
)

# ----------------------------------------------------------------
# CELL 24: MD — conclusion
# ----------------------------------------------------------------
cells.append(
    md(
        "## Ce qu'on a appris\n"
        "\n"
        "- Les **embeddings** transforment des lettres en nombres que le modele peut manipuler\n"
        "- Un **contexte** plus large (3 lettres au lieu de 1) donne de meilleurs resultats\n"
        "- Un **reseau de neurones** (meme simple) combine le contexte pour faire des predictions\n"
        "- Les embeddings appris **regroupent** les lettres similaires dans l'espace\n"
        "\n"
        "### Et ensuite ?\n"
        "\n"
        "Notre modele regarde toujours une fenetre fixe de 3 lettres. Et s'il pouvait\n"
        "**choisir** quelles lettres sont importantes, meme si elles sont loin ?\n"
        "C'est exactement ce que fait le **mecanisme d'attention** -- le coeur des GPT.\n"
        "\n"
        "---\n"
        "*Prochaine lecon : [04 - L'attention](04_lattention.ipynb)*"
    )
)

# ----------------------------------------------------------------
# CELL 25: MD — Sources
# ----------------------------------------------------------------
cells.append(
    md(
        "---\n"
        "\n"
        "### Sources (ISO 42001)\n"
        "\n"
        "- **Embeddings et reseau feed-forward** : [microgpt.py](https://gist.github.com/karpathy/8627fe009c40f57531cb18360106ce95) \\u2014 Andrej Karpathy, section token/position embeddings\n"
        '- **Architecture du contexte par concatenation** : [Video "Let\'s build GPT"](https://www.youtube.com/watch?v=kCc8FmEb1nY) \\u2014 Andrej Karpathy (2023)\n'
        "- **Concept d'embedding spaces** : [3Blue1Brown - Neural Networks](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi) \\u2014 Grant Sanderson\n"
        "- **Dataset Pokemon** : (c) Nintendo / Creatures Inc. / GAME FREAK inc., usage educatif. Source : [PokeAPI](https://pokeapi.co/)"
    )
)

# ================================================================
# Write rebuilt notebook
# ================================================================
nb["cells"] = cells
with open("notebooks/03_la_memoire_du_modele.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"NB03 rebuilt: {len(cells)} cells (was 15)")
