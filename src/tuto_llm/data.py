"""Utilitaires de chargement et nettoyage de datasets.

Fournit des fonctions pour charger des fichiers texte (un mot par ligne)
ou CSV, nettoyer les caractères non-ASCII (accents), valider la
compatibilité avec le vocabulaire du mini-LLM (a-z + '.'), et formater
les mots pour l'entraînement.
"""

from __future__ import annotations

import csv
import unicodedata
from pathlib import Path

from tuto_llm.vocab import VOCAB

# Ensemble des lettres acceptées par le vocabulaire (sans le point délimiteur).
# Calculé une seule fois au chargement du module.
_LETTRES: frozenset[str] = frozenset(VOCAB) - {"."}


def charger_dataset(chemin: str) -> list[str]:
    """Charge un fichier texte avec une entrée par ligne.

    Args:
        chemin: Chemin vers le fichier texte.

    Returns:
        Liste des lignes non vides, sans espaces superflus.

    Raises:
        FileNotFoundError: Si le fichier n'existe pas.
    """
    path = Path(chemin)
    if not path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {chemin}")
    text = path.read_text(encoding="utf-8")
    return [line.strip() for line in text.splitlines() if line.strip()]


def charger_csv(chemin: str) -> list[dict[str, str]]:
    """Charge un fichier CSV avec header en liste de dictionnaires.

    Args:
        chemin: Chemin vers le fichier CSV.

    Returns:
        Liste de dictionnaires {colonne: valeur} pour chaque ligne.

    Raises:
        FileNotFoundError: Si le fichier n'existe pas.
    """
    path = Path(chemin)
    if not path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {chemin}")
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def nettoyer_mot(mot: str) -> str:
    """Nettoie un mot : minuscules, suppression des accents, filtre a-z.

    Args:
        mot: Le mot brut à nettoyer.

    Returns:
        Le mot nettoyé contenant uniquement des caractères a-z.

    Examples:
        >>> nettoyer_mot("Éloïse")
        'eloise'
        >>> nettoyer_mot("Jean-Pierre")
        'jeanpierre'
    """
    mot = mot.lower().strip()
    # Décomposition Unicode : é -> e + accent combinant
    nfkd = unicodedata.normalize("NFKD", mot)
    sans_accents = "".join(c for c in nfkd if not unicodedata.combining(c))
    # Garde uniquement a-z
    return "".join(c for c in sans_accents if "a" <= c <= "z")


def valider_vocab(mots: list[str], min_len: int = 1) -> list[str]:
    """Filtre les mots compatibles avec le vocabulaire du mini-LLM.

    Un mot est compatible si tous ses caractères sont dans VOCAB
    (lettres a-z) et sa longueur est >= min_len. Les mots vides
    sont toujours exclus.

    Args:
        mots: Liste de mots à valider.
        min_len: Longueur minimale acceptée (défaut: 1).

    Returns:
        Liste des mots dont tous les caractères sont dans le vocabulaire.
    """
    return [
        mot for mot in mots if len(mot) >= min_len and all(c in _LETTRES for c in mot)
    ]


def formater_training(mots: list[str]) -> list[str]:
    """Formate des mots pour l'entraînement du mini-LLM.

    Ajoute le délimiteur '.' au début et à la fin de chaque mot,
    conformément au format attendu par le modèle bigramme/LLM.

    Args:
        mots: Liste de mots bruts (ex: ["pikachu", "evoli"]).

    Returns:
        Liste de mots formatés (ex: [".pikachu.", ".evoli."]).
    """
    return [f".{mot}." for mot in mots if mot]
