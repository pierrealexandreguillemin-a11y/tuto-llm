"""Smoke tests : vérifier que les 6 notebooks s'exécutent sans erreur (ISO 29119)."""

from __future__ import annotations

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

# Notebook 06 entraîne un LLM et nécessite un timeout plus long.
_TRAINING_NOTEBOOKS = {"06_entrainer_le_modele.ipynb"}


@pytest.mark.slow
@pytest.mark.parametrize("notebook", NOTEBOOKS)
def test_notebook_executes(notebooks_dir: Path, notebook: str) -> None:
    """Chaque notebook doit s'exécuter sans erreur."""
    nb_path = notebooks_dir / notebook
    assert nb_path.exists(), f"Notebook introuvable : {nb_path}"

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
    assert result.returncode == 0, f"Notebook {notebook} a échoué :\n{result.stderr}"
