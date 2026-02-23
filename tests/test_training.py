"""Tests unitaires pour src/tuto_llm/training.py (ISO 29119)."""

from __future__ import annotations

import copy
import math
import random

import pytest

from tuto_llm.core import forward_llm, rand_matrix, rand_vector
from tuto_llm.training import (
    backward_llm,
    calcul_loss,
    cross_entropy_loss,
    forward_with_cache,
)
from tuto_llm.vocab import VOCAB_SIZE, char_to_id

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def model_kwargs() -> dict:
    """Poids deterministes pour les tests."""
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
        "b1": rand_vector(hidden_dim, 0.1),
        "w2": rand_matrix(embed_dim, hidden_dim, 0.2),
        "b2": rand_vector(embed_dim, 0.1),
        "w_out": rand_matrix(VOCAB_SIZE, embed_dim, 0.2),
        "context": context,
        "embed_dim": embed_dim,
    }


# ---------------------------------------------------------------------------
# TestCrossEntropyLoss
# ---------------------------------------------------------------------------


class TestCrossEntropyLoss:
    """Tests pour cross_entropy_loss."""

    def test_prediction_parfaite(self) -> None:
        probas = [0.0] * 27
        probas[5] = 1.0
        assert cross_entropy_loss(probas, 5) == pytest.approx(0.0, abs=1e-6)

    def test_prediction_uniforme(self) -> None:
        probas = [1.0 / 27] * 27
        loss = cross_entropy_loss(probas, 0)
        assert loss == pytest.approx(math.log(27), rel=1e-3)

    def test_prediction_mauvaise(self) -> None:
        probas = [0.0] * 27
        probas[0] = 0.99
        probas[1] = 0.01
        loss = cross_entropy_loss(probas, 1)
        assert loss > 4.0  # -log(0.01) ~= 4.6

    def test_prob_quasi_nulle(self) -> None:
        """Epsilon 1e-10 empeche log(0)."""
        probas = [0.0] * 27
        probas[0] = 1.0
        loss = cross_entropy_loss(probas, 5)
        assert math.isfinite(loss)
        assert loss > 20  # -log(1e-10) ~= 23


# ---------------------------------------------------------------------------
# TestForwardWithCache
# ---------------------------------------------------------------------------


class TestForwardWithCache:
    """Tests pour forward_with_cache."""

    def test_retourne_probas_valides(self, model_kwargs: dict) -> None:
        seq = [char_to_id["."], char_to_id["a"]]
        probas, cache = forward_with_cache(seq, **model_kwargs)
        assert len(probas) == VOCAB_SIZE
        assert abs(sum(probas) - 1.0) < 1e-6
        assert all(p >= 0 for p in probas)

    def test_cache_contient_cles_attendues(self, model_kwargs: dict) -> None:
        seq = [char_to_id["."], char_to_id["a"]]
        _, cache = forward_with_cache(seq, **model_kwargs)
        expected_keys = {
            "sequence_ids",
            "hidden",
            "q",
            "keys",
            "values",
            "scores_raw",
            "attn_weights",
            "attn_out",
            "x_after_attn",
            "h1_pre",
            "h1",
            "mlp_out",
            "x_final",
            "logits",
        }
        assert set(cache.keys()) == expected_keys

    def test_probas_identiques_a_forward_llm(self, model_kwargs: dict) -> None:
        seq = [char_to_id["."], char_to_id["e"], char_to_id["m"]]
        probas_cache, _ = forward_with_cache(seq, **model_kwargs)
        probas_core = forward_llm(seq, **model_kwargs)
        for i in range(VOCAB_SIZE):
            assert probas_cache[i] == pytest.approx(probas_core[i], abs=1e-10)

    def test_formes_correctes(self, model_kwargs: dict) -> None:
        embed_dim = model_kwargs["embed_dim"]
        hidden_dim = len(model_kwargs["b1"])
        seq = [char_to_id["."], char_to_id["a"], char_to_id["b"]]
        _, cache = forward_with_cache(seq, **model_kwargs)
        assert len(cache["hidden"]) == 3
        assert len(cache["hidden"][0]) == embed_dim
        assert len(cache["q"]) == embed_dim
        assert len(cache["keys"]) == 3
        assert len(cache["attn_weights"]) == 3
        assert len(cache["h1"]) == hidden_dim
        assert len(cache["x_final"]) == embed_dim
        assert len(cache["logits"]) == VOCAB_SIZE


# ---------------------------------------------------------------------------
# TestBackwardLlm
# ---------------------------------------------------------------------------


class TestBackwardLlm:
    """Tests pour backward_llm."""

    def _get_grads(self, model_kwargs: dict, seq: list[int], cible: int) -> dict:
        """Helper : forward + backward."""
        probas, cache = forward_with_cache(seq, **model_kwargs)
        backward_kwargs = {
            "wq": model_kwargs["wq"],
            "wk": model_kwargs["wk"],
            "wv": model_kwargs["wv"],
            "w1": model_kwargs["w1"],
            "w2": model_kwargs["w2"],
            "w_out": model_kwargs["w_out"],
            "embed_dim": model_kwargs["embed_dim"],
        }
        return backward_llm(cache, probas, cible, **backward_kwargs)

    def test_formes_des_gradients(self, model_kwargs: dict) -> None:
        embed_dim = model_kwargs["embed_dim"]
        hidden_dim = len(model_kwargs["b1"])
        seq = [char_to_id["."], char_to_id["a"]]
        grads = self._get_grads(model_kwargs, seq, char_to_id["b"])

        assert len(grads["d_w_out"]) == VOCAB_SIZE
        assert len(grads["d_w_out"][0]) == embed_dim
        assert len(grads["d_w1"]) == hidden_dim
        assert len(grads["d_w1"][0]) == embed_dim
        assert len(grads["d_w2"]) == embed_dim
        assert len(grads["d_w2"][0]) == hidden_dim
        assert len(grads["d_b1"]) == hidden_dim
        assert len(grads["d_b2"]) == embed_dim
        assert len(grads["d_wq"]) == embed_dim
        assert len(grads["d_wq"][0]) == embed_dim
        assert len(grads["d_wk"]) == embed_dim
        assert len(grads["d_wv"]) == embed_dim
        assert len(grads["d_tok_emb"]) == VOCAB_SIZE
        assert len(grads["d_tok_emb"][0]) == embed_dim

    def test_gradient_non_nul(self, model_kwargs: dict) -> None:
        seq = [char_to_id["."], char_to_id["a"]]
        grads = self._get_grads(model_kwargs, seq, char_to_id["b"])
        # W_out devrait toujours avoir un gradient non-nul
        total = sum(
            abs(grads["d_w_out"][v][d])
            for v in range(VOCAB_SIZE)
            for d in range(model_kwargs["embed_dim"])
        )
        assert total > 0.0

    def test_gradient_w_out_numerique(self, model_kwargs: dict) -> None:
        """Verification numerique : (loss+ - loss-) / 2eps vs gradient analytique."""
        seq = [char_to_id["."], char_to_id["a"]]
        cible = char_to_id["l"]
        grads = self._get_grads(model_kwargs, seq, cible)
        eps = 1e-5

        # Tester quelques elements de W_out
        for v_idx, d_idx in [(0, 0), (5, 2), (26, 3)]:
            kw_plus = copy.deepcopy(model_kwargs)
            kw_minus = copy.deepcopy(model_kwargs)
            kw_plus["w_out"][v_idx][d_idx] += eps
            kw_minus["w_out"][v_idx][d_idx] -= eps

            probas_p, _ = forward_with_cache(seq, **kw_plus)
            probas_m, _ = forward_with_cache(seq, **kw_minus)
            loss_p = cross_entropy_loss(probas_p, cible)
            loss_m = cross_entropy_loss(probas_m, cible)
            grad_num = (loss_p - loss_m) / (2 * eps)
            grad_ana = grads["d_w_out"][v_idx][d_idx]
            assert grad_num == pytest.approx(grad_ana, abs=1e-3), (
                f"W_out[{v_idx}][{d_idx}]: num={grad_num:.6f} ana={grad_ana:.6f}"
            )

    def test_gradient_w1_numerique(self, model_kwargs: dict) -> None:
        """Verification numerique pour W1."""
        seq = [char_to_id["."], char_to_id["e"]]
        cible = char_to_id["m"]
        grads = self._get_grads(model_kwargs, seq, cible)
        eps = 1e-5

        for j_idx, d_idx in [(0, 0), (3, 1)]:
            kw_plus = copy.deepcopy(model_kwargs)
            kw_minus = copy.deepcopy(model_kwargs)
            kw_plus["w1"][j_idx][d_idx] += eps
            kw_minus["w1"][j_idx][d_idx] -= eps

            probas_p, _ = forward_with_cache(seq, **kw_plus)
            probas_m, _ = forward_with_cache(seq, **kw_minus)
            loss_p = cross_entropy_loss(probas_p, cible)
            loss_m = cross_entropy_loss(probas_m, cible)
            grad_num = (loss_p - loss_m) / (2 * eps)
            grad_ana = grads["d_w1"][j_idx][d_idx]
            assert grad_num == pytest.approx(grad_ana, abs=1e-3), (
                f"W1[{j_idx}][{d_idx}]: num={grad_num:.6f} ana={grad_ana:.6f}"
            )

    def test_gradient_wq_numerique(self, model_kwargs: dict) -> None:
        """Verification numerique pour Wq (attention)."""
        seq = [char_to_id["."], char_to_id["a"]]
        cible = char_to_id["b"]
        grads = self._get_grads(model_kwargs, seq, cible)
        eps = 1e-5

        for r, c in [(0, 0), (1, 2)]:
            kw_plus = copy.deepcopy(model_kwargs)
            kw_minus = copy.deepcopy(model_kwargs)
            kw_plus["wq"][r][c] += eps
            kw_minus["wq"][r][c] -= eps

            probas_p, _ = forward_with_cache(seq, **kw_plus)
            probas_m, _ = forward_with_cache(seq, **kw_minus)
            loss_p = cross_entropy_loss(probas_p, cible)
            loss_m = cross_entropy_loss(probas_m, cible)
            grad_num = (loss_p - loss_m) / (2 * eps)
            grad_ana = grads["d_wq"][r][c]
            assert grad_num == pytest.approx(grad_ana, abs=1e-3), (
                f"Wq[{r}][{c}]: num={grad_num:.6f} ana={grad_ana:.6f}"
            )

    def test_gradient_tok_emb_numerique(self, model_kwargs: dict) -> None:
        """Verification numerique pour les token embeddings."""
        seq = [char_to_id["."], char_to_id["a"]]
        cible = char_to_id["b"]
        grads = self._get_grads(model_kwargs, seq, cible)
        eps = 1e-5

        # Token 'a' (id=1) est dans la sequence
        tok_id = char_to_id["a"]
        for d_idx in [0, 2]:
            kw_plus = copy.deepcopy(model_kwargs)
            kw_minus = copy.deepcopy(model_kwargs)
            kw_plus["tok_emb"][tok_id][d_idx] += eps
            kw_minus["tok_emb"][tok_id][d_idx] -= eps

            probas_p, _ = forward_with_cache(seq, **kw_plus)
            probas_m, _ = forward_with_cache(seq, **kw_minus)
            loss_p = cross_entropy_loss(probas_p, cible)
            loss_m = cross_entropy_loss(probas_m, cible)
            grad_num = (loss_p - loss_m) / (2 * eps)
            grad_ana = grads["d_tok_emb"][tok_id][d_idx]
            assert grad_num == pytest.approx(grad_ana, abs=1e-3), (
                f"tok_emb[{tok_id}][{d_idx}]: num={grad_num:.6f} ana={grad_ana:.6f}"
            )

    def test_gradient_sequence_un_token(self, model_kwargs: dict) -> None:
        """Backward fonctionne avec une sequence d'un seul token."""
        seq = [char_to_id["."]]
        grads = self._get_grads(model_kwargs, seq, char_to_id["a"])
        total = sum(
            abs(grads["d_w_out"][v][d])
            for v in range(VOCAB_SIZE)
            for d in range(model_kwargs["embed_dim"])
        )
        assert total > 0.0

    def test_loss_diminue_apres_update(self, model_kwargs: dict) -> None:
        """Un pas de SGD doit reduire la loss."""
        seq = [char_to_id["."], char_to_id["a"]]
        cible = char_to_id["l"]
        lr = 0.1

        # Loss avant
        probas_before, cache = forward_with_cache(seq, **model_kwargs)
        loss_before = cross_entropy_loss(probas_before, cible)

        # Backward
        backward_kwargs = {
            "wq": model_kwargs["wq"],
            "wk": model_kwargs["wk"],
            "wv": model_kwargs["wv"],
            "w1": model_kwargs["w1"],
            "w2": model_kwargs["w2"],
            "w_out": model_kwargs["w_out"],
            "embed_dim": model_kwargs["embed_dim"],
        }
        grads = backward_llm(cache, probas_before, cible, **backward_kwargs)

        # Update W_out seulement (test minimal)
        updated = copy.deepcopy(model_kwargs)
        for v in range(VOCAB_SIZE):
            for d in range(model_kwargs["embed_dim"]):
                updated["w_out"][v][d] -= lr * grads["d_w_out"][v][d]

        # Loss apres
        probas_after, _ = forward_with_cache(seq, **updated)
        loss_after = cross_entropy_loss(probas_after, cible)
        assert loss_after < loss_before


# ---------------------------------------------------------------------------
# TestCalculLoss
# ---------------------------------------------------------------------------


class TestCalculLoss:
    """Tests pour calcul_loss."""

    def test_loss_positive(self, model_kwargs: dict) -> None:
        loss = calcul_loss([".ab.", ".cd."], **model_kwargs)
        assert loss > 0

    def test_loss_initiale_proche_log_vocab(self, model_kwargs: dict) -> None:
        """Poids aleatoires -> loss ~log(27) ~= 3.3."""
        loss = calcul_loss([".alice.", ".bob.", ".emma."], **model_kwargs)
        assert 2.0 < loss < 5.0

    def test_loss_diminue_apres_update(self, model_kwargs: dict) -> None:
        """Plusieurs pas de SGD sur un seul mot reduisent la loss."""
        mots = [".ab."]
        lr = 0.1
        loss_before = calcul_loss(mots, **model_kwargs)

        # 10 pas de SGD sur le mot
        kw = copy.deepcopy(model_kwargs)
        for _step in range(10):
            ids = [char_to_id[c] for c in ".ab."]
            for i in range(1, len(ids)):
                seq = ids[:i]
                cible_id = ids[i]
                probas, cache = forward_with_cache(seq, **kw)
                backward_kw = {
                    "wq": kw["wq"],
                    "wk": kw["wk"],
                    "wv": kw["wv"],
                    "w1": kw["w1"],
                    "w2": kw["w2"],
                    "w_out": kw["w_out"],
                    "embed_dim": kw["embed_dim"],
                }
                grads = backward_llm(cache, probas, cible_id, **backward_kw)
                # Update tous les poids
                for v in range(VOCAB_SIZE):
                    for d in range(kw["embed_dim"]):
                        kw["w_out"][v][d] -= lr * grads["d_w_out"][v][d]
                for j in range(len(kw["b1"])):
                    kw["b1"][j] -= lr * grads["d_b1"][j]
                    for d in range(kw["embed_dim"]):
                        kw["w1"][j][d] -= lr * grads["d_w1"][j][d]
                for d in range(kw["embed_dim"]):
                    kw["b2"][d] -= lr * grads["d_b2"][d]
                    for j in range(len(kw["b1"])):
                        kw["w2"][d][j] -= lr * grads["d_w2"][d][j]

        loss_after = calcul_loss(mots, **kw)
        assert loss_after < loss_before

    def test_liste_vide(self, model_kwargs: dict) -> None:
        loss = calcul_loss([], **model_kwargs)
        assert loss == 0.0
