#!/usr/bin/env python3
"""Refactor NB01: Deviner la suite — pedagogical overhaul.

Reads the existing notebook, extracts reusable parts (verifier, exercice),
rewrites with interactive visualizations, box-drawing delimiters, and
markdown before every code cell.
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
with open("notebooks/01_deviner_la_suite.ipynb", encoding="utf-8") as f:
    nb = json.load(f)

# Extract original cell-1 source (verifier + exercice functions)
original_cell1_lines = nb["cells"][1]["source"]
original_cell1 = "".join(original_cell1_lines)

# Extract verifier function (from "def verifier" to next "def " or blank line pattern)
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
# CELL: Intro (markdown)
# ----------------------------------------------------------------
cells.append(
    md(
        "# Lecon 1 : Deviner la suite\n"
        "\n"
        "> **Bienvenue !** Ce notebook est interactif : tu vas lire,\n"
        "> executer du code, et ecrire tes propres lignes de Python.\n"
        "\n"
        "### Comment ca marche ?\n"
        "\n"
        "1. Clique sur une cellule grise (c'est du code Python)\n"
        "2. Appuie sur **Shift + Entree** pour l'executer\n"
        "3. Le resultat s'affiche juste en dessous\n"
        "4. Passe a la cellule suivante et recommence !\n"
        "\n"
        "**Regle d'or** : execute les cellules **dans l'ordre**, de haut en bas.\n"
        "Si tu sautes une cellule, la suivante risque de ne pas marcher.\n"
        "\n"
        "---"
    )
)

# ----------------------------------------------------------------
# CELL: Infrastructure (code) — with interactive visualizations
# ----------------------------------------------------------------
# Build the infrastructure cell by combining:
# 1. Header comment
# 2. Imports (add json, uuid for interactive viz)
# 3. Original verifier + exercice
# 4. New interactive viz functions

infra_source = (
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
    "_NB_TOTAL = 4\n"
    "\n"
    "\n" + verifier_code + "\n"
    "\n"
    "\n" + exercice_code + "\n"
    "\n"
    "\n"
    # afficher_heatmap — interactive
    'def afficher_heatmap(compteur, titre="Heatmap des bigrammes"):\n'
    '    """Heatmap interactive des bigrammes (survol = detail, highlight ligne/colonne)."""\n'
    "    uid = uuid.uuid4().hex[:8]\n"
    "    lettres = sorted(\n"
    "        set(k for k in compteur) | set(s for v in compteur.values() for s in v)\n"
    "    )\n"
    "    max_count = max(\n"
    "        (c for v in compteur.values() for c in v.values()), default=1\n"
    "    )\n"
    "    # En-tete du tableau\n"
    '    header = "".join(\n'
    "        f'<th style=\"padding:2px 4px;font-size:0.75em\">{ch}</th>'\n"
    "        for ch in lettres\n"
    "    )\n"
    "    # Lignes de donnees avec data-attributes pour le JS\n"
    '    rows = ""\n'
    "    for i, l1 in enumerate(lettres):\n"
    '        cells = ""\n'
    "        for j, l2 in enumerate(lettres):\n"
    "            count = compteur.get(l1, {}).get(l2, 0)\n"
    "            opacity = count / max_count if max_count > 0 else 0\n"
    '            bg = f"rgba(21,101,192,{opacity:.2f})"\n'
    "            cells += (\n"
    '                f\'<td data-r="{i}" data-c="{j}" data-v="{count}"\'\n'
    "                f' style=\"padding:2px 4px;background:{bg};text-align:center;'\n"
    "                f'font-size:0.65em;border:1px solid #eee;min-width:16px;'\n"
    '                f\'cursor:crosshair">{count if count > 0 else ""}</td>\'\n'
    "            )\n"
    "        rows += f'<tr><th style=\"padding:2px 4px;font-size:0.75em\">{l1}</th>{cells}</tr>'\n"
    "    lettres_js = json.dumps(lettres)\n"
    '    hint = "Survole une case pour voir le detail"\n'
    "    # HTML + JS interactif (hover = highlight ligne/colonne + info)\n"
    "    display(HTML(\n"
    "        f'<!-- tuto-viz -->'\n"
    "        f'<div style=\"margin:8px 0;overflow-x:auto\"><b>{titre}</b>'\n"
    '        f\'<table id="t{uid}" style="border-collapse:collapse;margin-top:4px">\'\n'
    "        f'<tr><th></th>{header}</tr>{rows}</table>'\n"
    '        f\'<div id="i{uid}" style="margin-top:4px;color:#555;font-size:0.85em;\'\n'
    "        f'min-height:1.3em\">{hint}</div></div>'\n"
    "        f'<script>(function(){{\"use strict\";'\n"
    "        f'var t=document.getElementById(\"t{uid}\"),'\n"
    "        f'info=document.getElementById(\"i{uid}\"),'\n"
    "        f'L={lettres_js};'\n"
    "        f'function hl(r,c){{t.querySelectorAll(\"td[data-r]\").forEach(function(d){{'\n"
    "        f'var a=+d.dataset.r===r||+d.dataset.c===c;'\n"
    '        f\'d.style.outline=a?"2px solid #1565c0":"";\'\n'
    '        f\'d.style.position=a?"relative":""}});}};\'\n'
    "        f't.addEventListener(\"mouseover\",function(e){{'\n"
    "        f'var d=e.target.closest(\"td[data-r]\");if(!d)return;'\n"
    "        f'var r=+d.dataset.r,c=+d.dataset.c;hl(r,c);'\n"
    '        f\'info.textContent=L[r]+" \\u2192 "+L[c]+" : "+d.dataset.v+" fois"}});\'\n'
    "        f't.addEventListener(\"mouseleave\",function(){{hl(-1,-1);'\n"
    "        f'info.textContent=\"{hint}\"}})'\n"
    "        f'}})();</script>'\n"
    "    ))\n"
    "\n"
    "\n"
    # afficher_barres — animated
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
    # afficher_generation — letter by letter animation
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

cells.append(code(infra_source))

# ----------------------------------------------------------------
# CELL: Comment une IA "devine" (markdown)
# ----------------------------------------------------------------
cells.append(
    md(
        '## Comment une IA "devine" le mot suivant ?\n'
        "\n"
        "Quand tu ecris un message sur ton telephone, il te **propose** le mot suivant.\n"
        "Comment fait-il ? Il a appris quels mots viennent souvent apres d'autres.\n"
        "\n"
        "On va faire pareil, mais avec des **lettres** au lieu de mots.\n"
        "\n"
        "Par exemple, pense a ces suites :\n"
        "- **A, B, C** \\u2192 quelle est la suite ? **D** (l'alphabet !)\n"
        "- **L, U, N, D** \\u2192 quelle est la suite ? **I** (les jours de la semaine)\n"
        "- **Q** \\u2192 quelle lettre vient presque toujours apres ? ..."
    )
)

# ----------------------------------------------------------------
# CELL: Exercise 1 — Q -> U (code)
# ----------------------------------------------------------------
cells.append(
    code(
        "exercice(\n"
        "    1,\n"
        '    "Quelle lettre suit Q ?",\n'
        '    "Change <code>ma_reponse</code> ci-dessous, puis <b>Shift + Entree</b>. Quelle lettre vient presque toujours apres Q ?",\n'
        '    "Si ta reponse est bonne, la box passe au vert.",\n'
        ")\n"
        "\n"
        "# --- Code de preparation (ne touche pas) ---\n"
        'print("Reponses :")\n'
        'print("  A, B, C -> D  (l\'alphabet !)")\n'
        'print("  L, U, N, D -> I  (les jours : Lundi)")\n'
        "\n"
        "# \u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557\n"
        "# \u2551  A TOI DE JOUER !                    \u2551\n"
        "# \u2560\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2563\n"
        "\n"
        'ma_reponse = "?"  # <-- Quelle lettre vient apres Q ?\n'
        "\n"
        "# \u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d\n"
        "\n"
        'print(f"  Q -> {ma_reponse.upper()}  (ta reponse !)")\n'
        "\n"
        "# Validation exercice 1\n"
        "verifier(\n"
        "    1,\n"
        '    ma_reponse.lower() == "u",\n'
        '    "Bravo ! Apres Q vient presque toujours U.",\n'
        '    "Pas tout a fait... quelle lettre vient presque toujours apres Q ?",\n'
        ")"
    )
)

# ----------------------------------------------------------------
# CELL: Transition — charger les Pokemon (markdown)
# ----------------------------------------------------------------
cells.append(
    md(
        "---\n"
        "## Etape 1 : Charger nos Pokemon\n"
        "\n"
        "On va prendre une liste de noms de Pokemon et compter quelle lettre\n"
        "vient apres quelle autre. Ces 20 noms sont notre **dataset**\n"
        "(les donnees d'entrainement).\n"
        "\n"
        "Execute la cellule ci-dessous pour charger nos 20 Pokemon :"
    )
)

# ----------------------------------------------------------------
# CELL: Load Pokemon list (code)
# ----------------------------------------------------------------
cells.append(
    code(
        '# Nos 20 Pokemon : le "dataset" de cette lecon\n'
        "pokemons = [\n"
        '    "arcanin",     # 7 lettres\n'
        '    "bulbizarre",  # 10 lettres\n'
        '    "carapuce",    # 8 lettres\n'
        '    "dracaufeu",   # 9 lettres\n'
        '    "ectoplasma",  # 10 lettres\n'
        '    "evoli",       # 5 lettres\n'
        '    "felinferno",  # 10 lettres\n'
        '    "gardevoir",   # 9 lettres\n'
        '    "goupix",      # 6 lettres\n'
        '    "lokhlass",    # 8 lettres\n'
        '    "lucario",     # 7 lettres\n'
        '    "metamorph",   # 9 lettres\n'
        '    "mewtwo",      # 6 lettres\n'
        '    "noctali",     # 7 lettres\n'
        '    "pikachu",     # 7 lettres\n'
        '    "rondoudou",   # 9 lettres\n'
        '    "ronflex",     # 7 lettres\n'
        '    "salameche",   # 9 lettres\n'
        '    "togepi",      # 6 lettres\n'
        '    "voltali",     # 7 lettres\n'
        "]\n"
        "\n"
        'print(f"On a {len(pokemons)} Pokemon pour apprendre.")\n'
        "print()\n"
        'print("Les 5 premiers :", pokemons[:5])'
    )
)

# ----------------------------------------------------------------
# CELL: Intro exercise 2 (markdown)
# ----------------------------------------------------------------
cells.append(md("Explore un peu cette liste avant de continuer :"))

# ----------------------------------------------------------------
# CELL: Exercise 2 — explore list (code)
# ----------------------------------------------------------------
cells.append(
    code(
        "exercice(\n"
        "    2,\n"
        '    "Explore la liste de Pokemon",\n'
        "    'Complete les variables ci-dessous avec <code>pokemons[-1]</code> et <code>len(\"bulbizarre\")</code>.',\n"
        '    "Tu vas voir le dernier Pokemon et le nombre de lettres.",\n'
        ")\n"
        "\n"
        "# --- Code de preparation (ne touche pas) ---\n"
        "# pokemons[-1] donne le dernier element d'une liste\n"
        '# len("mot") donne le nombre de lettres\n'
        "\n"
        "# \u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557\n"
        "# \u2551  A TOI DE JOUER !                    \u2551\n"
        "# \u2560\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2563\n"
        "\n"
        "dernier_pokemon = ...  # <-- Ecris pokemons[-1]\n"
        'nb_lettres = ...       # <-- Ecris len("bulbizarre")\n'
        "\n"
        "# \u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d\n"
        "\n"
        'print(f"Le dernier Pokemon est : {dernier_pokemon}")\n'
        "print(f\"'bulbizarre' a {nb_lettres} lettres\")\n"
        "\n"
        "# Validation exercice 2\n"
        "verifier(\n"
        "    2,\n"
        "    isinstance(dernier_pokemon, str)\n"
        "    and isinstance(nb_lettres, int)\n"
        "    and dernier_pokemon == pokemons[-1]\n"
        '    and nb_lettres == len("bulbizarre"),\n'
        "    f\"Bravo ! {dernier_pokemon} est le dernier, et 'bulbizarre' a {nb_lettres} lettres.\",\n"
        "    \"Remplace les ... par pokemons[-1] et len('bulbizarre').\",\n"
        ")"
    )
)

# ----------------------------------------------------------------
# CELL: Transition — bigrammes (markdown)
# ----------------------------------------------------------------
cells.append(
    md(
        "---\n"
        "## Etape 2 : Compter les paires de lettres (bigrammes)\n"
        "\n"
        "Maintenant, on va compter **quelle lettre vient apres quelle autre**.\n"
        'Par exemple, dans "pikachu" :\n'
        '- apres "p" vient "i"\n'
        '- apres "i" vient "k"\n'
        '- apres "k" vient "a"\n'
        "- ...\n"
        "\n"
        "On utilise un **point** `.` pour marquer le debut et la fin :\n"
        '`.pikachu.` signifie "le nom commence et finit ici".\n'
        "\n"
        "Ces paires de lettres s'appellent des **bigrammes** :"
    )
)

# ----------------------------------------------------------------
# CELL: Count bigrammes + heatmap (code)
# ----------------------------------------------------------------
cells.append(
    code(
        "from collections import Counter\n"
        "\n"
        "# Comptons : apres chaque lettre, quelle lettre vient ensuite ?\n"
        "compteur = {}\n"
        "\n"
        "for pokemon in pokemons:\n"
        '    mot = "." + pokemon + "."       # ex: ".pikachu."\n'
        "    for i in range(len(mot) - 1):\n"
        "        lettre_actuelle = mot[i]    # la lettre courante\n"
        "        lettre_suivante = mot[i + 1]  # celle juste apres\n"
        "        if lettre_actuelle not in compteur:\n"
        "            compteur[lettre_actuelle] = Counter()\n"
        "        compteur[lettre_actuelle][lettre_suivante] += 1\n"
        "\n"
        "# Que vient-il apres la lettre 'a' ?\n"
        "print(\"Apres la lettre 'a', on trouve :\")\n"
        'for lettre, nb in compteur["a"].most_common():\n'
        "    print(f\"  '{lettre}' -> {nb} fois\")\n"
        "\n"
        "print()\n"
        'print("Visualisation interactive (survole les cases) :")\n'
        "\n"
        "# Heatmap interactive : survole pour voir le detail\n"
        'afficher_heatmap(compteur, titre="Heatmap : quelle lettre suit quelle autre ?")'
    )
)

# ----------------------------------------------------------------
# CELL: Observation after heatmap (markdown)
# ----------------------------------------------------------------
cells.append(
    md(
        "**Qu'est-ce que tu remarques ?**\n"
        "\n"
        "- Quelles paires de lettres sont les plus frequentes (cases foncees) ?\n"
        "- Est-ce que certaines lettres ne se suivent jamais (cases vides) ?\n"
        "- Regarde la ligne du `.` (debut de mot) : quelles lettres commencent les noms ?\n"
        "\n"
        "---"
    )
)

# ----------------------------------------------------------------
# CELL: Exercise 3 — explore pairs (code)
# ----------------------------------------------------------------
cells.append(
    code(
        "exercice(\n"
        "    3,\n"
        '    "Explore les paires de lettres",\n'
        '    \'Change <code>ma_lettre</code> ci-dessous (essaie <code>"p"</code>, <code>"."</code> ou ta lettre preferee).\',\n'
        '    "Les comptages changent selon la lettre choisie.",\n'
        ")\n"
        "\n"
        "# \u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557\n"
        "# \u2551  A TOI DE JOUER !                    \u2551\n"
        "# \u2560\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2563\n"
        "\n"
        'ma_lettre = "a"  # <-- Change cette lettre !\n'
        "\n"
        "# \u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d\n"
        "\n"
        "print(f\"Apres la lettre '{ma_lettre}', on trouve :\")\n"
        "for lettre, nb in compteur[ma_lettre].most_common():\n"
        "    print(f\"  '{lettre}' -> {nb} fois\")\n"
        "\n"
        "# Validation exercice 3\n"
        "verifier(\n"
        "    3,\n"
        '    ma_lettre != "a",\n'
        "    f\"Bien joue ! Tu as explore les suites de '{ma_lettre}'.\",\n"
        "    \"Change ma_lettre pour une autre lettre, par exemple 'p' ou '.'.\",\n"
        ")"
    )
)

# ----------------------------------------------------------------
# CELL: Transition — probabilites (markdown)
# ----------------------------------------------------------------
cells.append(
    md(
        "---\n"
        "## Etape 3 : Transformer les comptes en probabilites\n"
        "\n"
        "Au lieu de dire \"la lettre 'r' vient 3 fois apres 'a'\",\n"
        "on veut dire \"il y a 25% de chances que 'r' vienne apres 'a'\".\n"
        "\n"
        "C'est ce qu'on appelle une **probabilite** : un nombre entre 0% et 100%\n"
        'qui dit "a quel point c\'est probable".\n'
        "\n"
        "On divise chaque compte par le total :"
    )
)

# ----------------------------------------------------------------
# CELL: Compute probas + barres (code)
# ----------------------------------------------------------------
cells.append(
    code(
        "# Transformer les comptes en probabilites\n"
        "probas = {}\n"
        "\n"
        "for lettre, suivantes in compteur.items():\n"
        "    total = sum(suivantes.values())  # nombre total de suites observees\n"
        "    probas[lettre] = {}\n"
        "    for suivante, nb in suivantes.items():\n"
        "        probas[lettre][suivante] = nb / total  # compte / total = probabilite\n"
        "\n"
        "# Affichons les probabilites apres 'a'\n"
        "print(\"Probabilites apres 'a' :\")\n"
        'for lettre, p in sorted(probas["a"].items(), key=lambda x: -x[1]):\n'
        '    barre = "#" * int(p * 40)  # barre proportionnelle\n'
        "    print(f\"  '{lettre}' : {p:.0%} {barre}\")\n"
        "\n"
        "# Barres animees : les 8 lettres les plus probables apres 'a'\n"
        '_top = sorted(probas["a"].items(), key=lambda x: -x[1])[:8]\n'
        "afficher_barres(\n"
        "    [v for _, v in _top], [k for k, _ in _top], titre=\"Probabilites apres 'a'\"\n"
        ")"
    )
)

# ----------------------------------------------------------------
# CELL: Transition — generation (markdown)
# ----------------------------------------------------------------
cells.append(
    md(
        "---\n"
        "## Etape 4 : Generer un nom de Pokemon !\n"
        "\n"
        "Maintenant on peut **inventer** un nom de Pokemon :\n"
        "1. On part du debut (le point `.`)\n"
        "2. On choisit la lettre suivante au hasard, en respectant les probabilites\n"
        "3. On recommence jusqu'a tomber sur un point `.` (fin du nom)\n"
        "\n"
        "C'est exactement comme ca que ChatGPT fonctionne, mais avec des **mots**\n"
        "au lieu de lettres, et des milliards de parametres au lieu de 20 Pokemon."
    )
)

# ----------------------------------------------------------------
# CELL: Generate function + demo (code)
# ----------------------------------------------------------------
cells.append(
    code(
        "import random\n"
        "\n"
        "\n"
        "def generer_pokemon(probas):\n"
        '    """Genere un nom de Pokemon lettre par lettre."""\n'
        '    nom = ""\n'
        '    lettre = "."  # on commence au debut\n'
        "\n"
        "    while True:\n"
        "        # Choisir la lettre suivante selon les probabilites\n"
        "        choix = list(probas[lettre].keys())   # lettres possibles\n"
        "        poids = list(probas[lettre].values()) # leurs probabilites\n"
        "        lettre = random.choices(choix, weights=poids, k=1)[0]\n"
        "\n"
        '        if lettre == ".":  # fin du nom\n'
        "            break\n"
        "        nom += lettre\n"
        "\n"
        "    return nom\n"
        "\n"
        "\n"
        "# Generons 10 noms de Pokemon !\n"
        'print("Noms de Pokemon inventes par notre modele :")\n'
        "print()\n"
        "noms_generes = []\n"
        "for i in range(10):\n"
        "    nom = generer_pokemon(probas)\n"
        "    noms_generes.append(nom)\n"
        '    print(f"  {i + 1}. {nom.capitalize()}")\n'
        "\n"
        "# Animation du dernier nom genere\n"
        "print()\n"
        'print("Animation du dernier nom genere :")\n'
        "afficher_generation(noms_generes[-1].capitalize(), delai_ms=300)"
    )
)

# ----------------------------------------------------------------
# CELL: Observation after generation (markdown)
# ----------------------------------------------------------------
cells.append(
    md(
        "**Qu'est-ce que tu remarques ?**\n"
        "\n"
        "- Les noms generes ressemblent-ils a des Pokemon ?\n"
        "- Certains sont tres courts (1-2 lettres). Pourquoi ?\n"
        "- Le modele ne regarde que **1 lettre en arriere**. Il ne sait pas\n"
        '  que "Pik" est un bon debut de Pokemon.\n'
        "\n"
        "Re-execute la cellule au-dessus pour generer d'autres noms !\n"
        "\n"
        "---"
    )
)

# ----------------------------------------------------------------
# CELL: Exercise 4 — generate many (code)
# ----------------------------------------------------------------
cells.append(
    code(
        "exercice(\n"
        "    4,\n"
        '    "Genere plein de Pokemon !",\n'
        '    "Change <code>nombre</code> ci-dessous (essaie 50 ou 100).",\n'
        '    "Plus tu en generes, plus tu verras de noms droles.",\n'
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
        "for i in range(nombre):\n"
        '    print(f"  {i + 1}. {generer_pokemon(probas).capitalize()}")\n'
        "\n"
        "# Validation exercice 4\n"
        "verifier(\n"
        "    4,\n"
        "    nombre != 10,\n"
        '    f"Genial ! Tu as genere {nombre} Pokemon.",\n'
        '    "Change nombre pour une autre valeur, par exemple 50.",\n'
        ")"
    )
)

# ----------------------------------------------------------------
# CELL: Post-exercise reflection (markdown)
# ----------------------------------------------------------------
cells.append(
    md(
        "**Les noms ressemblent-ils a des Pokemon ? Pourquoi ?**\n"
        "\n"
        "Notre modele a appris les **paires de lettres** frequentes dans les noms\n"
        'de Pokemon. Alors les noms generes "sonnent" un peu comme du Pokemon...\n'
        "mais pas toujours, parce qu'il ne regarde qu'**une seule lettre en arriere**.\n"
        "\n"
        "---"
    )
)

# ----------------------------------------------------------------
# CELL: Conclusion (markdown)
# ----------------------------------------------------------------
cells.append(
    md(
        "## Ce qu'on a appris\n"
        "\n"
        "- Un modele de langage **predit la suite** en se basant sur ce qu'il a vu avant\n"
        "- Il utilise des **probabilites** : certaines lettres sont plus probables que d'autres\n"
        '- Meme un modele tres simple peut generer des noms qui "sonnent" bien\n'
        "\n"
        "### Le probleme de notre modele\n"
        "\n"
        "Notre modele ne regarde que **1 lettre en arriere**. Il ne sait pas que\n"
        '"Pik" est un bon debut de Pokemon, parce qu\'il ne voit que la derniere lettre.\n'
        "\n"
        "Dans la prochaine lecon, on va lui apprendre a **s'ameliorer quand il se trompe**.\n"
        "\n"
        "---\n"
        "*Prochaine lecon : [02 - Apprendre de ses erreurs](02_apprendre_des_erreurs.ipynb)*"
    )
)

# ----------------------------------------------------------------
# CELL: Sources (markdown)
# ----------------------------------------------------------------
cells.append(
    md(
        "---\n"
        "\n"
        "### Sources (ISO 42001)\n"
        "\n"
        "- **Concept de bigrammes et modeles de langage** : [microgpt.py](https://gist.github.com/karpathy/8627fe009c40f57531cb18360106ce95) -- Andrej Karpathy\n"
        '- **Approche pedagogique character-level** : [Video "Let\'s build GPT"](https://www.youtube.com/watch?v=kCc8FmEb1nY) -- Andrej Karpathy (2023)\n'
        "- **Visualisation des reseaux de neurones** : [3Blue1Brown - Neural Networks](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi) -- Grant Sanderson\n"
        "- **Dataset Pokemon** : (c) Nintendo / Creatures Inc. / GAME FREAK inc., usage educatif. Source : [PokeAPI](https://pokeapi.co/)"
    )
)

# ================================================================
# Write notebook
# ================================================================
nb["cells"] = cells
with open("notebooks/01_deviner_la_suite.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"NB01 rebuilt: {len(cells)} cells (was 16)")
