#!/usr/bin/env python3
"""Refactor NB05: Mon premier LLM — pedagogical overhaul.

Splits cell 3 (config) and cell 7 (forward), adds slider temperature,
BertViz attention, animated bars, animation generation, box-drawing exercises.
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
with open("notebooks/05_mon_premier_llm.ipynb", encoding="utf-8") as f:
    nb = json.load(f)

# Extract original cell-1 source (verifier + exercice + afficher_architecture)
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
architecture_match = re.search(
    r"(def afficher_architecture\(.*?\n(?:(?:    .*|)\n)*)",
    original_cell1,
    re.MULTILINE,
)

verifier_code = verifier_match.group(1).rstrip("\n") if verifier_match else ""
exercice_code = exercice_match.group(1).rstrip("\n") if exercice_match else ""
architecture_code = (
    architecture_match.group(1).rstrip("\n") if architecture_match else ""
)

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
        "# Lecon 5 : Mon premier LLM\n"
        "\n"
        "## On assemble tout !\n"
        "\n"
        "Tu as appris :\n"
        "1. **Predire la suite** avec des probabilites\n"
        "2. **Apprendre de ses erreurs** avec la loss et le gradient\n"
        "3. **Les embeddings** pour donner une memoire au modele\n"
        "4. **L'attention** pour regarder les lettres importantes\n"
        "\n"
        "Maintenant, on met tout ensemble pour creer un **vrai mini-LLM**\n"
        "qui genere des noms de Pokemon inventes !"
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
    # ---- afficher_attention: BertViz-style SVG ----
    'def afficher_attention(poids, positions, titre="Poids d\'attention"):\n'
    '    """Attention BertViz-style : lignes entre tokens, opacite = poids."""\n'
    "    n = len(positions)\n"
    "    col_w, row_h = 60, 36\n"
    "    svg_w = col_w * n + 40\n"
    "    svg_h = row_h * 3 + 20\n"
    '    elems = ""\n'
    "    for i, c in enumerate(positions):\n"
    "        x = 20 + i * col_w + col_w // 2\n"
    "        elems += (\n"
    '            f\'<text x="{x}" y="20" text-anchor="middle" \'\n'
    '            f\'font-size="16" font-weight="bold" fill="#333">{c}</text>\'\n'
    "        )\n"
    "        w = poids[i]\n"
    "        opacity = max(w, 0.05)\n"
    "        stroke_w = 1 + w * 8\n"
    "        elems += (\n"
    '            f\'<line x1="{x}" y1="28" x2="{svg_w // 2}" y2="{svg_h - 30}" \'\n'
    '            f\'stroke="#1565c0" stroke-width="{stroke_w:.1f}" \'\n'
    '            f\'stroke-opacity="{opacity:.2f}" stroke-linecap="round"/>\'\n'
    "        )\n"
    "        elems += (\n"
    '            f\'<text x="{x}" y="42" text-anchor="middle" \'\n'
    '            f\'font-size="11" fill="#555">{w:.0%}</text>\'\n'
    "        )\n"
    "    elems += (\n"
    '        f\'<text x="{svg_w // 2}" y="{svg_h - 10}" text-anchor="middle" \'\n'
    '        f\'font-size="14" font-weight="bold" fill="#1565c0">query</text>\'\n'
    "    )\n"
    "    display(HTML(\n"
    "        f'<!-- tuto-viz -->'\n"
    "        f'<div style=\"margin:8px 0\"><b>{titre}</b>'\n"
    '        f\'<svg width="{svg_w}" height="{svg_h}" \'\n'
    "        f'style=\"margin-top:4px;display:block\">{elems}</svg></div>'\n"
    "    ))\n"
    "\n"
    "\n"
    # ---- afficher_architecture: kept from original ----
     + architecture_code + "\n"
    "\n"
    "\n"
    # ---- afficher_temperature: slider + real-time bars ----
    'def afficher_temperature(probas, labels, titre="Effet de la temperature"):\n'
    '    """Slider temperature interactif avec barres de probas en temps reel."""\n'
    "    import math as _m\n"
    "    uid = uuid.uuid4().hex[:8]\n"
    "    log_p = [_m.log(p + 1e-10) for p in probas]\n"
    '    data_json = json.dumps({"logp": log_p, "labels": labels})\n'
    "    n = len(labels)\n"
    "    bar_h, gap, lbl_w, bar_w = 22, 3, 30, 200\n"
    "    svg_h = n * (bar_h + gap) + gap + 4\n"
    "    svg_w = lbl_w + bar_w + 70\n"
    "    display(HTML(\n"
    "        f'<!-- tuto-viz -->'\n"
    '        f\'<div id="tp{uid}" style="margin:8px 0"><b>{titre}</b>\'\n'
    "        f'<div style=\"margin-top:6px\">'\n"
    '        f\'Temperature : <input type="range" id="sl{uid}" \'\n'
    '        f\'min="0.1" max="3.0" step="0.1" value="1.0" \'\n'
    "        f'style=\"width:200px;vertical-align:middle\"> '\n"
    "        f'<b id=\"tv{uid}\">1.0</b></div>'\n"
    '        f\'<svg id="sv{uid}" width="{svg_w}" height="{svg_h}" \'\n'
    "        f'style=\"margin-top:4px;display:block\"></svg>'\n"
    "        f'<div style=\"color:#555;font-size:0.85em;margin-top:4px\">'\n"
    "        f'Deplace le curseur pour voir l\\'effet de la temperature</div></div>'\n"
    "        f'<script>(function(){{'\n"
    "        f'var d={data_json};'\n"
    "        f'var sl=document.getElementById(\"sl{uid}\");'\n"
    "        f'var tv=document.getElementById(\"tv{uid}\");'\n"
    "        f'var svg=document.getElementById(\"sv{uid}\");'\n"
    "        f'var ns=\"http://www.w3.org/2000/svg\";'\n"
    "        f'function sm(lp,t){{'\n"
    "        f'var mx=Math.max.apply(null,lp.map(function(v){{return v/t}}));'\n"
    "        f'var e=lp.map(function(v){{return Math.exp(v/t-mx)}});'\n"
    "        f'var s=e.reduce(function(a,b){{return a+b}},0);'\n"
    "        f'return e.map(function(v){{return v/s}})}}'\n"
    "        f'function draw(t){{'\n"
    "        f'while(svg.firstChild)svg.removeChild(svg.firstChild);'\n"
    "        f'var p=sm(d.logp,t);'\n"
    "        f'var mx=Math.max.apply(null,p);'\n"
    "        f'for(var i=0;i<d.labels.length;i++){{'\n"
    "        f'var y=i*{bar_h + gap}+{gap};'\n"
    "        f'var w=Math.max(p[i]/mx*{bar_w},2);'\n"
    "        f'var tl=document.createElementNS(ns,\"text\");'\n"
    '        f\'tl.setAttribute("x",{lbl_w - 4});tl.setAttribute("y",y+{bar_h}*0.72);\'\n'
    '        f\'tl.setAttribute("text-anchor","end");tl.setAttribute("font-size","13");\'\n'
    '        f\'tl.setAttribute("font-weight","bold");tl.setAttribute("fill","#333");\'\n'
    "        f'tl.textContent=d.labels[i];svg.appendChild(tl);'\n"
    "        f'var r=document.createElementNS(ns,\"rect\");'\n"
    '        f\'r.setAttribute("x",{lbl_w});r.setAttribute("y",y);\'\n'
    '        f\'r.setAttribute("width",w);r.setAttribute("height",{bar_h});\'\n'
    '        f\'r.setAttribute("rx","4");r.setAttribute("fill","#1565c0");\'\n'
    '        f\'r.setAttribute("opacity","0.85");svg.appendChild(r);\'\n'
    "        f'var tv2=document.createElementNS(ns,\"text\");'\n"
    '        f\'tv2.setAttribute("x",{lbl_w + bar_w + 8});tv2.setAttribute("y",y+{bar_h}*0.72);\'\n'
    '        f\'tv2.setAttribute("font-size","12");tv2.setAttribute("fill","#555");\'\n'
    "        f'tv2.textContent=(p[i]*100).toFixed(1)+\"%\";svg.appendChild(tv2)}}}}'\n"
    "        f'sl.addEventListener(\"input\",function(){{'\n"
    "        f'var t=parseFloat(sl.value);tv.textContent=t.toFixed(1);draw(t)}});'\n"
    "        f'draw(1.0)'\n"
    "        f'}})();</script>'\n"
    "    ))\n"
    "\n"
    "\n"
    # ---- afficher_generation: letter by letter animation ----
    "def afficher_generation(mot, delai_ms=300):\n"
    '    """Anime l\'apparition d\'un mot lettre par lettre."""\n'
    "    uid = uuid.uuid4().hex[:8]\n"
    "    lettres_js = json.dumps(list(mot))\n"
    "    display(HTML(\n"
    "        f'<!-- tuto-viz -->'\n"
    "        f'<div style=\"margin:8px 0;font-family:monospace;font-size:1.3em\">'\n"
    '        f\'<span id="g{uid}" style="letter-spacing:2px"></span>\'\n'
    '        f\'<span id="c{uid}" style="animation:bk{uid} 0.7s infinite">|</span></div>\'\n'
    "        f'<style>@keyframes bk{uid}{{0%,100%{{opacity:1}}50%{{opacity:0}}}}</style>'\n"
    "        f'<script>(function(){{'\n"
    "        f'var L={lettres_js},i=0,'\n"
    "        f'el=document.getElementById(\"g{uid}\"),'\n"
    "        f'cur=document.getElementById(\"c{uid}\");'\n"
    "        f'var iv=setInterval(function(){{'\n"
    "        f'if(i>=L.length){{clearInterval(iv);cur.style.display=\"none\";return}}'\n"
    "        f'var s=document.createElement(\"span\");'\n"
    "        f's.textContent=L[i];'\n"
    "        f's.style.cssText=\"opacity:0;transition:opacity 0.3s\";'\n"
    "        f'el.appendChild(s);'\n"
    "        f'setTimeout(function(){{s.style.opacity=\"1\"}},30);'\n"
    "        f'i++}},{delai_ms})'\n"
    "        f'}})();</script>'\n"
    "    ))\n"
    "\n"
    "\n"
    'print("Outils de visualisation charges !")'
)
cells.append(code(infra))

# ----------------------------------------------------------------
# CELL 2: MD — Architecture
# ----------------------------------------------------------------
cells.append(
    md(
        "---\n"
        "## Architecture de notre LLM\n"
        "\n"
        "Notre mini-LLM a la **meme architecture** que GPT-2, GPT-3 et GPT-4.\n"
        "Seule la taille change. Voyons les pieces :"
    )
)

# ----------------------------------------------------------------
# CELL 3: Config + param count (code)
# ----------------------------------------------------------------
cells.append(
    code(
        "import math\n"
        "import random\n"
        "\n"
        "random.seed(42)  # pour que tout le monde ait le meme resultat\n"
        "\n"
        "# --- Vocabulaire (meme que lecon 3) ---\n"
        'VOCAB = list(".abcdefghijklmnopqrstuvwxyz")\n'
        "VOCAB_SIZE = len(VOCAB)  # 26 lettres + le point (debut/fin)\n"
        "char_to_id = {c: i for i, c in enumerate(VOCAB)}\n"
        "id_to_char = {i: c for i, c in enumerate(VOCAB)}\n"
        "\n"
        "# --- Configuration du modele ---\n"
        "# Chaque lettre sera representee par 16 nombres (sa 'fiche d'identite')\n"
        "EMBED_DIM = 16   # taille des embeddings\n"
        "CONTEXT = 8      # le modele regarde 8 lettres en arriere (max)\n"
        "NUM_HEADS = 1    # 1 tete d'attention (pour simplifier)\n"
        "HEAD_DIM = EMBED_DIM // NUM_HEADS  # = 16\n"
        "HIDDEN_DIM = 32  # taille du reseau de neurones interne\n"
        "\n"
        "# Comptons combien de nombres le modele doit apprendre\n"
        "nb_params = (\n"
        "    VOCAB_SIZE * EMBED_DIM       # token embeddings       = 432\n"
        "    + CONTEXT * EMBED_DIM        # position embeddings    = 128\n"
        "    + 3 * EMBED_DIM * EMBED_DIM  # Q, K, V matrices      = 768\n"
        "    + EMBED_DIM * HIDDEN_DIM     # MLP couche 1 (poids)  = 512\n"
        "    + HIDDEN_DIM                 # MLP couche 1 (biais)  = 32\n"
        "    + HIDDEN_DIM * EMBED_DIM     # MLP couche 2 (poids)  = 512\n"
        "    + EMBED_DIM                  # MLP couche 2 (biais)  = 16\n"
        "    + EMBED_DIM * VOCAB_SIZE     # couche de sortie      = 432\n"
        ")\n"
        "\n"
        'print("Configuration du mini-LLM :")\n'
        'print(f"  Vocabulaire : {VOCAB_SIZE} caracteres")\n'
        'print(f"  Dimension embeddings : {EMBED_DIM}")\n'
        'print(f"  Contexte max : {CONTEXT} lettres")\n'
        'print(f"  Taille MLP : {HIDDEN_DIM}")\n'
        'print(f"  Nombre de parametres : {nb_params:,}")\n'
        "print()\n"
        'print(f"  (GPT-4 en a ~1,800,000,000,000 -- {nb_params / 1.8e12 * 100:.10f}% de GPT-4)")'
    )
)

# ----------------------------------------------------------------
# CELL 4: Architecture diagram (code)
# ----------------------------------------------------------------
cells.append(code("# Schema de l'architecture\nafficher_architecture()"))

# ----------------------------------------------------------------
# CELL 5: MD — before exercise 1
# ----------------------------------------------------------------
cells.append(md("A toi de changer la taille du modele :"))

# ----------------------------------------------------------------
# CELL 6: Exercise 1 — change EMBED_DIM (code)
# ----------------------------------------------------------------
cells.append(
    code(
        "exercice(\n"
        "    1,\n"
        '    "Change la taille du modele",\n'
        '    "Change <code>EMBED_DIM_test</code> ci-dessous (essaie 8 ou 32), puis <b>Shift + Entree</b>.",\n'
        '    "Doubler EMBED_DIM quadruple presque le nombre de parametres !",\n'
        ")\n"
        "\n"
        "# \u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557\n"
        "# \u2551  A TOI DE JOUER !                    \u2551\n"
        "# \u2560\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2563\n"
        "\n"
        "EMBED_DIM_test = 16  # <-- Essaie 8 (petit) ou 32 (grand) !\n"
        "\n"
        "# \u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d\n"
        "\n"
        "HIDDEN_DIM_test = EMBED_DIM_test * 2\n"
        "nb_params_test = (\n"
        "    VOCAB_SIZE * EMBED_DIM_test\n"
        "    + CONTEXT * EMBED_DIM_test\n"
        "    + 3 * EMBED_DIM_test * EMBED_DIM_test\n"
        "    + EMBED_DIM_test * HIDDEN_DIM_test\n"
        "    + HIDDEN_DIM_test\n"
        "    + HIDDEN_DIM_test * EMBED_DIM_test\n"
        "    + EMBED_DIM_test\n"
        "    + EMBED_DIM_test * VOCAB_SIZE\n"
        ")\n"
        "\n"
        'print(f"Avec EMBED_DIM = {EMBED_DIM_test} :")\n'
        'print(f"  Nombre de parametres : {nb_params_test:,}")\n'
        'print(f"  (Notre modele en a {nb_params:,})")\n'
        "if EMBED_DIM_test < EMBED_DIM:\n"
        '    print("  -> Plus petit : moins de parametres, plus rapide, mais moins precis.")\n'
        "elif EMBED_DIM_test > EMBED_DIM:\n"
        '    print("  -> Plus grand : plus de parametres, potentiellement meilleur.")\n'
        "\n"
        "verifier(\n"
        "    1,\n"
        "    EMBED_DIM_test != 16,\n"
        '    f"Bien joue ! Avec {EMBED_DIM_test} dimensions, le modele a {nb_params_test:,} parametres.",\n'
        '    "Change EMBED_DIM_test pour une autre valeur, par exemple 8 ou 32.",\n'
        ")"
    )
)

# ----------------------------------------------------------------
# CELL 7: MD — Utils
# ----------------------------------------------------------------
cells.append(
    md(
        "---\n"
        "## Les briques de base\n"
        "\n"
        "Avant de construire le LLM, on definit les operations mathematiques\n"
        "de base. Tu les reconnais des lecons precedentes :"
    )
)

# ----------------------------------------------------------------
# CELL 8: Utility functions (code)
# ----------------------------------------------------------------
cells.append(
    code(
        "def rand_matrix(rows, cols, scale=0.3):\n"
        '    """Cree une matrice aleatoire."""\n'
        "    return [[random.gauss(0, scale) for _ in range(cols)] for _ in range(rows)]\n"
        "\n"
        "\n"
        "def rand_vector(size, scale=0.3):\n"
        '    """Cree un vecteur aleatoire."""\n'
        "    return [random.gauss(0, scale) for _ in range(size)]\n"
        "\n"
        "\n"
        "# mat_vec : comme passer a travers un filtre (lecon 3)\n"
        "def mat_vec(mat, vec):\n"
        '    """Multiplication matrice x vecteur."""\n'
        "    return [sum(mat[i][j] * vec[j] for j in range(len(vec))) for i in range(len(mat))]\n"
        "\n"
        "\n"
        "def vec_add(a, b):\n"
        '    """Addition de deux vecteurs."""\n'
        "    return [x + y for x, y in zip(a, b, strict=False)]\n"
        "\n"
        "\n"
        "# softmax : les scores deviennent des probabilites (lecon 1)\n"
        "def softmax(scores):\n"
        '    """Scores -> probabilites (somme = 1)."""\n'
        "    max_s = max(scores)\n"
        "    exps = [math.exp(s - max_s) for s in scores]\n"
        "    total = sum(exps)\n"
        "    return [e / total for e in exps]\n"
        "\n"
        "\n"
        "# relu : porte a sens unique, seules les valeurs positives passent\n"
        "def relu(x):\n"
        '    """Si positif, on garde. Si negatif, on met a zero."""\n'
        "    return [max(0, v) for v in x]\n"
        "\n"
        "\n"
        'print("Fonctions utilitaires definies !")'
    )
)

# ----------------------------------------------------------------
# CELL 9: MD — Init weights
# ----------------------------------------------------------------
cells.append(
    md(
        "---\n"
        "## Etape 1 : Initialiser les poids\n"
        "\n"
        "Chaque composant du LLM a ses propres poids (nombres aleatoires au debut).\n"
        "L'entrainement (lecon 6) trouvera les bonnes valeurs :"
    )
)

# ----------------------------------------------------------------
# CELL 10: Initialize weights (code)
# ----------------------------------------------------------------
cells.append(
    code(
        "# --- Embeddings (chaque lettre et chaque position ont leur vecteur) ---\n"
        "tok_emb = rand_matrix(VOCAB_SIZE, EMBED_DIM, 0.5)  # lettre -> vecteur\n"
        "pos_emb = rand_matrix(CONTEXT, EMBED_DIM, 0.5)     # position -> vecteur\n"
        "\n"
        "# --- Attention : qui est important pour predire la suite ? ---\n"
        "Wq = rand_matrix(EMBED_DIM, EMBED_DIM, 0.2)  # matrice Query\n"
        "Wk = rand_matrix(EMBED_DIM, EMBED_DIM, 0.2)  # matrice Key\n"
        "Wv = rand_matrix(EMBED_DIM, EMBED_DIM, 0.2)  # matrice Value\n"
        "\n"
        "# --- MLP (2 couches) ---\n"
        "W1 = rand_matrix(HIDDEN_DIM, EMBED_DIM, 0.2)  # 16 -> 32\n"
        "b1 = rand_vector(HIDDEN_DIM, 0.1)              # biais\n"
        "W2 = rand_matrix(EMBED_DIM, HIDDEN_DIM, 0.2)   # 32 -> 16\n"
        "b2 = rand_vector(EMBED_DIM, 0.1)               # biais\n"
        "\n"
        "# --- Sortie ---\n"
        "W_out = rand_matrix(VOCAB_SIZE, EMBED_DIM, 0.2)  # 16 -> 27 (une proba par lettre)\n"
        "\n"
        'print("Modele initialise avec des poids aleatoires.")\n'
        'print("Il ne sait rien encore -- il faut l\'entrainer !")'
    )
)

# ----------------------------------------------------------------
# CELL 11: MD — Forward: Embeddings
# ----------------------------------------------------------------
cells.append(
    md(
        "---\n"
        "## Etape 2 : Le forward pass (etape par etape)\n"
        "\n"
        'Le "forward pass" transforme une sequence de lettres en probabilites.\n'
        'Decomposons chaque etape sur l\'exemple **".pik"** :\n'
        "\n"
        "### Etape 2a : Embeddings (lettre + position)"
    )
)

# ----------------------------------------------------------------
# CELL 12: Forward - embeddings demo (code)
# ----------------------------------------------------------------
cells.append(
    code(
        '# On encode ".pik" : chaque lettre -> vecteur de 16 nombres\n'
        'test_mot = ".pik"\n'
        "test_ids = [char_to_id[c] for c in test_mot]  # lettres -> numeros\n"
        "\n"
        "# Embedding = sens de la lettre + sa position dans le mot\n"
        "hidden = []\n"
        "for i, tok_id in enumerate(test_ids):\n"
        "    # On additionne les 2 embeddings pour avoir une representation complete\n"
        "    h = vec_add(tok_emb[tok_id], pos_emb[i % CONTEXT])\n"
        "    hidden.append(h)\n"
        "\n"
        "print(f\"Entree : '{test_mot}' -> ids {test_ids}\")\n"
        'print(f"Apres embeddings : {len(hidden)} vecteurs de {len(hidden[0])} nombres")\n'
        'print(f"  (chaque lettre est maintenant {EMBED_DIM} nombres)")'
    )
)

# ----------------------------------------------------------------
# CELL 13: MD — Forward: Attention
# ----------------------------------------------------------------
cells.append(
    md(
        "### Etape 2b : Self-Attention\n"
        "\n"
        "L'attention decide **quelles lettres sont importantes** pour predire\n"
        "la suite (lecon 4). Elle calcule Q, K, V puis les poids :"
    )
)

# ----------------------------------------------------------------
# CELL 14: Forward - attention demo + BertViz (code)
# ----------------------------------------------------------------
cells.append(
    code(
        "# Query = 'que cherche-t-on ?' (pour la derniere position)\n"
        "q = mat_vec(Wq, hidden[-1])  # 16 nombres\n"
        "\n"
        "# Key = 'qu'a-t-on a offrir ?' et Value = 'l'info a transmettre'\n"
        "scores_attn = []\n"
        "values = []\n"
        "for i in range(len(test_ids)):\n"
        "    k = mat_vec(Wk, hidden[i])  # Key de chaque position\n"
        "    v = mat_vec(Wv, hidden[i])  # Value de chaque position\n"
        "    # Score = compatibilite entre la question (Q) et la reponse (K)\n"
        "    score = sum(q[d] * k[d] for d in range(EMBED_DIM)) / math.sqrt(EMBED_DIM)\n"
        "    scores_attn.append(score)\n"
        "    values.append(v)\n"
        "\n"
        "attn_weights = softmax(scores_attn)  # transformer les scores en poids\n"
        "\n"
        "print(\"Poids d'attention (qui est important pour predire apres 'k') :\")\n"
        "for ch, w in zip(test_mot, attn_weights, strict=False):\n"
        "    print(f\"  '{ch}' : {w:.1%}\")\n"
        "\n"
        "# Somme ponderee des Values\n"
        "attn_out = [0.0] * EMBED_DIM\n"
        "for i in range(len(test_ids)):\n"
        "    for d in range(EMBED_DIM):\n"
        "        attn_out[d] += attn_weights[i] * values[i][d]\n"
        "\n"
        "# Connexion residuelle (raccourci)\n"
        "x = vec_add(hidden[-1], attn_out)\n"
        'print(f"\\nApres attention + residuelle : {len(x)} nombres")\n'
        "\n"
        "# Visualisation BertViz\n"
        "afficher_attention(attn_weights, list(test_mot), titre=\"Attention sur '.pik'\")"
    )
)

# ----------------------------------------------------------------
# CELL 15: MD — Forward: MLP + output
# ----------------------------------------------------------------
cells.append(
    md(
        "### Etape 2c : MLP + Sortie\n"
        "\n"
        "Le MLP transforme le resultat de l'attention, puis une derniere\n"
        "couche convertit en 27 scores (un par lettre) :"
    )
)

# ----------------------------------------------------------------
# CELL 16: Forward - MLP + softmax + barres (code)
# ----------------------------------------------------------------
cells.append(
    code(
        "# MLP : le reseau de neurones interne transforme le resultat de l'attention\n"
        "h = relu(vec_add(mat_vec(W1, x), b1))    # 32 nombres (couche cachee)\n"
        "mlp_out = vec_add(mat_vec(W2, h), b2)     # 16 nombres (retour a EMBED_DIM)\n"
        "# Connexion residuelle : garder l'original + ajouter la nouveaute\n"
        "x = vec_add(x, mlp_out)\n"
        "\n"
        "# Sortie : les 16 nombres deviennent 27 scores (un par lettre)\n"
        "logits = mat_vec(W_out, x)  # scores bruts (peuvent etre negatifs)\n"
        "probas = softmax(logits)    # probabilites (entre 0 et 1, somme = 1)\n"
        "\n"
        "# Top 5 predictions\n"
        "top5 = sorted(range(VOCAB_SIZE), key=lambda i: -probas[i])[:5]\n"
        "print(\"Predictions (avant entrainement) pour la lettre apres '.pik' :\")\n"
        "for idx in top5:\n"
        "    print(f\"  '{id_to_char[idx]}' : {probas[idx]:.1%}\")\n"
        "print(\"\\n  (C'est du hasard pour l'instant - il faut entrainer !)\")\n"
        "\n"
        "afficher_barres(\n"
        "    [probas[i] for i in top5],\n"
        "    [id_to_char[i] for i in top5],\n"
        "    titre=\"Top 5 predictions apres '.pik' (avant entrainement)\",\n"
        ")"
    )
)

# ----------------------------------------------------------------
# CELL 17: MD — Complete function
# ----------------------------------------------------------------
cells.append(
    md(
        "---\n"
        "## La fonction complete\n"
        "\n"
        "On assemble les 3 etapes en une seule fonction `forward_llm` :"
    )
)

# ----------------------------------------------------------------
# CELL 18: forward_llm complete (code)
# ----------------------------------------------------------------
cells.append(
    code(
        "# Cette fonction assemble les 3 etapes en une seule\n"
        "def forward_llm(sequence_ids):\n"
        '    """Passe une sequence dans le mini-LLM et retourne les probas."""\n'
        "    n = len(sequence_ids)\n"
        "\n"
        "    # 1. Embeddings : sens de la lettre + position dans le mot\n"
        "    hidden = []\n"
        "    for i, tok_id in enumerate(sequence_ids):\n"
        "        h = vec_add(tok_emb[tok_id], pos_emb[i % CONTEXT])\n"
        "        hidden.append(h)\n"
        "\n"
        "    # 2. Self-Attention (sur la derniere position)\n"
        "    q = mat_vec(Wq, hidden[-1])\n"
        "    scores = []\n"
        "    values = []\n"
        "    for i in range(n):\n"
        "        k = mat_vec(Wk, hidden[i])\n"
        "        v = mat_vec(Wv, hidden[i])\n"
        "        score = sum(q[d] * k[d] for d in range(EMBED_DIM)) / math.sqrt(EMBED_DIM)\n"
        "        scores.append(score)\n"
        "        values.append(v)\n"
        "    attn_weights = softmax(scores)\n"
        "    attn_out = [0.0] * EMBED_DIM\n"
        "    for i in range(n):\n"
        "        for d in range(EMBED_DIM):\n"
        "            attn_out[d] += attn_weights[i] * values[i][d]\n"
        "    x = vec_add(hidden[-1], attn_out)  # + residuelle\n"
        "\n"
        "    # 3. MLP\n"
        "    h = relu(vec_add(mat_vec(W1, x), b1))\n"
        "    mlp_out = vec_add(mat_vec(W2, h), b2)\n"
        "    x = vec_add(x, mlp_out)  # + residuelle\n"
        "\n"
        "    # 4. Sortie\n"
        "    logits = mat_vec(W_out, x)\n"
        "    return softmax(logits)\n"
        "\n"
        "\n"
        "def _calculer_poids_attention(texte):\n"
        '    """Calcule les poids d\'attention pour un texte."""\n'
        "    ids = [char_to_id[c] for c in texte]\n"
        "    hidden = [vec_add(tok_emb[tid], pos_emb[i % CONTEXT]) for i, tid in enumerate(ids)]\n"
        "    q = mat_vec(Wq, hidden[-1])\n"
        "    scores = []\n"
        "    for i in range(len(ids)):\n"
        "        k = mat_vec(Wk, hidden[i])\n"
        "        score = sum(q[d] * k[d] for d in range(EMBED_DIM)) / math.sqrt(EMBED_DIM)\n"
        "        scores.append(score)\n"
        "    return softmax(scores)\n"
        "\n"
        "\n"
        "# Verification rapide\n"
        "check = forward_llm(test_ids)\n"
        "print(f\"forward_llm('.pik') -> {len(check)} probabilites, somme = {sum(check):.4f}\")\n"
        'print("Fonction complete prete !")'
    )
)

# ----------------------------------------------------------------
# CELL 19: MD — Before exercise 2
# ----------------------------------------------------------------
cells.append(md("Testons le modele avec differents debuts de mots :"))

# ----------------------------------------------------------------
# CELL 20: Exercise 2 — change debut (code)
# ----------------------------------------------------------------
cells.append(
    code(
        "exercice(\n"
        "    2,\n"
        '    "Change le debut du mot",\n'
        '    \'Change <code>mon_debut</code> ci-dessous (essaie <code>".bul"</code>, <code>".evo"</code> ou <code>".dra"</code>).\',\n'
        '    "Le modele predit des lettres differentes selon le debut.",\n'
        ")\n"
        "\n"
        "# \u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557\n"
        "# \u2551  A TOI DE JOUER !                    \u2551\n"
        "# \u2560\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2563\n"
        "\n"
        'mon_debut = ".pik"  # <-- Essaie ".bul", ".evo" ou ".dra" !\n'
        "\n"
        "# \u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d\n"
        "\n"
        "test_ids = [char_to_id[c] for c in mon_debut]\n"
        "probas = forward_llm(test_ids)\n"
        "top5 = sorted(range(VOCAB_SIZE), key=lambda i: -probas[i])[:5]\n"
        "\n"
        "print(f\"Predictions apres '{mon_debut}' :\")\n"
        "for idx in top5:\n"
        "    print(f\"  '{id_to_char[idx]}' : {probas[idx]:.1%}\")\n"
        "print(\"\\n(Le modele n'est pas entraine, donc c'est du hasard !)\")\n"
        "\n"
        "afficher_barres(\n"
        "    [probas[i] for i in top5],\n"
        "    [id_to_char[i] for i in top5],\n"
        "    titre=f\"Top 5 predictions apres '{mon_debut}'\",\n"
        ")\n"
        "afficher_attention(\n"
        "    _calculer_poids_attention(mon_debut),\n"
        "    list(mon_debut),\n"
        "    titre=f\"Poids d'attention pour '{mon_debut}'\",\n"
        ")\n"
        "\n"
        "verifier(\n"
        "    2,\n"
        '    mon_debut != ".pik",\n'
        "    f\"Super ! Tu as teste les predictions apres '{mon_debut}'.\",\n"
        "    \"Change mon_debut pour un autre debut, par exemple '.bul' ou '.evo'.\",\n"
        ")"
    )
)

# ----------------------------------------------------------------
# CELL 21: MD — Loss
# ----------------------------------------------------------------
cells.append(
    md(
        "---\n"
        "## La loss du modele\n"
        "\n"
        "Comme dans la lecon 2, on mesure l'erreur du modele avec la **loss**.\n"
        "Un modele aleatoire a une loss de ~3.3 (= log(27)).\n"
        "Apres entrainement, elle devrait descendre bien plus bas :"
    )
)

# ----------------------------------------------------------------
# CELL 22: Loss calculation (code)
# ----------------------------------------------------------------
cells.append(
    code(
        "pokemons = [\n"
        '    "arcanin", "bulbizarre", "carapuce", "dracaufeu", "ectoplasma",\n'
        '    "evoli", "felinferno", "gardevoir", "goupix", "lokhlass",\n'
        '    "lucario", "metamorph", "mewtwo", "noctali", "pikachu",\n'
        '    "rondoudou", "ronflex", "salameche", "togepi", "voltali",\n'
        "]\n"
        "\n"
        "\n"
        "def calcul_loss(pokemons):\n"
        '    """Calcule la loss moyenne sur tous les Pokemon."""\n'
        "    loss_totale = 0\n"
        "    nb = 0\n"
        "    for pokemon in pokemons:\n"
        '        mot = "." + pokemon + "."\n'
        "        ids = [char_to_id[c] for c in mot]\n"
        "        for i in range(1, len(ids)):\n"
        "            seq = ids[:i]\n"
        "            cible = ids[i]  # la bonne reponse\n"
        "            probas = forward_llm(seq[-CONTEXT:])\n"
        "            # -log(proba) : si le modele est sur -> petite loss, incertain -> grande loss\n"
        "            loss_totale += -math.log(probas[cible] + 1e-10)\n"
        "            nb += 1\n"
        "    return loss_totale / nb  # moyenne sur toutes les positions\n"
        "\n"
        "\n"
        "loss_initiale = calcul_loss(pokemons)\n"
        'print(f"Loss initiale : {loss_initiale:.3f}")\n'
        'print(f"(Loss d\'un modele aleatoire : {math.log(VOCAB_SIZE):.3f})")\n'
        "print()\n"
        'print("L\'entrainement complet se fait dans la lecon 6.")\n'
        'print("Mais l\'ARCHITECTURE est exactement la meme que GPT-2/3/4 !")'
    )
)

# ----------------------------------------------------------------
# CELL 23: MD — Generation
# ----------------------------------------------------------------
cells.append(
    md(
        "---\n"
        "## Generation de noms\n"
        "\n"
        "Meme sans entrainement, on peut voir le **mecanisme** de generation :\n"
        "le modele genere une lettre a la fois, en se basant sur les probabilites :"
    )
)

# ----------------------------------------------------------------
# CELL 24: Generation function + demo + animation (code)
# ----------------------------------------------------------------
cells.append(
    code(
        "# Generer un nom lettre par lettre, comme ChatGPT genere mot par mot\n"
        'def generer_llm(debut=".", temperature=1.0, max_len=15):\n'
        '    """Genere un nom de Pokemon lettre par lettre."""\n'
        "    ids = [char_to_id[c] for c in debut]\n"
        "    resultat = debut\n"
        "    for _ in range(max_len):\n"
        "        probas = forward_llm(ids[-CONTEXT:])  # predire la prochaine lettre\n"
        "        # Temperature : basse = toujours la meme chose, haute = surprenant\n"
        "        if temperature != 1.0:\n"
        "            logits = [math.log(p + 1e-10) / temperature for p in probas]\n"
        "            probas = softmax(logits)\n"
        "        idx = random.choices(range(VOCAB_SIZE), weights=probas, k=1)[0]\n"
        '        if idx == char_to_id["."]:\n'
        "            break\n"
        "        ids.append(idx)\n"
        "        resultat += id_to_char[idx]\n"
        '    return resultat[1:] if resultat.startswith(".") else resultat\n'
        "\n"
        "\n"
        'print("Noms generes (modele non-entraine, juste le mecanisme) :")\n'
        "print()\n"
        "noms = [generer_llm(temperature=0.8).capitalize() for _ in range(10)]\n"
        "for nom in noms:\n"
        '    print(f"  {nom}")\n'
        "print()\n"
        "print(\"C'est du charabia car le modele n'est pas entraine.\")\n"
        'print("Mais le MECANISME est exactement celui de ChatGPT !")\n'
        "\n"
        "# Animation du dernier nom genere\n"
        "afficher_generation(noms[-1], delai_ms=250)"
    )
)

# ----------------------------------------------------------------
# CELL 25: MD — Temperature
# ----------------------------------------------------------------
cells.append(
    md(
        "---\n"
        "## La temperature\n"
        "\n"
        "La **temperature** controle la creativite du modele :\n"
        "- **T < 1** : conservateur (toujours les lettres les plus probables)\n"
        "- **T = 1** : normal\n"
        "- **T > 1** : creatif (explore des combinaisons inhabituelles)\n"
        "\n"
        "Deplace le curseur ci-dessous pour voir l'effet en temps reel :"
    )
)

# ----------------------------------------------------------------
# CELL 26: Temperature slider + exercise 3 (code)
# ----------------------------------------------------------------
cells.append(
    code(
        "# Calcul des probas pour le slider interactif\n"
        '_probas_temp = forward_llm([char_to_id[c] for c in ".pik"])\n'
        "_top_idx = sorted(range(VOCAB_SIZE), key=lambda i: -_probas_temp[i])[:10]\n"
        "afficher_temperature(\n"
        "    [_probas_temp[i] for i in _top_idx],\n"
        "    [id_to_char[i] for i in _top_idx],\n"
        "    titre=\"Effet de la temperature sur les predictions apres '.pik'\",\n"
        ")"
    )
)

# ----------------------------------------------------------------
# CELL 27: MD — before exercise 3
# ----------------------------------------------------------------
cells.append(md("A toi de generer avec differentes temperatures :"))

# ----------------------------------------------------------------
# CELL 28: Exercise 3 — temperature (code)
# ----------------------------------------------------------------
cells.append(
    code(
        "exercice(\n"
        "    3,\n"
        '    "Joue avec la temperature",\n'
        '    "Change <code>ma_temperature</code> ci-dessous (essaie 0.1 ou 2.0).",\n'
        '    "Temperature basse = repetitif. Temperature haute = creatif.",\n'
        ")\n"
        "\n"
        "# \u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557\n"
        "# \u2551  A TOI DE JOUER !                    \u2551\n"
        "# \u2560\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2563\n"
        "\n"
        "ma_temperature = 0.8  # <-- Essaie 0.1 (sage) ou 2.0 (fou) !\n"
        "\n"
        "# \u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d\n"
        "\n"
        'print(f"Generation avec temperature = {ma_temperature} :")\n'
        "print()\n"
        "for _ in range(10):\n"
        "    nom = generer_llm(temperature=ma_temperature).capitalize()\n"
        '    print(f"  {nom}")\n'
        "print()\n"
        "if ma_temperature < 0.5:\n"
        '    print("Temperature basse : le modele choisit toujours les lettres les plus probables.")\n'
        "elif ma_temperature > 1.5:\n"
        '    print("Temperature haute : le modele explore des combinaisons inhabituelles !")\n'
        "else:\n"
        '    print("Temperature moyenne : un bon equilibre entre creativite et coherence.")\n'
        "\n"
        "verifier(\n"
        "    3,\n"
        "    ma_temperature != 0.8,\n"
        '    f"Genial ! Tu as explore la temperature {ma_temperature}.",\n'
        '    "Change ma_temperature pour une autre valeur, par exemple 0.1 ou 2.0.",\n'
        ")"
    )
)

# ----------------------------------------------------------------
# CELL 29: MD — Conclusion
# ----------------------------------------------------------------
cells.append(
    md(
        "---\n"
        "## Ce qu'on a appris\n"
        "\n"
        "```\n"
        "Lecon 1 : Compter les lettres qui suivent        -> bigramme\n"
        "Lecon 2 : Apprendre de ses erreurs                -> entrainement\n"
        "Lecon 3 : Regarder plusieurs lettres en arriere   -> embeddings + contexte\n"
        "Lecon 4 : Choisir les lettres importantes          -> attention\n"
        "Lecon 5 : Assembler le tout                       -> mini-LLM !\n"
        "```\n"
        "\n"
        "## La difference avec ChatGPT\n"
        "\n"
        "| | Notre mini-LLM | ChatGPT |\n"
        "|---|---|---|\n"
        "| Architecture | La meme ! | La meme ! |\n"
        "| Parametres | ~2,800 | ~1,800,000,000,000 |\n"
        "| Donnees | 20 Pokemon | Internet entier |\n"
        "| Calcul | 1 PC, secondes | Des milliers de GPU, des mois |\n"
        "| Resultat | Noms de Pokemon inventes | Conversations, code, poesie... |\n"
        "\n"
        "L'algorithme est **le meme**. La seule difference, c'est l'echelle.\n"
        "\n"
        '> *"This file is the complete algorithm. Everything else is just efficiency."*\n'
        "> -- Andrej Karpathy\n"
        "\n"
        "---\n"
        "\n"
        "**Felicitations ! Tu as compris comment fonctionne un LLM.**\n"
        "\n"
        "*Prochaine lecon : [06 - Entrainer le modele](06_entrainer_le_modele.ipynb)*"
    )
)

# ----------------------------------------------------------------
# CELL 30: MD — Sources
# ----------------------------------------------------------------
cells.append(
    md(
        "---\n"
        "\n"
        "### Sources (ISO 42001)\n"
        "\n"
        "- **Architecture complete GPT (embedding + attention + MLP + softmax)** : [microgpt.py](https://gist.github.com/karpathy/8627fe009c40f57531cb18360106ce95) \\u2014 Andrej Karpathy\n"
        "- **Comparaison des parametres GPT-4** : estimations publiques basees sur les rapports techniques OpenAI\n"
        '- **Explication du forward pass complet** : [Video "Let\'s build GPT"](https://www.youtube.com/watch?v=kCc8FmEb1nY) \\u2014 Andrej Karpathy (2023)\n'
        "- **Concept de temperature pour la generation** : meme source, section sampling\n"
        '- **"Attention Is All You Need"** : Vaswani et al., 2017, [arXiv:1706.03762](https://arxiv.org/abs/1706.03762)\n'
        "- **Dataset Pokemon** : (c) Nintendo / Creatures Inc. / GAME FREAK inc., usage educatif. Source : [PokeAPI](https://pokeapi.co/)"
    )
)

# ================================================================
# Write rebuilt notebook
# ================================================================
nb["cells"] = cells
with open("notebooks/05_mon_premier_llm.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"NB05 rebuilt: {len(cells)} cells (was 15)")
