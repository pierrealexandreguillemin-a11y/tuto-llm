"""Tests unitaires pour src/tuto_llm/core.py (ISO 29119)."""

from __future__ import annotations

import math
import random

import pytest

from tuto_llm.core import (
    calculer_probas,
    forward_llm,
    generer_llm,
    mat_vec,
    rand_matrix,
    relu,
    softmax,
    vec_add,
)
from tuto_llm.vocab import VOCAB_SIZE, char_to_id


# ---------------------------------------------------------------------------
# TestSoftmax
# ---------------------------------------------------------------------------


class TestSoftmax:
    """Tests pour la fonction softmax."""

    def test_somme_egale_un(self) -> None:
        scores = [1.0, 2.0, 3.0]
        probas = softmax(scores)
        assert abs(sum(probas) - 1.0) < 1e-7

    def test_toutes_positives(self) -> None:
        scores = [-5.0, 0.0, 5.0]
        probas = softmax(scores)
        assert all(p >= 0 for p in probas)

    def test_plus_grand_score_plus_grande_proba(self) -> None:
        scores = [1.0, 3.0, 2.0]
        probas = softmax(scores)
        assert probas[1] > probas[2] > probas[0]

    def test_scores_identiques_donnent_probas_uniformes(self) -> None:
        scores = [2.0, 2.0, 2.0]
        probas = softmax(scores)
        for p in probas:
            assert abs(p - 1 / 3) < 1e-7

    def test_stabilite_numerique_grands_scores(self) -> None:
        scores = [1000.0, 1001.0, 1002.0]
        probas = softmax(scores)
        assert abs(sum(probas) - 1.0) < 1e-7

    def test_un_seul_element(self) -> None:
        probas = softmax([42.0])
        assert abs(probas[0] - 1.0) < 1e-7


# ---------------------------------------------------------------------------
# TestMatVec
# ---------------------------------------------------------------------------


class TestMatVec:
    """Tests pour la multiplication matrice x vecteur."""

    def test_identite(self) -> None:
        identite = [[1, 0], [0, 1]]
        vec = [3.0, 5.0]
        result = mat_vec(identite, vec)
        assert result == pytest.approx([3.0, 5.0])

    def test_matrice_2x3(self) -> None:
        mat = [[1, 2, 3], [4, 5, 6]]
        vec = [1.0, 0.0, -1.0]
        result = mat_vec(mat, vec)
        # [1*1+2*0+3*(-1), 4*1+5*0+6*(-1)] = [-2, -2]
        assert result == pytest.approx([-2.0, -2.0])

    def test_vecteur_zero(self) -> None:
        mat = [[1, 2], [3, 4]]
        vec = [0.0, 0.0]
        result = mat_vec(mat, vec)
        assert result == pytest.approx([0.0, 0.0])


# ---------------------------------------------------------------------------
# TestVecAdd
# ---------------------------------------------------------------------------


class TestVecAdd:
    """Tests pour l'addition vectorielle."""

    def test_addition_simple(self) -> None:
        assert vec_add([1, 2], [3, 4]) == pytest.approx([4, 6])

    def test_addition_zero(self) -> None:
        assert vec_add([1, 2, 3], [0, 0, 0]) == pytest.approx([1, 2, 3])

    def test_addition_negatifs(self) -> None:
        assert vec_add([1, -2], [-1, 2]) == pytest.approx([0, 0])


# ---------------------------------------------------------------------------
# TestRelu
# ---------------------------------------------------------------------------


class TestRelu:
    """Tests pour la fonction ReLU."""

    def test_positifs_inchanges(self) -> None:
        assert relu([1.0, 2.0, 3.0]) == pytest.approx([1.0, 2.0, 3.0])

    def test_negatifs_a_zero(self) -> None:
        assert relu([-1.0, -5.0]) == pytest.approx([0.0, 0.0])

    def test_mixte(self) -> None:
        assert relu([-1.0, 0.0, 1.0]) == pytest.approx([0.0, 0.0, 1.0])

    def test_zero(self) -> None:
        assert relu([0.0]) == pytest.approx([0.0])


# ---------------------------------------------------------------------------
# TestRandMatrix
# ---------------------------------------------------------------------------


class TestRandMatrix:
    """Tests pour la génération de matrices aléatoires."""

    def test_dimensions(self) -> None:
        mat = rand_matrix(3, 5)
        assert len(mat) == 3
        assert all(len(row) == 5 for row in mat)

    def test_reproductibilite(self) -> None:
        random.seed(123)
        m1 = rand_matrix(2, 2)
        random.seed(123)
        m2 = rand_matrix(2, 2)
        assert m1 == m2


# ---------------------------------------------------------------------------
# TestCalculerProbas
# ---------------------------------------------------------------------------


class TestCalculerProbas:
    """Tests pour le softmax sur dictionnaire (notebook 2)."""

    def test_somme_egale_un(self) -> None:
        poids = {"a": {"b": 1.0, "c": 2.0, "d": 0.5}}
        probas = calculer_probas(poids, "a")
        assert abs(sum(probas.values()) - 1.0) < 1e-7

    def test_cles_preservees(self) -> None:
        poids = {"x": {"a": 0.0, "b": 0.0}}
        probas = calculer_probas(poids, "x")
        assert set(probas.keys()) == {"a", "b"}


# ---------------------------------------------------------------------------
# TestForwardLlm
# ---------------------------------------------------------------------------


class TestForwardLlm:
    """Tests pour le forward pass du mini-LLM."""

    @pytest.fixture()
    def model_weights(self) -> dict:
        """Crée des poids de modèle déterministes pour les tests."""
        random.seed(42)
        embed_dim = 4
        context = 4
        hidden_dim = 8
        return {
            "tok_emb": rand_matrix(VOCAB_SIZE, embed_dim, 0.5),
            "pos_emb": rand_matrix(context, embed_dim, 0.5),
            "wq": rand_matrix(embed_dim, embed_dim, 0.2),
            "wk": rand_matrix(embed_dim, embed_dim, 0.2),
            "wv": rand_matrix(embed_dim, embed_dim, 0.2),
            "w1": rand_matrix(hidden_dim, embed_dim, 0.2),
            "b1": [0.0] * hidden_dim,
            "w2": rand_matrix(embed_dim, hidden_dim, 0.2),
            "b2": [0.0] * embed_dim,
            "w_out": rand_matrix(VOCAB_SIZE, embed_dim, 0.2),
            "context": context,
            "embed_dim": embed_dim,
        }

    def test_retourne_probas_valides(self, model_weights: dict) -> None:
        seq = [char_to_id["."], char_to_id["e"]]
        probas = forward_llm(seq, **model_weights)
        assert len(probas) == VOCAB_SIZE
        assert abs(sum(probas) - 1.0) < 1e-6
        assert all(p >= 0 for p in probas)

    def test_sequence_un_seul_token(self, model_weights: dict) -> None:
        seq = [char_to_id["."]]
        probas = forward_llm(seq, **model_weights)
        assert len(probas) == VOCAB_SIZE
        assert abs(sum(probas) - 1.0) < 1e-6

    def test_determinisme(self, model_weights: dict) -> None:
        seq = [char_to_id["."], char_to_id["a"], char_to_id["b"]]
        p1 = forward_llm(seq, **model_weights)
        p2 = forward_llm(seq, **model_weights)
        assert p1 == pytest.approx(p2)


# ---------------------------------------------------------------------------
# TestGeneration
# ---------------------------------------------------------------------------


class TestGeneration:
    """Tests pour la génération de prénoms."""

    @pytest.fixture()
    def model_weights(self) -> dict:
        """Crée des poids de modèle déterministes pour les tests."""
        random.seed(42)
        embed_dim = 4
        context = 4
        hidden_dim = 8
        return {
            "tok_emb": rand_matrix(VOCAB_SIZE, embed_dim, 0.5),
            "pos_emb": rand_matrix(context, embed_dim, 0.5),
            "wq": rand_matrix(embed_dim, embed_dim, 0.2),
            "wk": rand_matrix(embed_dim, embed_dim, 0.2),
            "wv": rand_matrix(embed_dim, embed_dim, 0.2),
            "w1": rand_matrix(hidden_dim, embed_dim, 0.2),
            "b1": [0.0] * hidden_dim,
            "w2": rand_matrix(embed_dim, hidden_dim, 0.2),
            "b2": [0.0] * embed_dim,
            "w_out": rand_matrix(VOCAB_SIZE, embed_dim, 0.2),
            "context": context,
            "embed_dim": embed_dim,
        }

    def test_genere_une_chaine(self, model_weights: dict) -> None:
        random.seed(99)
        result = generer_llm(debut=".", max_len=5, **model_weights)
        assert isinstance(result, str)
        assert len(result) <= 5

    def test_respecte_max_len(self, model_weights: dict) -> None:
        random.seed(99)
        result = generer_llm(debut=".", max_len=3, **model_weights)
        assert len(result) <= 3

    def test_temperature(self, model_weights: dict) -> None:
        random.seed(99)
        r1 = generer_llm(debut=".", temperature=0.5, max_len=10, **model_weights)
        assert isinstance(r1, str)
