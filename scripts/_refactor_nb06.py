#!/usr/bin/env python3
"""Refactor NB06: Entrainer le modele — pedagogical overhaul.

Key changes:
- Cell 1 infra: animated loss curve + comparaison avant/apres + generation animation
- Pokemon data: comment header + print dataset size
- Config: split config + utils
- forward_avec_cache: split into function + test
- backward: keep as one function, enrich comments, add demo after
- Training: animated loss curve
- After training: comparaison avant/apres (new viz 9/9)
- All 3 exercises: box-drawing delimiters
"""

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


with open("notebooks/06_entrainer_le_modele.ipynb", encoding="utf-8") as f:
    nb = json.load(f)

# Extract verifier + exercice from cell 1
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

# Extract Pokemon data from cell 3
pokemon_cell = "".join(
    nb["cells"][3]["source"]
    if isinstance(nb["cells"][3]["source"], list)
    else [nb["cells"][3]["source"]]
)

cells = []

# ================================================================
# CELL 0: Intro (markdown)
# ================================================================
cells.append(
    md(
        "> **Rappel** : clique sur une cellule grise, puis **Shift + Entree** pour l'executer.\n"
        "> Execute les cellules **dans l'ordre** de haut en bas.\n"
        "\n"
        "---\n"
        "\n"
        "# Lecon 6 : Entrainer le modele\n"
        "\n"
        "## Le moment de verite !\n"
        "\n"
        "Dans la lecon 5, on a construit un mini-LLM complet : embeddings,\n"
        "attention, MLP, softmax. Mais ses poids etaient **aleatoires** --\n"
        "il ne savait rien et generait du charabia.\n"
        "\n"
        "Aujourd'hui, on va lui **apprendre** a generer des noms de Pokemon.\n"
        "\n"
        "C'est comme un joueur qui decouvre des centaines de Pokemon et finit\n"
        'par comprendre "comment ca sonne", un nom de Pokemon.\n'
        "\n"
        "> L'entrainement va prendre quelques minutes. Pendant que le modele\n"
        '> apprend, tu pourras lire les sections "En vrai..." plus bas !'
    )
)

# ================================================================
# CELL 1: Infrastructure (code)
# ================================================================
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
    # --- afficher_evolution_loss: animated SVG curve (from NB02 pattern) ---
    'def afficher_evolution_loss(pertes, titre="Courbe de loss"):\n'
    '    """Courbe de loss animee (la ligne se dessine + hover = valeur)."""\n'
    "    if not pertes:\n"
    "        return\n"
    "    uid = uuid.uuid4().hex[:8]\n"
    "    n = len(pertes)\n"
    "    max_loss = max(pertes)\n"
    "    min_loss = min(pertes)\n"
    "    w, h, pad = 500, 160, 30\n"
    "    pw = w - 2 * pad\n"
    "    ph = h - 2 * pad\n"
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
    "    path_len = n * 20\n"
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
    # --- afficher_barres: animated SVG bars ---
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
    # --- afficher_comparaison: before/after split view (NEW viz 9/9) ---
    "def afficher_comparaison(noms_avant, noms_apres):\n"
    '    """Comparaison avant/apres entrainement cote a cote."""\n'
    '    avant_html = ""\n'
    "    for nom in noms_avant:\n"
    "        avant_html += (\n"
    "            f'<div style=\"padding:3px 0;font-family:monospace;font-size:0.95em\">{nom.capitalize()}</div>'\n"
    "        )\n"
    '    apres_html = ""\n'
    "    for nom in noms_apres:\n"
    "        apres_html += (\n"
    "            f'<div style=\"padding:3px 0;font-family:monospace;font-size:0.95em\">{nom.capitalize()}</div>'\n"
    "        )\n"
    "    display(HTML(\n"
    "        f'<!-- tuto-viz -->'\n"
    "        f'<div style=\"display:flex;gap:16px;margin:8px 0\">'\n"
    "        f'<div style=\"flex:1;padding:12px;background:#fff3cd;border-radius:8px;border:2px solid #ffc107\">'\n"
    "        f'<div style=\"font-weight:bold;margin-bottom:8px;color:#856404\">'\n"
    "        f'\\u274c AVANT entrainement</div>'\n"
    "        f'{avant_html}</div>'\n"
    "        f'<div style=\"flex:1;padding:12px;background:#d4edda;border-radius:8px;border:2px solid #28a745\">'\n"
    "        f'<div style=\"font-weight:bold;margin-bottom:8px;color:#155724\">'\n"
    "        f'\\u2705 APRES entrainement</div>'\n"
    "        f'{apres_html}</div></div>'\n"
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

# ================================================================
# CELL 2: MD — Etape 1: Charger les Pokemon
# ================================================================
cells.append(
    md(
        "---\n"
        "## Etape 1 : Charger les noms de Pokemon\n"
        "\n"
        "Dans les lecons precedentes, on utilisait une poignee de Pokemon\n"
        "ecrits a la main. Maintenant, on utilise un vrai dataset :\n"
        "\n"
        "**~1 000 noms de Pokemon** tires de la PokeAPI ((c) Nintendo).\n"
        "\n"
        "Fais defiler la cellule ci-dessous, pas besoin de lire les noms :"
    )
)

# ================================================================
# CELL 3: Pokemon data (code) — add header comment + print
# ================================================================
cells.append(code(pokemon_cell))

# ================================================================
# CELL 4: MD — Etape 2: Preparer le modele
# ================================================================
cells.append(
    md(
        "---\n"
        "## Etape 2 : Preparer le modele\n"
        "\n"
        "On reprend **exactement la meme architecture** que la lecon 5\n"
        "(embeddings + attention + MLP) avec les memes dimensions :\n"
        "\n"
        "| Parametre | Valeur | Rappel |\n"
        "|-----------|--------|--------|\n"
        "| Dimension embeddings | 16 | Chaque lettre = 16 nombres |\n"
        "| Taille MLP | 32 | Reseau de neurones interne |\n"
        "| Contexte | 8 | Fenetre de 8 lettres max |\n"
        "| Parametres | ~2 800 | Les nombres que le modele va ajuster |\n"
        "\n"
        "C'est exactement le modele de la lecon 5, mais cette fois on va\n"
        "l'entrainer **pour de vrai** !"
    )
)

# ================================================================
# CELL 5: Vocab + config (code)
# ================================================================
cells.append(
    code(
        "# --- Vocabulaire ---\n"
        'VOCAB = list(".abcdefghijklmnopqrstuvwxyz")\n'
        "VOCAB_SIZE = len(VOCAB)  # 27 symboles\n"
        "# Dictionnaires de traduction : lettre <-> numero\n"
        "char_to_id = {c: i for i, c in enumerate(VOCAB)}\n"
        "id_to_char = {i: c for i, c in enumerate(VOCAB)}\n"
        "\n"
        "# --- Configuration (memes dimensions que lecon 5) ---\n"
        "# Chaque lettre = 16 nombres (sa 'fiche d'identite')\n"
        "EMBED_DIM = 16    # taille des embeddings\n"
        "CONTEXT = 8       # fenetre de contexte\n"
        "HIDDEN_DIM = 32   # taille du MLP\n"
        "\n"
        "# Comptons les parametres : c'est le nombre de nombres que le modele apprend\n"
        "nb_params = (\n"
        "    VOCAB_SIZE * EMBED_DIM      # tok_emb : 27 x 16 = 432\n"
        "    + CONTEXT * EMBED_DIM       # pos_emb : 8 x 16 = 128\n"
        "    + 3 * EMBED_DIM * EMBED_DIM # Wq, Wk, Wv : 3 x 256 = 768\n"
        "    + HIDDEN_DIM * EMBED_DIM    # W1 : 32 x 16 = 512\n"
        "    + HIDDEN_DIM               # b1 : 32\n"
        "    + EMBED_DIM * HIDDEN_DIM    # W2 : 16 x 32 = 512\n"
        "    + EMBED_DIM               # b2 : 16\n"
        "    + VOCAB_SIZE * EMBED_DIM    # W_out : 27 x 16 = 432\n"
        ")\n"
        'print(f"Parametres du modele : {nb_params}")\n'
        'print(f"  Embeddings : {VOCAB_SIZE} x {EMBED_DIM} = {VOCAB_SIZE * EMBED_DIM}")\n'
        'print(f"  Attention : 3 x {EMBED_DIM} x {EMBED_DIM} = {3 * EMBED_DIM * EMBED_DIM}")\n'
        'print(f"  MLP : {HIDDEN_DIM * EMBED_DIM + HIDDEN_DIM + EMBED_DIM * HIDDEN_DIM + EMBED_DIM}")\n'
        'print(f"  Sortie : {VOCAB_SIZE} x {EMBED_DIM} = {VOCAB_SIZE * EMBED_DIM}")'
    )
)

# ================================================================
# CELL 6: MD — fonctions utilitaires
# ================================================================
cells.append(
    md(
        "Les fonctions de base sont les memes que dans la lecon 5\n"
        "(matrice x vecteur, softmax, initialisation aleatoire) :"
    )
)

# ================================================================
# CELL 7: Utils + init poids (code)
# ================================================================
cells.append(
    code(
        "import math\n"
        "import random\n"
        "import time\n"
        "\n"
        "# Graine fixe : memes resultats a chaque execution\n"
        "random.seed(42)\n"
        "\n"
        "\n"
        "def rand_matrix(rows, cols, scale=0.3):\n"
        '    """Cree une matrice de nombres aleatoires."""\n'
        "    return [[random.gauss(0, scale) for _ in range(cols)] for _ in range(rows)]\n"
        "\n"
        "\n"
        "def rand_vector(size, scale=0.3):\n"
        '    """Cree un vecteur de nombres aleatoires."""\n'
        "    return [random.gauss(0, scale) for _ in range(size)]\n"
        "\n"
        "\n"
        "def softmax(scores):\n"
        '    """Transforme des scores en probabilites (somme = 1)."""\n'
        "    max_s = max(scores)\n"
        "    exps = [math.exp(s - max_s) for s in scores]\n"
        "    total = sum(exps)\n"
        "    return [e / total for e in exps]\n"
        "\n"
        "\n"
        "def mat_vec(mat, vec):\n"
        '    """Multiplie une matrice par un vecteur."""\n'
        "    return [sum(mat[i][j] * vec[j] for j in range(len(vec))) for i in range(len(mat))]\n"
        "\n"
        "\n"
        "# --- Initialisation des poids (aleatoires) ---\n"
        "# Au debut, le modele ne sait rien : tous les poids sont au hasard\n"
        "tok_emb = rand_matrix(VOCAB_SIZE, EMBED_DIM, 0.5)  # embeddings des tokens\n"
        "pos_emb = rand_matrix(CONTEXT, EMBED_DIM, 0.5)      # embeddings de position\n"
        "Wq = rand_matrix(EMBED_DIM, EMBED_DIM, 0.2)         # poids attention (query)\n"
        "Wk = rand_matrix(EMBED_DIM, EMBED_DIM, 0.2)         # poids attention (key)\n"
        "Wv = rand_matrix(EMBED_DIM, EMBED_DIM, 0.2)         # poids attention (value)\n"
        "W1 = rand_matrix(HIDDEN_DIM, EMBED_DIM, 0.2)        # MLP couche 1\n"
        "b1 = rand_vector(HIDDEN_DIM, 0.1)                   # biais couche 1\n"
        "W2 = rand_matrix(EMBED_DIM, HIDDEN_DIM, 0.2)        # MLP couche 2\n"
        "b2 = rand_vector(EMBED_DIM, 0.1)                    # biais couche 2\n"
        "W_out = rand_matrix(VOCAB_SIZE, EMBED_DIM, 0.2)     # couche de sortie\n"
        "\n"
        'print(f"Mini-LLM initialise avec {nb_params} parametres aleatoires.")'
    )
)

# ================================================================
# CELL 8: MD — forward avec cache
# ================================================================
cells.append(
    md(
        "---\n"
        "### Le forward pass (avec cache)\n"
        "\n"
        "Le forward pass est le meme que dans la lecon 5, mais il **sauvegarde\n"
        "les etapes intermediaires** dans un cache. On en aura besoin pour\n"
        "le backward (la retropropagation) :"
    )
)

# ================================================================
# CELL 9: forward_avec_cache function (code)
# ================================================================
cells.append(
    code(
        "def forward_avec_cache(sequence_ids):\n"
        '    """Forward pass qui sauvegarde les etapes pour le backward."""\n'
        "    # Meme calcul que lecon 5, mais on garde tout en memoire (le cache)\n"
        "    n = len(sequence_ids)\n"
        "\n"
        "    # 1. Embeddings : combiner le sens de la lettre + sa position dans le mot\n"
        "    hidden = []\n"
        "    for i, tok_id in enumerate(sequence_ids):\n"
        "        h = [tok_emb[tok_id][d] + pos_emb[i % CONTEXT][d] for d in range(EMBED_DIM)]\n"
        "        hidden.append(h)\n"
        "\n"
        "    # 2. Self-Attention (derniere position uniquement)\n"
        "    q = mat_vec(Wq, hidden[-1])  # query de la derniere lettre\n"
        "\n"
        "    # Pour chaque position, calculer cle et valeur (qui suis-je ? qu'ai-je a offrir ?)\n"
        "    scores_bruts = []\n"
        "    cles = []\n"
        "    valeurs = []\n"
        "    for i in range(n):\n"
        "        k = mat_vec(Wk, hidden[i])  # cle de la position i\n"
        "        v = mat_vec(Wv, hidden[i])  # valeur de la position i\n"
        "        # Score = combien la query s'interesse a cette cle\n"
        "        score = sum(q[d] * k[d] for d in range(EMBED_DIM)) / math.sqrt(EMBED_DIM)\n"
        "        scores_bruts.append(score)\n"
        "        cles.append(k)\n"
        "        valeurs.append(v)\n"
        "\n"
        "    # Les scores deviennent des probabilites (qui est le plus important ?)\n"
        "    poids_attn = softmax(scores_bruts)\n"
        "\n"
        "    # Somme ponderee des valeurs\n"
        "    # Somme ponderee : collecter l'info selon les poids d'attention\n"
        "    sortie_attn = [0.0] * EMBED_DIM\n"
        "    for i in range(n):\n"
        "        for d in range(EMBED_DIM):\n"
        "            sortie_attn[d] += poids_attn[i] * valeurs[i][d]\n"
        "\n"
        "    # Connexion residuelle 1 : garder l'original + ajouter l'attention\n"
        "    x = [hidden[-1][d] + sortie_attn[d] for d in range(EMBED_DIM)]\n"
        "    x_apres_attn = list(x)  # sauvegarde pour le backward\n"
        "\n"
        "    # 3. MLP (reseau de neurones)\n"
        "    h1_pre = [  # couche cachee : melanger toutes les dimensions\n"
        "        sum(W1[j][d] * x[d] for d in range(EMBED_DIM)) + b1[j]\n"
        "        for j in range(HIDDEN_DIM)\n"
        "    ]\n"
        "    h1 = [max(0.0, v) for v in h1_pre]  # ReLU : garde les positifs\n"
        "    sortie_mlp = [  # reprojeter vers la taille d'embedding\n"
        "        sum(W2[d][j] * h1[j] for j in range(HIDDEN_DIM)) + b2[d]\n"
        "        for d in range(EMBED_DIM)\n"
        "    ]\n"
        "\n"
        "    # Connexion residuelle 2 : original + sortie MLP\n"
        "    x_final = [x[d] + sortie_mlp[d] for d in range(EMBED_DIM)]\n"
        "\n"
        "    # 4. Sortie : transformer le vecteur final en 27 scores (un par lettre)\n"
        "    logits = [\n"
        "        sum(W_out[v][d] * x_final[d] for d in range(EMBED_DIM))\n"
        "        for v in range(VOCAB_SIZE)\n"
        "    ]\n"
        "    probas = softmax(logits)\n"
        "\n"
        "    # Sauvegarder TOUT pour le backward (on en aura besoin pour remonter)\n"
        "    cache = {\n"
        '        "ids": sequence_ids,\n'
        '        "hidden": hidden,\n'
        '        "q": q,\n'
        '        "cles": cles,\n'
        '        "valeurs": valeurs,\n'
        '        "scores_bruts": scores_bruts,\n'
        '        "poids_attn": poids_attn,\n'
        '        "sortie_attn": sortie_attn,\n'
        '        "x_apres_attn": x_apres_attn,\n'
        '        "h1_pre": h1_pre,\n'
        '        "h1": h1,\n'
        '        "sortie_mlp": sortie_mlp,\n'
        '        "x_final": x_final,\n'
        "    }\n"
        "    return probas, cache\n"
        "\n"
        "\n"
        'print("Forward pass defini (avec cache pour le backward).")'
    )
)

# ================================================================
# CELL 10: MD — test loss initiale
# ================================================================
cells.append(
    md(
        "Testons le modele avec ses poids aleatoires. La loss devrait etre\n"
        "proche de log(27) = 3.30 (le modele devine au hasard parmi 27 lettres) :"
    )
)

# ================================================================
# CELL 11: Test loss initiale (code)
# ================================================================
cells.append(
    code(
        "# Loss initiale (poids aleatoires)\n"
        "loss_totale = 0\n"
        "nb = 0\n"
        "for pokemon in pokemons[:100]:  # 100 Pokemon pour aller vite\n"
        '    mot = "." + pokemon + "."\n'
        "    ids = [char_to_id[c] for c in mot]\n"
        "    for i in range(1, len(ids)):\n"
        "        seq = ids[:i][-CONTEXT:]  # fenetre de contexte\n"
        "        cible = ids[i]            # lettre a predire\n"
        "        probas, _ = forward_avec_cache(seq)\n"
        "        # -log(proba) : si le modele donne 1% -> loss = 4.6 (mauvais !)\n"
        "        loss_totale += -math.log(probas[cible] + 1e-10)\n"
        "        nb += 1\n"
        "\n"
        "loss_initiale = loss_totale / nb\n"
        'print(f"Loss initiale (poids aleatoires) : {loss_initiale:.3f}")\n'
        'print(f"Loss theorique aleatoire : {math.log(VOCAB_SIZE):.3f}")\n'
        'print(f"  -> Le modele devine au hasard parmi {VOCAB_SIZE} lettres.")'
    )
)

# ================================================================
# CELL 12: MD — generation avant
# ================================================================
cells.append(
    md(
        "### Generation avant entrainement\n"
        "\n"
        "Voyons ce que le modele genere avec ses poids aleatoires :"
    )
)

# ================================================================
# CELL 13: generer + noms_avant (code)
# ================================================================
cells.append(
    code(
        "# Le modele predit lettre par lettre (comme ChatGPT predit mot par mot)\n"
        'def generer(debut=".", temperature=0.8, max_len=15):\n'
        '    """Genere un nom de Pokemon lettre par lettre."""\n'
        "    ids = [char_to_id[c] for c in debut]  # convertir lettres en numeros\n"
        "    resultat = debut\n"
        "    for _ in range(max_len):  # max 15 lettres (securite)\n"
        "        # Predire la prochaine lettre avec le forward pass\n"
        "        probas, _ = forward_avec_cache(ids[-CONTEXT:])\n"
        "        # temperature < 1 = prudent, > 1 = creatif\n"
        "        if temperature != 1.0:\n"
        "            logits_t = [math.log(p + 1e-10) / temperature for p in probas]\n"
        "            probas = softmax(logits_t)\n"
        "        # Tirer au sort une lettre selon les probabilites\n"
        "        idx = random.choices(range(VOCAB_SIZE), weights=probas, k=1)[0]\n"
        '        if idx == char_to_id["."]:\n'
        "            break  # le point = fin du nom\n"
        "        ids.append(idx)\n"
        "        resultat += id_to_char[idx]\n"
        "    # Enlever le point de debut\n"
        '    return resultat[1:] if resultat.startswith(".") else resultat\n'
        "\n"
        "\n"
        'print("=== AVANT entrainement (poids aleatoires) ===")\n'
        "print()\n"
        "# Garder les noms pour comparer apres l'entrainement\n"
        "noms_avant = []\n"
        "for _ in range(10):\n"
        "    nom = generer()\n"
        "    noms_avant.append(nom)\n"
        '    print(f"  {nom.capitalize()}")\n'
        "print()\n"
        "print(\"C'est du charabia ! Le modele ne sait pas ce qu'est un Pokemon.\")"
    )
)

# ================================================================
# CELL 14: MD — before exercise 1
# ================================================================
cells.append(md("Teste par toi-meme avec differentes temperatures :"))

# ================================================================
# CELL 15: Exercise 1 (code)
# ================================================================
cells.append(
    code(
        "exercice(\n"
        "    1,\n"
        '    "Genere avant l\'entrainement",\n'
        '    "Change <code>ma_temperature</code> ci-dessous (essaie 0.1 ou 2.0), puis <b>Shift + Entree</b>.",\n'
        '    "C\'est du charabia ! La temperature ne change rien sans entrainement.",\n'
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
        'print(f"Generation AVANT entrainement (temperature = {ma_temperature}) :")\n'
        "print()\n"
        "# Generer 10 noms avec cette temperature\n"
        "for _ in range(10):\n"
        "    nom = generer(temperature=ma_temperature)\n"
        '    print(f"  {nom.capitalize()}")\n'
        "print()\n"
        'print("C\'est du charabia ! Sans entrainement, la temperature ne change rien.")\n'
        "\n"
        "verifier(\n"
        "    1,\n"
        "    ma_temperature != 0.8,\n"
        '    f"Bien joue ! Avec temperature={ma_temperature}, les noms sont "\n'
        "    f\"{'sages' if ma_temperature < 0.5 else 'fous' if ma_temperature > 1.5 else 'equilibres'}.\",\n"
        '    "Change ma_temperature pour une autre valeur, par exemple 0.1 ou 2.0.",\n'
        ")"
    )
)

# ================================================================
# CELL 16: MD — Etape 3: Retropropagation
# ================================================================
cells.append(
    md(
        "---\n"
        "## Etape 3 : La retropropagation\n"
        "\n"
        "Dans les lecons 2 et 3, on calculait les gradients facilement parce que\n"
        "le modele etait simple. Maintenant, notre LLM a **7 couches de calcul** :\n"
        "\n"
        "```\n"
        "emb -> attention -> residuel -> MLP -> residuel -> W_out -> softmax\n"
        "```\n"
        "\n"
        "Pour calculer les gradients, on fait le **chemin inverse** :\n"
        "\n"
        "```\n"
        "softmax -> W_out -> residuel -> MLP -> residuel -> attention -> emb\n"
        "```\n"
        "\n"
        "C'est la **retropropagation** (backpropagation). L'idee :\n"
        "\n"
        "1. On part de l'erreur a la sortie (la loss)\n"
        "2. On remonte couche par couche\n"
        '3. A chaque couche, on calcule "de combien ce poids a contribue a l\'erreur"\n'
        "4. On ajuste chaque poids dans la bonne direction\n"
        "\n"
        "> **Analogie** : Imagine une chaine de dominos. Le dernier domino (la loss)\n"
        "> est tombe trop a droite. Tu remontes la chaine : quel domino a pousse\n"
        "> trop fort ? C'est celui-la qu'on ajuste."
    )
)

# ================================================================
# CELL 17: MD — formule magique
# ================================================================
cells.append(
    md(
        "La formule de depart est **la meme** que dans les lecons 2 et 3 :\n"
        "\n"
        "```\n"
        "gradient[lettre] = proba_predite - (1 si bonne reponse, 0 sinon)\n"
        "```\n"
        "\n"
        "Ensuite, ce gradient se propage en arriere a travers les 7 couches.\n"
        "C'est beaucoup de code (~80 lignes), mais chaque etape est simple :"
    )
)

# ================================================================
# CELL 18: backward function (code)
# ================================================================
cells.append(
    code(
        "def backward(cache, probas, cible):\n"
        '    """Calcule les gradients -- le chemin inverse du forward."""\n'
        "    # On recupere tout ce que le forward avait sauvegarde\n"
        '    hidden = cache["hidden"]\n'
        '    q = cache["q"]\n'
        '    cles = cache["cles"]\n'
        '    valeurs = cache["valeurs"]\n'
        '    poids_attn = cache["poids_attn"]\n'
        '    x_apres_attn = cache["x_apres_attn"]\n'
        '    h1_pre = cache["h1_pre"]\n'
        '    h1 = cache["h1"]\n'
        '    x_final = cache["x_final"]\n'
        '    ids = cache["ids"]\n'
        "    n = len(ids)\n"
        "\n"
        "    # === ETAPE 1 : gradient de la sortie ===\n"
        "    # Meme formule que lecons 2 et 3 !\n"
        "    # Si proba du bon = 0.3 -> gradient = 0.3 - 1 = -0.7 (faut augmenter !)\n"
        "    d_logits = [probas[v] - (1.0 if v == cible else 0.0) for v in range(VOCAB_SIZE)]\n"
        "\n"
        "    # === ETAPE 2 : gradient de W_out ===\n"
        "    # L'erreur se propage de la sortie vers l'interieur du modele\n"
        "    # d_W_out[v][d] = combien W_out[v][d] a contribue a l'erreur\n"
        "    d_W_out = [\n"
        "        [d_logits[v] * x_final[d] for d in range(EMBED_DIM)] for v in range(VOCAB_SIZE)\n"
        "    ]\n"
        "    # d_x = l'erreur propagee vers la couche precedente\n"
        "    d_x = [\n"
        "        sum(d_logits[v] * W_out[v][d] for v in range(VOCAB_SIZE))\n"
        "        for d in range(EMBED_DIM)\n"
        "    ]\n"
        "\n"
        "    # === ETAPE 3 : connexion residuelle 2 ===\n"
        "    # La connexion residuelle copie le gradient dans 2 branches\n"
        "    d_mlp = list(d_x)   # branche MLP\n"
        "    d_xa = list(d_x)    # branche directe (skip connection)\n"
        "\n"
        "    # === ETAPE 4 : backward du MLP ===\n"
        "    # On remonte a travers le reseau de neurones\n"
        "    # Gradient de W2 : combien chaque poids de la couche 2 a contribue\n"
        "    d_W2 = [[d_mlp[d] * h1[j] for j in range(HIDDEN_DIM)] for d in range(EMBED_DIM)]\n"
        "    d_b2 = list(d_mlp)  # gradient du biais = copie directe du gradient\n"
        "    d_h1 = [\n"
        "        sum(d_mlp[d] * W2[d][j] for d in range(EMBED_DIM)) for j in range(HIDDEN_DIM)\n"
        "    ]\n"
        "    # ReLU backward : le gradient passe si h1_pre > 0, sinon bloque\n"
        "    d_h1p = [d_h1[j] * (1.0 if h1_pre[j] > 0 else 0.0) for j in range(HIDDEN_DIM)]\n"
        "    # Gradient de W1 et b1 : meme logique que W2\n"
        "    d_W1 = [\n"
        "        [d_h1p[j] * x_apres_attn[d] for d in range(EMBED_DIM)]\n"
        "        for j in range(HIDDEN_DIM)\n"
        "    ]\n"
        "    d_b1 = list(d_h1p)\n"
        "    # Propager l'erreur du MLP vers la branche directe\n"
        "    for d in range(EMBED_DIM):\n"
        "        d_xa[d] += sum(d_h1p[j] * W1[j][d] for j in range(HIDDEN_DIM))\n"
        "\n"
        "    # === ETAPE 5 : connexion residuelle 1 ===\n"
        "    # Meme principe : le gradient se divise en 2 branches\n"
        "    d_attn_out = list(d_xa)     # branche attention\n"
        "    d_hidden_last = list(d_xa)  # branche directe\n"
        "\n"
        "    # === ETAPE 6 : backward de l'attention ===\n"
        "    # L'erreur remonte vers les query, cles et valeurs\n"
        "    # Gradient des poids d'attention (combien chaque position comptait)\n"
        "    d_pw = [\n"
        "        sum(d_attn_out[d] * valeurs[i][d] for d in range(EMBED_DIM)) for i in range(n)\n"
        "    ]\n"
        "    # Gradient des valeurs (l'info transmise par chaque position)\n"
        "    d_val = [\n"
        "        [d_attn_out[d] * poids_attn[i] for d in range(EMBED_DIM)] for i in range(n)\n"
        "    ]\n"
        "    # Softmax backward : la partie la plus technique\n"
        "    d_sc = [0.0] * n\n"
        "    for i in range(n):\n"
        "        for j in range(n):\n"
        "            if i == j:\n"
        "                d_sc[i] += poids_attn[i] * (1 - poids_attn[i]) * d_pw[i]\n"
        "            else:\n"
        "                d_sc[i] -= poids_attn[j] * poids_attn[i] * d_pw[j]\n"
        "    echelle = math.sqrt(EMBED_DIM)\n"
        "    d_sc = [ds / echelle for ds in d_sc]\n"
        "\n"
        "    # Gradient de la query et des cles\n"
        "    d_q = [sum(d_sc[i] * cles[i][d] for i in range(n)) for d in range(EMBED_DIM)]\n"
        "    d_cles = [[d_sc[i] * q[d] for d in range(EMBED_DIM)] for i in range(n)]\n"
        "\n"
        "    # Gradient de Wq : combien la matrice query a contribue\n"
        "    d_Wq = [\n"
        "        [d_q[r] * hidden[-1][c] for c in range(EMBED_DIM)] for r in range(EMBED_DIM)\n"
        "    ]\n"
        "    for d in range(EMBED_DIM):\n"
        "        d_hidden_last[d] += sum(d_q[r] * Wq[r][d] for r in range(EMBED_DIM))\n"
        "\n"
        "    # Gradients de Wk et Wv : accumules sur toutes les positions\n"
        "    d_Wk = [[0.0] * EMBED_DIM for _ in range(EMBED_DIM)]\n"
        "    d_Wv = [[0.0] * EMBED_DIM for _ in range(EMBED_DIM)]\n"
        "    d_hkv = [[0.0] * EMBED_DIM for _ in range(n)]  # gradient vers les embeddings\n"
        "    for i in range(n):\n"
        "        for r in range(EMBED_DIM):\n"
        "            for c in range(EMBED_DIM):\n"
        "                d_Wk[r][c] += d_cles[i][r] * hidden[i][c]\n"
        "                d_Wv[r][c] += d_val[i][r] * hidden[i][c]\n"
        "                d_hkv[i][c] += d_cles[i][r] * Wk[r][c]\n"
        "                d_hkv[i][c] += d_val[i][r] * Wv[r][c]\n"
        "\n"
        "    # === ETAPE 7 : gradient des embeddings ===\n"
        "    # Finalement, on ajuste la 'fiche d'identite' de chaque lettre\n"
        "    d_tok_emb = [[0.0] * EMBED_DIM for _ in range(VOCAB_SIZE)]\n"
        "    d_pos_emb = [[0.0] * EMBED_DIM for _ in range(n)]\n"
        "    for i in range(n):\n"
        "        d_h = list(d_hkv[i])\n"
        "        if i == n - 1:  # la derniere position recoit aussi le gradient direct\n"
        "            for d in range(EMBED_DIM):\n"
        "                d_h[d] += d_hidden_last[d]\n"
        "        # Repartir entre embedding du token et embedding de position\n"
        "        for d in range(EMBED_DIM):\n"
        "            d_tok_emb[ids[i]][d] += d_h[d]\n"
        "            d_pos_emb[i][d] += d_h[d]\n"
        "\n"
        "    # Retourner tous les gradients (un par matrice de poids)\n"
        "    return {\n"
        '        "d_W_out": d_W_out, "d_W2": d_W2, "d_b2": d_b2,\n'
        '        "d_W1": d_W1, "d_b1": d_b1, "d_Wq": d_Wq,\n'
        '        "d_Wk": d_Wk, "d_Wv": d_Wv,\n'
        '        "d_tok_emb": d_tok_emb, "d_pos_emb": d_pos_emb,\n'
        "    }\n"
        "\n"
        "\n"
        'print("Backward pass defini (7 etapes de retropropagation).")\n'
        'print("  Etape 1 : gradient sortie (cross-entropy)")\n'
        'print("  Etape 2 : gradient W_out")\n'
        'print("  Etape 3 : connexion residuelle 2")\n'
        'print("  Etape 4 : backward MLP (W1, W2, b1, b2)")\n'
        'print("  Etape 5 : connexion residuelle 1")\n'
        'print("  Etape 6 : backward attention (Wq, Wk, Wv)")\n'
        'print("  Etape 7 : gradient embeddings (tok_emb, pos_emb)")'
    )
)

# ================================================================
# CELL 19: MD — Etape 4: Entrainement
# ================================================================
cells.append(
    md(
        "---\n"
        "## Etape 4 : L'entrainement\n"
        "\n"
        "C'est la meme boucle que dans les lecons 2 et 3, mais avec le vrai LLM :\n"
        "\n"
        "1. Prendre un Pokemon\n"
        "2. Pour chaque position, predire la lettre suivante\n"
        "3. Calculer l'erreur (la loss)\n"
        "4. Calculer les gradients (backward)\n"
        "5. Ajuster tous les poids un petit peu (SGD)\n"
        "6. Recommencer\n"
        "\n"
        "> **Cette cellule va tourner pendant ~1-3 minutes.**\n"
        '> Pendant ce temps, lis les sections "En vrai..." plus bas !'
    )
)

# ================================================================
# CELL 20: Training loop (code)
# ================================================================
cells.append(
    code(
        "# NB_EPOCHS : combien de fois le modele voit TOUS les Pokemon\n"
        "NB_EPOCHS = 10\n"
        "# vitesse (learning rate) : de combien on corrige chaque poids\n"
        "vitesse = 0.01\n"
        "\n"
        "# Calculer le nombre total de mises a jour\n"
        "positions_par_mot = sum(len(p) + 1 for p in pokemons) / len(pokemons)\n"
        "total_updates = int(NB_EPOCHS * len(pokemons) * positions_par_mot)\n"
        "\n"
        'print(f"Entrainement : {NB_EPOCHS} epochs x {len(pokemons)} Pokemon")\n'
        'print(f"  ~{total_updates:,} mises a jour des poids au total")\n'
        'print("  (~1-3 minutes, profite pour lire les sections ci-dessous !)")\n'
        "print()\n"
        "\n"
        "# On garde l'historique pour la courbe de loss animee\n"
        "_historique_loss_epochs = []\n"
        "\n"
        "debut_chrono = time.time()  # chronometre pour mesurer la duree\n"
        "\n"
        "for epoch in range(NB_EPOCHS):\n"
        "    # Melanger les Pokemon a chaque epoch (evite les biais d'ordre)\n"
        "    random.shuffle(pokemons)\n"
        "    loss_epoch = 0\n"
        "    nb_epoch = 0\n"
        "\n"
        "    for idx_mot, pokemon in enumerate(pokemons):\n"
        "        # '.pikachu.' -> le modele apprend chaque lettre\n"
        '        mot = "." + pokemon + "."\n'
        "        ids = [char_to_id[c] for c in mot]\n"
        "\n"
        "        # Pour chaque position, predire la lettre suivante\n"
        "        for i in range(1, len(ids)):\n"
        "            seq = ids[:i][-CONTEXT:]  # contexte (max 8 lettres)\n"
        "            cible = ids[i]            # la bonne reponse\n"
        "\n"
        "            # Forward : predire les probabilites de chaque lettre\n"
        "            probas, cache = forward_avec_cache(seq)\n"
        "            loss_epoch += -math.log(probas[cible] + 1e-10)\n"
        "            nb_epoch += 1\n"
        "\n"
        "            # Backward : calculer dans quelle direction corriger\n"
        "            grads = backward(cache, probas, cible)\n"
        "\n"
        "            # SGD : poids -= vitesse * gradient (un petit pas dans la bonne direction)\n"
        "            # Ajuster la couche de sortie\n"
        "            for v in range(VOCAB_SIZE):\n"
        "                for d in range(EMBED_DIM):\n"
        '                    W_out[v][d] -= vitesse * grads["d_W_out"][v][d]\n'
        "            # Ajuster le MLP (W1, b1, W2, b2)\n"
        "            for j in range(HIDDEN_DIM):\n"
        '                b1[j] -= vitesse * grads["d_b1"][j]\n'
        "                for d in range(EMBED_DIM):\n"
        '                    W1[j][d] -= vitesse * grads["d_W1"][j][d]\n'
        "            for d in range(EMBED_DIM):\n"
        '                b2[d] -= vitesse * grads["d_b2"][d]\n'
        "                for j in range(HIDDEN_DIM):\n"
        '                    W2[d][j] -= vitesse * grads["d_W2"][d][j]\n'
        "            # Ajuster l'attention (Wq, Wk, Wv)\n"
        "            for r in range(EMBED_DIM):\n"
        "                for c in range(EMBED_DIM):\n"
        '                    Wq[r][c] -= vitesse * grads["d_Wq"][r][c]\n'
        '                    Wk[r][c] -= vitesse * grads["d_Wk"][r][c]\n'
        '                    Wv[r][c] -= vitesse * grads["d_Wv"][r][c]\n'
        "            # Ajuster les embeddings (seulement les lettres utilisees)\n"
        '            for tok_id in set(cache["ids"]):\n'
        "                for d in range(EMBED_DIM):\n"
        '                    tok_emb[tok_id][d] -= vitesse * grads["d_tok_emb"][tok_id][d]\n'
        "            for pos in range(len(seq)):\n"
        "                for d in range(EMBED_DIM):\n"
        '                    pos_emb[pos % CONTEXT][d] -= vitesse * grads["d_pos_emb"][pos][d]\n'
        "\n"
        "        # Afficher la progression tous les 250 mots\n"
        "        if (idx_mot + 1) % 250 == 0:\n"
        "            t = time.time() - debut_chrono\n"
        "            print(\n"
        '                f"  Epoch {epoch + 1}/{NB_EPOCHS} | Mot {idx_mot + 1:>5}/{len(pokemons)} "\n'
        '                f"| Loss : {loss_epoch / nb_epoch:.3f} | {t:.0f}s"\n'
        "            )\n"
        "\n"
        "    # Sauvegarder la loss moyenne de cette epoch pour la courbe\n"
        "    _historique_loss_epochs.append(loss_epoch / nb_epoch)\n"
        "\n"
        "    t = time.time() - debut_chrono\n"
        "    print(\n"
        '        f"  === Epoch {epoch + 1} terminee | Loss : {loss_epoch / nb_epoch:.3f} | {t:.0f}s ==="\n'
        "    )\n"
        "    print()\n"
        "\n"
        "duree = time.time() - debut_chrono\n"
        'print(f"Entrainement termine en {duree:.0f} secondes !")\n'
        'print(f"Loss : {loss_initiale:.3f} -> {loss_epoch / nb_epoch:.3f}")\n'
        "\n"
        "# Courbe de loss animee\n"
        "afficher_evolution_loss(\n"
        '    _historique_loss_epochs, titre="Evolution de la loss par epoch"\n'
        ")"
    )
)

# ================================================================
# CELL 21: MD — observation after training
# ================================================================
cells.append(
    md(
        "**La loss a baisse !** Le modele a appris des patterns dans les noms de Pokemon.\n"
        "\n"
        "---"
    )
)

# ================================================================
# CELL 22: Exercise 2 (code)
# ================================================================
cells.append(
    code(
        "exercice(\n"
        "    2,\n"
        '    "Observe l\'entrainement",\n'
        '    "Observe les resultats ci-dessous. La loss a-t-elle baisse ?",\n'
        '    "La loss baisse = le modele s\'ameliore.",\n'
        ")\n"
        "\n"
        "# \u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557\n"
        "# \u2551  A TOI DE JOUER !                    \u2551\n"
        "# \u2560\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2563\n"
        "\n"
        "# (Re-execute la cellule d'entrainement ci-dessus\n"
        "#  en changeant NB_EPOCHS ou vitesse)\n"
        "\n"
        "# \u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d\n"
        "\n"
        "# Resume de l'entrainement\n"
        'print("Resultats de l\'entrainement :")\n'
        'print(f"  Epochs : {NB_EPOCHS}")\n'
        'print(f"  Vitesse : {vitesse}")\n'
        'print(f"  Duree totale : {duree:.0f} secondes ({duree / NB_EPOCHS:.0f}s par epoch)")\n'
        'print(f"  Loss initiale : {loss_initiale:.3f}")\n'
        'print(f"  Loss finale : {loss_epoch / nb_epoch:.3f}")\n'
        'print(f"  Amelioration : {(1 - (loss_epoch / nb_epoch) / loss_initiale) * 100:.0f}%")\n'
        "print()\n"
        "# loss < 2.5 = le modele a bien appris les patterns Pokemon\n"
        "if loss_epoch / nb_epoch < 2.5:\n"
        '    print("Le modele a bien appris !")\n'
        "else:\n"
        "    print(\"Le modele peut encore s'ameliorer. Essaie plus d'epochs !\")\n"
        "\n"
        "verifier(\n"
        "    2,\n"
        "    loss_epoch / nb_epoch < loss_initiale,\n"
        '    f"Bien observe ! La loss est passee de {loss_initiale:.2f} a {loss_epoch / nb_epoch:.2f} en {NB_EPOCHS} epochs.",\n'
        "    \"Re-execute l'entrainement si la loss n'a pas baisse.\",\n"
        ")"
    )
)

# ================================================================
# CELL 23: MD — En vrai (autograd, GPU, Adam)
# ================================================================
cells.append(
    md(
        "---\n"
        "## En vrai... pendant que le modele s'entraine\n"
        "\n"
        "### Autograd vs notre backward manuel\n"
        "\n"
        "On a ecrit ~80 lignes de code pour le backward pass. C'est beaucoup !\n"
        "\n"
        "En vrai, les frameworks comme **PyTorch** font ca **automatiquement**.\n"
        "Tu ecris juste le forward pass, et PyTorch calcule les gradients tout seul.\n"
        "Ca s'appelle **l'autograd** (differentiation automatique).\n"
        "\n"
        "### GPU vs CPU\n"
        "\n"
        "Notre boucle Python fait les calculs **un par un**.\n"
        "Un **GPU** peut faire **des milliers de multiplications en parallele**.\n"
        "C'est comme la difference entre :\n"
        "- Un cuisinier qui prepare les plats un par un (CPU)\n"
        "- Une brigade de 1000 cuisiniers qui preparent tous en meme temps (GPU)\n"
        "\n"
        "GPT-4 a utilise **25 000 GPU** pendant **plusieurs mois**.\n"
        "\n"
        "### Adam vs SGD\n"
        "\n"
        "On utilise **SGD** (la descente de gradient la plus simple).\n"
        "**Adam** est plus intelligent :\n"
        "- Il **accelere** dans les zones plates\n"
        "- Il **freine** dans les zones pentues\n"
        "- C'est comme un velo avec des vitesses !"
    )
)

# ================================================================
# CELL 24: MD — Ce qu'on n'a pas implemente
# ================================================================
cells.append(
    md(
        "---\n"
        "## Ce qu'on n'a pas implemente\n"
        "\n"
        "| Technique | Notre mini-LLM | Les vrais LLM |\n"
        "|-----------|----------------|---------------|\n"
        "| **Batching** | 1 mot a la fois | 64-512 mots en parallele |\n"
        "| **LayerNorm** | Non | Oui (stabilise l'entrainement) |\n"
        "| **Dropout** | Non | Oui (evite le sur-apprentissage) |\n"
        "| **Multi-head** | 1 tete | 4-96 tetes en parallele |\n"
        "| **Multi-couches** | 1 couche | 6-96 couches empilees |\n"
        "| **Optimizer** | SGD basique | Adam (plus intelligent) |\n"
        "| **GPU** | Non (Python pur) | Oui (1000x plus rapide) |\n"
        "\n"
        "Mais l'**algorithme** est le meme ! La difference, c'est l'**echelle**."
    )
)

# ================================================================
# CELL 25: MD — generation apres
# ================================================================
cells.append(
    md(
        "---\n"
        "## Le resultat : generation apres entrainement\n"
        "\n"
        "Voyons si le modele a appris a generer des noms de Pokemon :"
    )
)

# ================================================================
# CELL 26: Generation apres + comparaison (code)
# ================================================================
cells.append(
    code(
        "# Generer 10 noms avec le modele entraine\n"
        'print("=== APRES entrainement ===")\n'
        "print()\n"
        "noms_apres = []\n"
        "for _ in range(10):\n"
        "    nom = generer(temperature=0.8)\n"
        "    noms_apres.append(nom)\n"
        '    print(f"  {nom.capitalize()}")\n'
        "\n"
        "# Animation : le meilleur nom apparait lettre par lettre\n"
        "print()\n"
        "afficher_generation(noms_apres[0].capitalize())\n"
        "\n"
        "# Comparaison cote a cote : avant vs apres\n"
        "print()\n"
        "afficher_comparaison(noms_avant[:8], noms_apres[:8])\n"
        "\n"
        "# Predictions apres entrainement\n"
        "# Que predit le modele apres '.pik' ? (il devrait predire 'a' pour pikachu)\n"
        '_probas_post, _ = forward_avec_cache([char_to_id[c] for c in ".pik"][-CONTEXT:])\n'
        "# Trier par probabilite decroissante et garder les 5 meilleurs\n"
        "_top = sorted(range(VOCAB_SIZE), key=lambda i: -_probas_post[i])[:5]\n"
        "afficher_barres(\n"
        "    [_probas_post[i] for i in _top],\n"
        "    [id_to_char[i] for i in _top],\n"
        "    titre=\"Top 5 predictions apres '.pik' (apres entrainement)\",\n"
        ")"
    )
)

# ================================================================
# CELL 27: MD — before exercise 3
# ================================================================
cells.append(md("Explore le modele entraine par toi-meme :"))

# ================================================================
# CELL 28: Exercise 3 (code)
# ================================================================
cells.append(
    code(
        "exercice(\n"
        "    3,\n"
        '    "Explore le modele entraine",\n'
        "    'Change <code>ma_temperature</code> et/ou <code>mon_debut</code> ci-dessous '\n"
        '    \'(essaie <code>".pik"</code>, <code>".bul"</code>).\',\n'
        '    "Compare avec l\'exercice 1 : maintenant ca ressemble a des Pokemon !",\n'
        ")\n"
        "\n"
        "# \u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557\n"
        "# \u2551  A TOI DE JOUER !                    \u2551\n"
        "# \u2560\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2563\n"
        "\n"
        "ma_temperature = 0.8  # <-- Essaie 0.1 (sage) ou 2.0 (fou) !\n"
        'mon_debut = "."       # <-- Essaie ".pik", ".bul" ou ".dra" !\n'
        "\n"
        "# \u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d\n"
        "\n"
        "print(\n"
        '    f"Generation APRES entrainement (temperature={ma_temperature}, "\n'
        "    f\"debut='{mon_debut}') :\"\n"
        ")\n"
        "print()\n"
        "# Generer 15 noms avec les parametres choisis\n"
        "for _ in range(15):\n"
        "    nom = generer(debut=mon_debut, temperature=ma_temperature)\n"
        '    print(f"  {nom.capitalize()}")\n'
        "print()\n"
        "# Compare avec l'exercice 1 : avant, c'etait du charabia !\n"
        "print(\"Compare avec l'exercice 1 : maintenant le modele sait ce qu'est un Pokemon !\")\n"
        "\n"
        "verifier(\n"
        "    3,\n"
        '    ma_temperature != 0.8 or mon_debut != ".",\n'
        "    f\"Genial ! Generation avec temperature={ma_temperature} et debut='{mon_debut}'.\",\n"
        '    "Change ma_temperature ou mon_debut pour explorer le modele entraine.",\n'
        ")"
    )
)

# ================================================================
# CELL 29: MD — Ce qu'on a appris
# ================================================================
cells.append(
    md(
        "---\n"
        "## Ce qu'on a appris\n"
        "\n"
        "```\n"
        "Lecon 1 : Compter les lettres qui suivent        -> bigramme\n"
        "Lecon 2 : Apprendre de ses erreurs               -> entrainement\n"
        "Lecon 3 : Regarder plusieurs lettres en arriere   -> embeddings + contexte\n"
        "Lecon 4 : Choisir les lettres importantes          -> attention\n"
        "Lecon 5 : Assembler le tout                       -> mini-LLM\n"
        "Lecon 6 : Entrainer pour de vrai                  -> retropropagation !\n"
        "```\n"
        "\n"
        "### Ce qu'on a fait dans cette lecon\n"
        "\n"
        "1. **Charge ~1 000 noms de Pokemon**\n"
        "2. **Implemente la retropropagation** : 7 etapes pour remonter les gradients\n"
        "3. **Entraine le mini-LLM** avec la descente de gradient (SGD)\n"
        "4. **Genere des noms de Pokemon inventes** qui ressemblent a de vrais Pokemon\n"
        "\n"
        "### Ce qu'on a appris\n"
        "\n"
        "- La **retropropagation** remonte l'erreur couche par couche\n"
        "- L'**entrainement** = repeter forward + backward + mise a jour des poids\n"
        "- Meme un modele de ~2 800 parametres peut **apprendre des patterns**\n"
        "- La difference avec ChatGPT n'est pas l'algorithme, c'est **l'echelle**\n"
        "\n"
        "---\n"
        "*Tu as construit et entraine ton propre LLM. Felicitations !*"
    )
)

# ================================================================
# CELL 30: Sources (markdown)
# ================================================================
cells.append(
    md(
        "---\n"
        "\n"
        "### Sources (ISO 42001)\n"
        "\n"
        "- **Retropropagation et descente de gradient** : [microgpt.py](https://gist.github.com/karpathy/8627fe009c40f57531cb18360106ce95) \\u2014 Andrej Karpathy, implementation complete du backward pass\n"
        '- **Architecture GPT (embedding + attention + MLP)** : [Video "Let\'s build GPT"](https://www.youtube.com/watch?v=kCc8FmEb1nY) \\u2014 Andrej Karpathy (2023)\n'
        "- **Cross-entropy loss et gradient softmax** : [3Blue1Brown - Neural Networks](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi) \\u2014 Grant Sanderson\n"
        '- **"Attention Is All You Need"** : Vaswani et al., 2017, [arXiv:1706.03762](https://arxiv.org/abs/1706.03762)\n'
        "- **Donnees d'entrainement** : [PokeAPI](https://pokeapi.co/) \\u2014 (c) Nintendo / Creatures Inc. / GAME FREAK inc., usage educatif uniquement"
    )
)

# ================================================================
# Write notebook
# ================================================================
nb["cells"] = cells
with open("notebooks/06_entrainer_le_modele.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"NB06 rebuilt: {len(cells)} cells (was 18)")
