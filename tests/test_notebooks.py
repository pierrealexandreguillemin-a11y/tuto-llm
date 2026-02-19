"""Smoke tests : vérifier que les 5 notebooks s'exécutent sans erreur (ISO 29119)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

NOTEBOOKS = [
    "01_deviner_la_suite.ipynb",
    "02_apprendre_des_erreurs.ipynb",
    "03_la_memoire_du_modele.ipynb",
    "04_lattention.ipynb",
    "05_mon_premier_llm.ipynb",
]


@pytest.mark.slow
@pytest.mark.parametrize("notebook", NOTEBOOKS)
def test_notebook_executes(notebooks_dir: Path, notebook: str) -> None:
    """Chaque notebook doit s'exécuter sans erreur."""
    nb_path = notebooks_dir / notebook
    assert nb_path.exists(), f"Notebook introuvable : {nb_path}"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "jupyter",
            "nbconvert",
            "--to",
            "notebook",
            "--execute",
            "--ExecutePreprocessor.timeout=120",
            str(nb_path),
            "--output",
            "/dev/null",
        ],
        capture_output=True,
        text=True,
        timeout=180,
    )
    assert result.returncode == 0, (
        f"Notebook {notebook} a échoué :\n{result.stderr}"
    )
