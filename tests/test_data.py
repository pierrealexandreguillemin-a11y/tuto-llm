"""Tests unitaires et d'intégration pour src/tuto_llm/data.py (ISO 29119)."""

from __future__ import annotations

from pathlib import Path

import pytest

from tuto_llm.data import (
    charger_csv,
    charger_dataset,
    formater_training,
    nettoyer_mot,
    valider_vocab,
)

# ---------------------------------------------------------------------------
# TestChargerDataset
# ---------------------------------------------------------------------------


class TestChargerDataset:
    """Tests pour le chargement de fichiers texte."""

    def test_charge_fichier_valide(self, tmp_path: Path) -> None:
        f = tmp_path / "noms.txt"
        f.write_text("alice\nbob\ncharlie\n", encoding="utf-8")
        result = charger_dataset(str(f))
        assert result == ["alice", "bob", "charlie"]

    def test_ignore_lignes_vides(self, tmp_path: Path) -> None:
        f = tmp_path / "noms.txt"
        f.write_text("alice\n\nbob\n\n", encoding="utf-8")
        result = charger_dataset(str(f))
        assert result == ["alice", "bob"]

    def test_strip_espaces(self, tmp_path: Path) -> None:
        f = tmp_path / "noms.txt"
        f.write_text("  alice  \n  bob  \n", encoding="utf-8")
        result = charger_dataset(str(f))
        assert result == ["alice", "bob"]

    def test_fichier_inexistant(self) -> None:
        with pytest.raises(FileNotFoundError):
            charger_dataset("/chemin/inexistant/fichier.txt")

    def test_fichier_vide(self, tmp_path: Path) -> None:
        f = tmp_path / "vide.txt"
        f.write_text("", encoding="utf-8")
        result = charger_dataset(str(f))
        assert result == []


# ---------------------------------------------------------------------------
# TestChargerCsv
# ---------------------------------------------------------------------------


class TestChargerCsv:
    """Tests pour le chargement de fichiers CSV."""

    def test_charge_csv_valide(self, tmp_path: Path) -> None:
        f = tmp_path / "data.csv"
        f.write_text("col1,col2\na,b\nc,d\n", encoding="utf-8")
        result = charger_csv(str(f))
        assert result == [{"col1": "a", "col2": "b"}, {"col1": "c", "col2": "d"}]

    def test_csv_fichier_inexistant(self) -> None:
        with pytest.raises(FileNotFoundError):
            charger_csv("/chemin/inexistant/fichier.csv")

    def test_csv_vide_avec_header(self, tmp_path: Path) -> None:
        f = tmp_path / "vide.csv"
        f.write_text("col1,col2\n", encoding="utf-8")
        result = charger_csv(str(f))
        assert result == []

    def test_csv_colonnes_preservees(self, tmp_path: Path) -> None:
        f = tmp_path / "h.csv"
        f.write_text("line1,line2,line3,source\na,b,c,src\n", encoding="utf-8")
        result = charger_csv(str(f))
        assert len(result) == 1
        assert set(result[0].keys()) == {"line1", "line2", "line3", "source"}


# ---------------------------------------------------------------------------
# TestNettoyerMot
# ---------------------------------------------------------------------------


class TestNettoyerMot:
    """Tests pour le nettoyage de mots."""

    def test_minuscules(self) -> None:
        assert nettoyer_mot("Alice") == "alice"

    def test_accent_aigu(self) -> None:
        assert nettoyer_mot("élodie") == "elodie"

    def test_accent_grave(self) -> None:
        assert nettoyer_mot("hélène") == "helene"

    def test_cedille(self) -> None:
        assert nettoyer_mot("françois") == "francois"

    def test_trema(self) -> None:
        assert nettoyer_mot("loïc") == "loic"

    def test_umlaut(self) -> None:
        assert nettoyer_mot("über") == "uber"

    def test_tiret_supprime(self) -> None:
        assert nettoyer_mot("Jean-Pierre") == "jeanpierre"

    def test_espaces_supprimes(self) -> None:
        assert nettoyer_mot("  alice  ") == "alice"

    def test_mot_vide(self) -> None:
        assert nettoyer_mot("") == ""

    def test_chiffres_supprimes(self) -> None:
        assert nettoyer_mot("abc123") == "abc"


# ---------------------------------------------------------------------------
# TestValiderVocab
# ---------------------------------------------------------------------------


class TestValiderVocab:
    """Tests pour la validation du vocabulaire."""

    def test_mots_valides(self) -> None:
        assert valider_vocab(["alice", "bob"]) == ["alice", "bob"]

    def test_filtre_caracteres_invalides(self) -> None:
        assert valider_vocab(["alice", "bob2", "ch@rlie"]) == ["alice"]

    def test_filtre_mots_vides(self) -> None:
        assert valider_vocab(["alice", "", "bob"]) == ["alice", "bob"]

    def test_liste_vide(self) -> None:
        assert valider_vocab([]) == []

    def test_point_non_accepte(self) -> None:
        """Le point est dans VOCAB mais pas dans les mots de dataset."""
        assert valider_vocab(["a.b"]) == []

    def test_accents_non_acceptes(self) -> None:
        assert valider_vocab(["élodie"]) == []

    def test_min_len_filtre_courts(self) -> None:
        assert valider_vocab(["a", "ab", "abc"], min_len=2) == ["ab", "abc"]

    def test_min_len_defaut_garde_un_char(self) -> None:
        assert valider_vocab(["a", "ab"]) == ["a", "ab"]


# ---------------------------------------------------------------------------
# TestFormaterTraining
# ---------------------------------------------------------------------------


class TestFormaterTraining:
    """Tests pour le formatage training-ready."""

    def test_ajoute_points(self) -> None:
        assert formater_training(["alice", "bob"]) == [".alice.", ".bob."]

    def test_liste_vide(self) -> None:
        assert formater_training([]) == []

    def test_filtre_mots_vides(self) -> None:
        assert formater_training(["alice", "", "bob"]) == [".alice.", ".bob."]

    def test_un_seul_mot(self) -> None:
        assert formater_training(["chat"]) == [".chat."]


# ---------------------------------------------------------------------------
# Tests d'intégration sur les vrais fichiers
# ---------------------------------------------------------------------------


class TestIntegrationPrenoms:
    """Tests d'intégration chargeant data/prenoms.txt."""

    @pytest.fixture()
    def prenoms(self) -> list[str]:
        return charger_dataset("data/prenoms.txt")

    def test_fichier_existe_et_non_vide(self, prenoms: list[str]) -> None:
        assert len(prenoms) > 10000

    def test_tous_pure_az(self, prenoms: list[str]) -> None:
        for mot in prenoms:
            assert mot.isalpha() and mot.isascii() and mot.islower(), f"invalide: {mot}"

    def test_pas_de_doublons(self, prenoms: list[str]) -> None:
        assert len(prenoms) == len(set(prenoms))

    def test_trie_alphabetiquement(self, prenoms: list[str]) -> None:
        assert prenoms == sorted(prenoms)

    def test_pas_de_mot_un_char(self, prenoms: list[str]) -> None:
        singles = [m for m in prenoms if len(m) == 1]
        assert singles == [], f"Prénoms 1 char trouvés : {singles}"

    def test_100pct_valides_vocab(self, prenoms: list[str]) -> None:
        assert valider_vocab(prenoms) == prenoms

    def test_formater_training(self, prenoms: list[str]) -> None:
        formatted = formater_training(prenoms[:3])
        assert all(m.startswith(".") and m.endswith(".") for m in formatted)


class TestIntegrationDinosaures:
    """Tests d'intégration chargeant data/dinosaures.txt."""

    @pytest.fixture()
    def dinos(self) -> list[str]:
        return charger_dataset("data/dinosaures.txt")

    def test_fichier_existe_et_non_vide(self, dinos: list[str]) -> None:
        assert len(dinos) > 1000

    def test_tous_pure_az(self, dinos: list[str]) -> None:
        for mot in dinos:
            assert mot.isalpha() and mot.isascii() and mot.islower(), f"invalide: {mot}"

    def test_pas_de_doublons(self, dinos: list[str]) -> None:
        assert len(dinos) == len(set(dinos))

    def test_trie_alphabetiquement(self, dinos: list[str]) -> None:
        assert dinos == sorted(dinos)

    def test_100pct_valides_vocab(self, dinos: list[str]) -> None:
        assert valider_vocab(dinos) == dinos


class TestIntegrationPokemonEng:
    """Tests d'intégration chargeant data/pokemon_eng.txt (noms anglais)."""

    @pytest.fixture()
    def pokemon(self) -> list[str]:
        return charger_dataset("data/pokemon_eng.txt")

    def test_fichier_existe_et_non_vide(self, pokemon: list[str]) -> None:
        assert len(pokemon) > 900

    def test_tous_pure_az(self, pokemon: list[str]) -> None:
        for mot in pokemon:
            assert mot.isalpha() and mot.isascii() and mot.islower(), f"invalide: {mot}"

    def test_pas_de_doublons(self, pokemon: list[str]) -> None:
        assert len(pokemon) == len(set(pokemon))

    def test_trie_alphabetiquement(self, pokemon: list[str]) -> None:
        assert pokemon == sorted(pokemon)

    def test_pas_de_mot_un_char(self, pokemon: list[str]) -> None:
        singles = [m for m in pokemon if len(m) == 1]
        assert singles == [], f"Pokémon 1 char trouvés : {singles}"

    def test_100pct_valides_vocab(self, pokemon: list[str]) -> None:
        assert valider_vocab(pokemon) == pokemon

    def test_formater_training(self, pokemon: list[str]) -> None:
        formatted = formater_training(pokemon[:3])
        assert all(m.startswith(".") and m.endswith(".") for m in formatted)


class TestIntegrationPokemonFr:
    """Tests d'intégration chargeant data/pokemon.txt (noms français)."""

    @pytest.fixture()
    def pokemon_fr(self) -> list[str]:
        return charger_dataset("data/pokemon.txt")

    def test_fichier_existe_et_non_vide(self, pokemon_fr: list[str]) -> None:
        assert len(pokemon_fr) > 800

    def test_tous_pure_az(self, pokemon_fr: list[str]) -> None:
        for mot in pokemon_fr:
            assert mot.isalpha() and mot.isascii() and mot.islower(), f"invalide: {mot}"

    def test_pas_de_doublons(self, pokemon_fr: list[str]) -> None:
        assert len(pokemon_fr) == len(set(pokemon_fr))

    def test_trie_alphabetiquement(self, pokemon_fr: list[str]) -> None:
        assert pokemon_fr == sorted(pokemon_fr)

    def test_min_3_chars(self, pokemon_fr: list[str]) -> None:
        courts = [m for m in pokemon_fr if len(m) < 3]
        assert courts == [], f"Pokémon < 3 chars trouvés : {courts}"

    def test_100pct_valides_vocab(self, pokemon_fr: list[str]) -> None:
        assert valider_vocab(pokemon_fr) == pokemon_fr

    def test_formater_training(self, pokemon_fr: list[str]) -> None:
        formatted = formater_training(pokemon_fr[:3])
        assert all(m.startswith(".") and m.endswith(".") for m in formatted)

    def test_noms_fr_reconnaissables(self, pokemon_fr: list[str]) -> None:
        """Vérifie que quelques noms FR iconiques sont présents."""
        attendus = {"pikachu", "dracaufeu", "ronflex", "evoli", "ectoplasma"}
        presents = attendus & set(pokemon_fr)
        assert len(presents) >= 4, f"Noms FR manquants : {attendus - presents}"


class TestIntegrationHaiku:
    """Tests d'intégration chargeant data/haiku.csv."""

    @pytest.fixture()
    def haiku(self) -> list[dict[str, str]]:
        return charger_csv("data/haiku.csv")

    def test_fichier_existe_et_non_vide(self, haiku: list[dict[str, str]]) -> None:
        assert len(haiku) == 1000

    def test_colonnes_correctes(self, haiku: list[dict[str, str]]) -> None:
        expected = {"line1", "line2", "line3", "source"}
        assert set(haiku[0].keys()) == expected

    def test_pas_de_ligne_vide(self, haiku: list[dict[str, str]]) -> None:
        for row in haiku:
            assert row["line1"].strip(), f"line1 vide: {row}"
