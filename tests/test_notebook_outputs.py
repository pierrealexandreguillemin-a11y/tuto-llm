"""Tests ISO 29119 : vérifier les outputs des notebooks (validations et visualisations).

Ces tests complètent les smoke tests de test_notebooks.py en vérifiant :
- Que chaque verifier() produit une sortie HTML (vert ou jaune)
- Que les valeurs par défaut produisent le feedback jaune (aide)
- Que chaque afficher_*() produit du HTML dans les outputs
- Que _NB_TOTAL correspond au nombre réel d'exercices
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

NOTEBOOKS = [
    "01_deviner_la_suite.ipynb",
    "02_apprendre_des_erreurs.ipynb",
    "03_la_memoire_du_modele.ipynb",
    "04_lattention.ipynb",
    "05_mon_premier_llm.ipynb",
    "06_entrainer_le_modele.ipynb",
]

# Nombre d'exercices par notebook (valeur de _NB_TOTAL)
EXPECTED_NB_TOTAL = {
    "01_deviner_la_suite.ipynb": 4,
    "02_apprendre_des_erreurs.ipynb": 3,
    "03_la_memoire_du_modele.ipynb": 3,
    "04_lattention.ipynb": 2,
    "05_mon_premier_llm.ipynb": 3,
    "06_entrainer_le_modele.ipynb": 3,
}

# Nombre de visualisations HTML attendues par notebook
EXPECTED_VIZ_COUNT = {
    "01_deviner_la_suite.ipynb": 3,  # heatmap + barres + generation
    "02_apprendre_des_erreurs.ipynb": 1,  # evolution_loss
    "03_la_memoire_du_modele.ipynb": 2,  # embeddings + barres
    "04_lattention.ipynb": 4,  # attention x2 + masque_causal x2
    "05_mon_premier_llm.ipynb": 5,  # architecture + barres x2 + attention x2
    "06_entrainer_le_modele.ipynb": 2,  # evolution_loss + barres
}

# Notebook 06 entraîne un LLM.
_TRAINING_NOTEBOOKS = {"06_entrainer_le_modele.ipynb"}

# HTML patterns for feedback detection (must be specific to verifier() output)
# verifier() green includes the checkmark and "Progression" text
_VERIFIER_GREEN = "background:#d4edda;border-left:5px solid #28a745"
_VERIFIER_YELLOW = "background:#fff3cd;border-left:5px solid #ffc107"

# Positive marker for visualization outputs (inserted by all afficher_* functions)
_VIZ_MARKER = "<!-- tuto-viz -->"


def _execute_notebook(notebooks_dir: Path, notebook: str) -> dict:
    """Execute a notebook and return the executed notebook JSON."""
    nb_path = notebooks_dir / notebook

    if notebook in _TRAINING_NOTEBOOKS:
        preproc_timeout = "600"
        subprocess_timeout = 660
    else:
        preproc_timeout = "120"
        subprocess_timeout = 180

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "output.ipynb"
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "nbconvert",
                "--to",
                "notebook",
                "--execute",
                f"--ExecutePreprocessor.timeout={preproc_timeout}",
                str(nb_path),
                "--output",
                str(output_path),
            ],
            capture_output=True,
            text=True,
            timeout=subprocess_timeout,
        )
        assert result.returncode == 0, (
            f"Notebook {notebook} execution failed:\n{result.stderr}"
        )

        with open(output_path, encoding="utf-8") as f:
            return json.load(f)


def _get_all_html_outputs(nb: dict) -> list[str]:
    """Extract all HTML output strings from an executed notebook."""
    html_outputs = []
    for cell in nb["cells"]:
        for output in cell.get("outputs", []):
            if output.get("output_type") == "display_data":
                html_parts = output.get("data", {}).get("text/html", [])
                if html_parts:
                    html_outputs.append("".join(html_parts))
    return html_outputs


def _count_verifier_outputs(html_outputs: list[str]) -> tuple[int, int]:
    """Count green (success) and yellow (aide) verifier outputs."""
    green = sum(1 for h in html_outputs if _VERIFIER_GREEN in h)
    yellow = sum(1 for h in html_outputs if _VERIFIER_YELLOW in h)
    return green, yellow


def _count_viz_outputs(html_outputs: list[str]) -> int:
    """Count visualization outputs using the positive <!-- tuto-viz --> marker."""
    return sum(1 for h in html_outputs if _VIZ_MARKER in h)


_NOTEBOOKS_DIR = Path(__file__).resolve().parent.parent / "notebooks"


@pytest.fixture(scope="module")
def executed_notebooks() -> dict[str, dict]:
    """Execute all notebooks once and cache the results."""
    results = {}
    for nb_name in NOTEBOOKS:
        results[nb_name] = _execute_notebook(_NOTEBOOKS_DIR, nb_name)
    return results


@pytest.mark.slow
@pytest.mark.parametrize("notebook", NOTEBOOKS)
def test_verifier_outputs(executed_notebooks: dict[str, dict], notebook: str) -> None:
    """Chaque verifier() doit produire une sortie HTML (vert ou jaune)."""
    nb = executed_notebooks[notebook]
    html_outputs = _get_all_html_outputs(nb)
    green, yellow = _count_verifier_outputs(html_outputs)
    total_feedback = green + yellow
    expected = EXPECTED_NB_TOTAL[notebook]

    assert total_feedback == expected, (
        f"{notebook}: attendu {expected} feedback verifier, "
        f"trouve {total_feedback} (vert={green}, jaune={yellow})"
    )


@pytest.mark.slow
@pytest.mark.parametrize("notebook", NOTEBOOKS)
def test_default_values_produce_aide(
    executed_notebooks: dict[str, dict], notebook: str
) -> None:
    """Avec les valeurs par defaut, les exercices doivent produire le feedback jaune."""
    nb = executed_notebooks[notebook]
    html_outputs = _get_all_html_outputs(nb)
    green, yellow = _count_verifier_outputs(html_outputs)

    # NB06 Ex2 is an exception: loss always decreases after training
    if notebook == "06_entrainer_le_modele.ipynb":
        assert green <= 1, (
            f"{notebook}: attendu max 1 vert (Ex2 loss), trouve {green} verts"
        )
        assert yellow >= 2, f"{notebook}: attendu au moins 2 jaunes, trouve {yellow}"
    else:
        assert green == 0, (
            f"{notebook}: valeurs par defaut ne doivent PAS produire de vert, "
            f"trouve {green} vert(s)"
        )
        assert yellow == EXPECTED_NB_TOTAL[notebook], (
            f"{notebook}: attendu {EXPECTED_NB_TOTAL[notebook]} jaunes, trouve {yellow}"
        )


@pytest.mark.slow
@pytest.mark.parametrize("notebook", NOTEBOOKS)
def test_visualizations_present(
    executed_notebooks: dict[str, dict], notebook: str
) -> None:
    """Chaque afficher_*() doit produire du HTML dans les outputs."""
    nb = executed_notebooks[notebook]
    html_outputs = _get_all_html_outputs(nb)
    viz_count = _count_viz_outputs(html_outputs)
    expected = EXPECTED_VIZ_COUNT[notebook]

    assert viz_count == expected, (
        f"{notebook}: attendu {expected} visualisations HTML, trouve {viz_count}"
    )


@pytest.mark.slow
@pytest.mark.parametrize("notebook", NOTEBOOKS)
def test_nb_total_matches_exercises(
    executed_notebooks: dict[str, dict], notebook: str
) -> None:
    """_NB_TOTAL doit correspondre au nombre reel d'exercices."""
    nb = executed_notebooks[notebook]

    # Find _NB_TOTAL in source
    nb_total = None
    exercise_nums: set[int] = set()

    for cell in nb["cells"]:
        src = "".join(cell.get("source", []))

        # Extract _NB_TOTAL
        match = re.search(r"_NB_TOTAL\s*=\s*(\d+)", src)
        if match:
            nb_total = int(match.group(1))

        # Extract exercise numbers from verifier() calls
        for m in re.finditer(r"verifier\(\s*(\d+)", src):
            exercise_nums.add(int(m.group(1)))

    assert nb_total is not None, f"{notebook}: _NB_TOTAL non trouve"
    assert nb_total == len(exercise_nums), (
        f"{notebook}: _NB_TOTAL={nb_total} mais {len(exercise_nums)} "
        f"exercices trouves ({sorted(exercise_nums)})"
    )
    assert nb_total == EXPECTED_NB_TOTAL[notebook], (
        f"{notebook}: _NB_TOTAL={nb_total} != attendu {EXPECTED_NB_TOTAL[notebook]}"
    )
