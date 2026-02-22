#!/usr/bin/env python3
"""Pipeline reproductible de construction des datasets.

Télécharge les sources brutes, nettoie et produit les fichiers finaux
dans data/. Peut être relancé à tout moment pour régénérer les datasets
à l'identique.

Usage:
    python scripts/build_datasets.py

Sources:
    - Prénoms INSEE : https://www.insee.fr/fr/statistiques/7633685
    - Dinosaures    : https://gist.github.com/Dvelezs94/24bfcc8ab6042613ab5d94275e2e395a
    - Haiku         : https://github.com/docmarionum1/haikurnn
    - Pokémon       : https://pokeapi.co/ (noms de base uniquement)
"""

from __future__ import annotations

import csv
import io
import json
import unicodedata
import urllib.request
import zipfile
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

DINOS_URL = (
    "https://gist.githubusercontent.com/Dvelezs94/"
    "24bfcc8ab6042613ab5d94275e2e395a/raw/"
    "ffc7ed8156b5419e63fa8963f0c306308a6c1012/dinos.txt"
)

PRENOMS_URL = "https://www.insee.fr/fr/statistiques/fichier/7633685/nat2022_csv.zip"

HAIKU_URL = (
    "https://raw.githubusercontent.com/docmarionum1/"
    "haikurnn/master/input/poems/haikus.csv"
)

POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon?limit=2000"

MIN_PRENOM_LEN = 2  # Exclure les prénoms d'un seul caractère (bruit)
MIN_POKEMON_LEN = 2  # Exclure les noms d'un seul caractère
HAIKU_SAMPLE_SIZE = 1000


# ---------------------------------------------------------------------------
# Fonctions utilitaires
# ---------------------------------------------------------------------------


def remove_accents(text: str) -> str:
    """Supprime les accents via décomposition NFKD."""
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def clean_word(word: str) -> str:
    """Lowercase, supprime accents, ne garde que a-z."""
    cleaned = remove_accents(word.lower().strip())
    return "".join(c for c in cleaned if "a" <= c <= "z")


def download(url: str, user_agent: str | None = None) -> bytes:
    """Télécharge une URL et retourne le contenu brut."""
    print(f"  Téléchargement : {url[:80]}...")
    req = urllib.request.Request(url)  # noqa: S310
    if user_agent:
        req.add_header("User-Agent", user_agent)
    with urllib.request.urlopen(req) as resp:  # noqa: S310
        return resp.read()


# ---------------------------------------------------------------------------
# Construction des datasets
# ---------------------------------------------------------------------------


def build_dinosaures() -> None:
    """Télécharge et nettoie le dataset de dinosaures."""
    print("\n[1/4] Dinosaures")
    raw = download(DINOS_URL).decode("utf-8")

    dinos: set[str] = set()
    for line in raw.splitlines():
        name = clean_word(line)
        if name and name.isalpha() and name.isascii():
            dinos.add(name)

    output = DATA_DIR / "dinosaures.txt"
    output.write_text(
        "\n".join(sorted(dinos)) + "\n",
        encoding="utf-8",
    )
    print(f"  -> {output} : {len(dinos)} noms")


def build_prenoms() -> None:
    """Télécharge et nettoie le dataset de prénoms INSEE."""
    print("\n[2/4] Prénoms INSEE")
    zip_data = download(PRENOMS_URL)

    with zipfile.ZipFile(io.BytesIO(zip_data)) as zf:
        # Le ZIP contient nat2022.csv
        csv_name = [n for n in zf.namelist() if n.endswith(".csv")][0]
        csv_bytes = zf.read(csv_name)

    csv_text = csv_bytes.decode("utf-8")
    reader = csv.DictReader(io.StringIO(csv_text), delimiter=";")

    prenoms: set[str] = set()
    for row in reader:
        name = row["preusuel"]
        if name.startswith("_"):
            continue
        cleaned = clean_word(name)
        if (
            cleaned
            and cleaned.isalpha()
            and cleaned.isascii()
            and len(cleaned) >= MIN_PRENOM_LEN
        ):
            prenoms.add(cleaned)

    output = DATA_DIR / "prenoms.txt"
    output.write_text(
        "\n".join(sorted(prenoms)) + "\n",
        encoding="utf-8",
    )
    print(f"  -> {output} : {len(prenoms)} prénoms (min_len={MIN_PRENOM_LEN})")


def build_haiku() -> None:
    """Télécharge un échantillon de haiku."""
    print("\n[3/4] Haiku")
    raw = download(HAIKU_URL).decode("utf-8")

    reader = csv.reader(io.StringIO(raw))
    _header = next(reader)  # 0,1,2,source,...

    rows: list[list[str]] = []
    for i, row in enumerate(reader):
        if i >= HAIKU_SAMPLE_SIZE:
            break
        rows.append(row)

    output = DATA_DIR / "haiku.csv"
    with output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["line1", "line2", "line3", "source"])
        for row in rows:
            writer.writerow([row[0], row[1], row[2], row[3]])

    print(f"  -> {output} : {len(rows)} haiku")


def build_pokemon() -> None:
    """Télécharge les noms de base des Pokémon depuis PokéAPI."""
    print("\n[4/4] Pokémon")
    raw = download(POKEAPI_URL, user_agent="TutoLLM/1.0")
    data = json.loads(raw)

    noms: set[str] = set()
    for entry in data["results"]:
        # Nom de base uniquement (avant le premier tiret).
        # Ex: "charizard-mega-x" -> "charizard"
        base = entry["name"].split("-")[0]
        cleaned = clean_word(base)
        if (
            cleaned
            and cleaned.isalpha()
            and cleaned.isascii()
            and len(cleaned) >= MIN_POKEMON_LEN
        ):
            noms.add(cleaned)

    output = DATA_DIR / "pokemon.txt"
    output.write_text(
        "\n".join(sorted(noms)) + "\n",
        encoding="utf-8",
    )
    print(f"  -> {output} : {len(noms)} noms")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    """Point d'entrée principal."""
    print(f"Répertoire de sortie : {DATA_DIR}")
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    build_dinosaures()
    build_prenoms()
    build_haiku()
    build_pokemon()

    print("\nTerminé. Fichiers générés :")
    for f in sorted(DATA_DIR.iterdir()):
        if f.name.startswith("."):
            continue
        print(f"  {f.name} ({f.stat().st_size:,} octets)")


if __name__ == "__main__":
    main()
