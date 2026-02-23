"""Fonctions d'entraînement du mini-LLM.

Ce module contient le forward pass avec cache, le backward pass analytique,
la cross-entropy loss et le calcul de loss sur un batch.
Extrait du notebook 06 pour permettre les tests unitaires.
"""

from __future__ import annotations

import math

from tuto_llm.vocab import VOCAB_SIZE, char_to_id


def cross_entropy_loss(probas: list[float], cible: int) -> float:
    """Calcule -log(probas[cible]).

    Args:
        probas: Distribution de probabilites (somme = 1).
        cible: Indice de la classe correcte.

    Returns:
        La loss (toujours >= 0).
    """
    return -math.log(probas[cible] + 1e-10)


def forward_with_cache(
    sequence_ids: list[int],
    *,
    tok_emb: list[list[float]],
    pos_emb: list[list[float]],
    wq: list[list[float]],
    wk: list[list[float]],
    wv: list[list[float]],
    w1: list[list[float]],
    b1: list[float],
    w2: list[list[float]],
    b2: list[float],
    w_out: list[list[float]],
    context: int,
    embed_dim: int,
) -> tuple[list[float], dict]:
    """Forward pass retournant probas + activations pour backward.

    Identique a forward_llm de core.py mais conserve toutes les
    activations intermediaires necessaires au backward pass.

    Returns:
        Tuple (probas, cache) ou cache contient les activations.
    """
    n = len(sequence_ids)
    hidden_dim = len(b1)

    # 1. Embeddings : token + position
    hidden = []
    for i, tok_id in enumerate(sequence_ids):
        h = [tok_emb[tok_id][d] + pos_emb[i % context][d] for d in range(embed_dim)]
        hidden.append(h)

    # 2. Self-Attention (derniere position uniquement)
    q = _mat_vec(wq, hidden[-1], embed_dim)

    scores_raw: list[float] = []
    keys: list[list[float]] = []
    values: list[list[float]] = []
    for i in range(n):
        k = _mat_vec(wk, hidden[i], embed_dim)
        v = _mat_vec(wv, hidden[i], embed_dim)
        score = sum(q[d] * k[d] for d in range(embed_dim)) / math.sqrt(embed_dim)
        scores_raw.append(score)
        keys.append(k)
        values.append(v)

    attn_weights = _softmax(scores_raw)

    attn_out = [0.0] * embed_dim
    for i in range(n):
        for d in range(embed_dim):
            attn_out[d] += attn_weights[i] * values[i][d]

    # Connexion residuelle 1
    x_after_attn = [hidden[-1][d] + attn_out[d] for d in range(embed_dim)]

    # 3. MLP
    h1_pre = [
        sum(w1[j][d] * x_after_attn[d] for d in range(embed_dim)) + b1[j]
        for j in range(hidden_dim)
    ]
    h1 = [max(0.0, v) for v in h1_pre]  # ReLU
    mlp_out = [
        sum(w2[d][j] * h1[j] for j in range(hidden_dim)) + b2[d]
        for d in range(embed_dim)
    ]

    # Connexion residuelle 2
    x_final = [x_after_attn[d] + mlp_out[d] for d in range(embed_dim)]

    # 4. Sortie
    logits = [
        sum(w_out[v][d] * x_final[d] for d in range(embed_dim))
        for v in range(VOCAB_SIZE)
    ]
    probas = _softmax(logits)

    cache = {
        "sequence_ids": sequence_ids,
        "hidden": hidden,
        "q": q,
        "keys": keys,
        "values": values,
        "scores_raw": scores_raw,
        "attn_weights": attn_weights,
        "attn_out": attn_out,
        "x_after_attn": x_after_attn,
        "h1_pre": h1_pre,
        "h1": h1,
        "mlp_out": mlp_out,
        "x_final": x_final,
        "logits": logits,
    }
    return probas, cache


def backward_llm(
    cache: dict,
    probas: list[float],
    cible: int,
    *,
    wq: list[list[float]],
    wk: list[list[float]],
    wv: list[list[float]],
    w1: list[list[float]],
    w2: list[list[float]],
    w_out: list[list[float]],
    embed_dim: int,
) -> dict:
    """Backward pass : retourne les gradients pour tous les poids.

    Args:
        cache: Activations intermediaires du forward pass.
        probas: Probabilites de sortie du forward pass.
        cible: Indice du token cible (la bonne reponse).
        wq, wk, wv, w1, w2, w_out: Poids du modele.
        embed_dim: Dimension des embeddings.

    Returns:
        Dictionnaire des gradients pour chaque parametre.
    """
    hidden = cache["hidden"]
    q = cache["q"]
    keys = cache["keys"]
    values = cache["values"]
    attn_weights = cache["attn_weights"]
    x_after_attn = cache["x_after_attn"]
    h1_pre = cache["h1_pre"]
    h1 = cache["h1"]
    x_final = cache["x_final"]
    sequence_ids = cache["sequence_ids"]
    n = len(sequence_ids)
    hidden_dim = len(h1)

    # --- Etape 1 : gradient de la loss par rapport aux logits ---
    # dL/d_logit[j] = probas[j] - 1(j == cible)
    d_logits = [probas[v] - (1.0 if v == cible else 0.0) for v in range(VOCAB_SIZE)]

    # --- Etape 2 : gradient de W_out et x_final ---
    d_w_out = [
        [d_logits[v] * x_final[d] for d in range(embed_dim)] for v in range(VOCAB_SIZE)
    ]
    d_x_final = [
        sum(d_logits[v] * w_out[v][d] for v in range(VOCAB_SIZE))
        for d in range(embed_dim)
    ]

    # --- Etape 3 : connexion residuelle 2 ---
    # x_final = x_after_attn + mlp_out
    d_mlp_out = list(d_x_final)
    d_x_after_attn = list(d_x_final)  # gradient passe aussi directement

    # --- Etape 4 : backward du MLP ---
    # mlp_out[d] = sum_j(w2[d][j] * h1[j]) + b2[d]
    d_w2 = [[d_mlp_out[d] * h1[j] for j in range(hidden_dim)] for d in range(embed_dim)]
    d_b2 = list(d_mlp_out)
    d_h1 = [
        sum(d_mlp_out[d] * w2[d][j] for d in range(embed_dim))
        for j in range(hidden_dim)
    ]

    # ReLU backward
    d_h1_pre = [d_h1[j] * (1.0 if h1_pre[j] > 0 else 0.0) for j in range(hidden_dim)]

    # h1_pre[j] = sum_d(w1[j][d] * x_after_attn[d]) + b1[j]
    d_w1 = [
        [d_h1_pre[j] * x_after_attn[d] for d in range(embed_dim)]
        for j in range(hidden_dim)
    ]
    d_b1 = list(d_h1_pre)
    # gradient de x_after_attn depuis le MLP
    for d in range(embed_dim):
        d_x_after_attn[d] += sum(d_h1_pre[j] * w1[j][d] for j in range(hidden_dim))

    # --- Etape 5 : connexion residuelle 1 ---
    # x_after_attn = hidden[-1] + attn_out
    d_attn_out = list(d_x_after_attn)
    d_hidden_last = list(d_x_after_attn)

    # --- Etape 6 : backward de l'attention ---
    # attn_out[d] = sum_i(attn_weights[i] * values[i][d])
    d_attn_weights = [
        sum(d_attn_out[d] * values[i][d] for d in range(embed_dim)) for i in range(n)
    ]
    d_values = [
        [d_attn_out[d] * attn_weights[i] for d in range(embed_dim)] for i in range(n)
    ]

    # Softmax backward pour les poids d'attention
    # d_score[i] = sum_j(attn_weights[i] * (delta_ij - attn_weights[j]) * d_attn_weights[j])
    d_scores = [0.0] * n
    for i in range(n):
        for j in range(n):
            if i == j:
                d_scores[i] += (
                    attn_weights[i] * (1.0 - attn_weights[i]) * d_attn_weights[i]
                )
            else:
                d_scores[i] += -attn_weights[j] * attn_weights[i] * d_attn_weights[j]

    # Diviser par sqrt(embed_dim) (scaling)
    scale = math.sqrt(embed_dim)
    d_scores = [ds / scale for ds in d_scores]

    # scores[i] = sum_d(q[d] * keys[i][d])
    d_q = [sum(d_scores[i] * keys[i][d] for i in range(n)) for d in range(embed_dim)]
    d_keys = [[d_scores[i] * q[d] for d in range(embed_dim)] for i in range(n)]

    # q = Wq @ hidden[-1]
    d_wq = [
        [d_q[r] * hidden[-1][c] for c in range(embed_dim)] for r in range(embed_dim)
    ]
    d_hidden_from_q = [
        sum(d_q[r] * wq[r][c] for r in range(embed_dim)) for c in range(embed_dim)
    ]
    for d in range(embed_dim):
        d_hidden_last[d] += d_hidden_from_q[d]

    # keys[i] = Wk @ hidden[i], values[i] = Wv @ hidden[i]
    d_wk = [[0.0] * embed_dim for _ in range(embed_dim)]
    d_wv = [[0.0] * embed_dim for _ in range(embed_dim)]
    d_hidden_from_kv: list[list[float]] = [[0.0] * embed_dim for _ in range(n)]

    for i in range(n):
        for r in range(embed_dim):
            for c in range(embed_dim):
                d_wk[r][c] += d_keys[i][r] * hidden[i][c]
                d_wv[r][c] += d_values[i][r] * hidden[i][c]
                d_hidden_from_kv[i][c] += d_keys[i][r] * wk[r][c]
                d_hidden_from_kv[i][c] += d_values[i][r] * wv[r][c]

    # --- Etape 7 : gradient des embeddings ---
    d_tok_emb: list[list[float]] = [[0.0] * embed_dim for _ in range(VOCAB_SIZE)]
    d_pos_emb: list[list[float]] = [[0.0] * embed_dim for _ in range(max(n, 1))]

    for i in range(n):
        d_h_i = list(d_hidden_from_kv[i])
        if i == n - 1:
            for d in range(embed_dim):
                d_h_i[d] += d_hidden_last[d]
        tok_id = sequence_ids[i]
        for d in range(embed_dim):
            d_tok_emb[tok_id][d] += d_h_i[d]
            d_pos_emb[i][d] += d_h_i[d]

    return {
        "d_w_out": d_w_out,
        "d_w2": d_w2,
        "d_b2": d_b2,
        "d_w1": d_w1,
        "d_b1": d_b1,
        "d_wq": d_wq,
        "d_wk": d_wk,
        "d_wv": d_wv,
        "d_tok_emb": d_tok_emb,
        "d_pos_emb": d_pos_emb,
    }


def calcul_loss(
    mots_formates: list[str],
    *,
    tok_emb: list[list[float]],
    pos_emb: list[list[float]],
    wq: list[list[float]],
    wk: list[list[float]],
    wv: list[list[float]],
    w1: list[list[float]],
    b1: list[float],
    w2: list[list[float]],
    b2: list[float],
    w_out: list[list[float]],
    context: int,
    embed_dim: int,
) -> float:
    """Loss moyenne sur un batch de mots formates (".pikachu.", ...).

    Args:
        mots_formates: Liste de mots au format ".mot." .
        Autres arguments: poids du modele et hyperparametres.

    Returns:
        Loss moyenne (cross-entropy) sur toutes les positions.
    """
    loss_totale = 0.0
    nb = 0
    for mot in mots_formates:
        ids = [char_to_id[c] for c in mot]
        for i in range(1, len(ids)):
            seq = ids[:i][-context:]
            cible = ids[i]
            probas, _ = forward_with_cache(
                seq,
                tok_emb=tok_emb,
                pos_emb=pos_emb,
                wq=wq,
                wk=wk,
                wv=wv,
                w1=w1,
                b1=b1,
                w2=w2,
                b2=b2,
                w_out=w_out,
                context=context,
                embed_dim=embed_dim,
            )
            loss_totale += cross_entropy_loss(probas, cible)
            nb += 1
    return loss_totale / nb if nb > 0 else 0.0


# ---------------------------------------------------------------------------
# Fonctions utilitaires internes
# ---------------------------------------------------------------------------


def _mat_vec(mat: list[list[float]], vec: list[float], size: int) -> list[float]:
    """Multiplication matrice x vecteur (interne)."""
    return [sum(mat[i][j] * vec[j] for j in range(size)) for i in range(len(mat))]


def _softmax(scores: list[float]) -> list[float]:
    """Softmax avec max-shift pour stabilite numerique (interne)."""
    max_s = max(scores)
    exps = [math.exp(s - max_s) for s in scores]
    total = sum(exps)
    return [e / total for e in exps]
