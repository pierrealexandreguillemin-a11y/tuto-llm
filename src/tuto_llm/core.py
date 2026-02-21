"""Fonctions réutilisables extraites des notebooks.

Ce module contient les fonctions mathématiques et le forward pass
du mini-LLM, extraits pour permettre les tests unitaires.
Les notebooks gardent leur code inline pour la pédagogie.
"""

from __future__ import annotations

import math
import random

from tuto_llm.vocab import VOCAB_SIZE, char_to_id, id_to_char

# ---------------------------------------------------------------------------
# Fonctions mathématiques de base (notebooks 3 & 5)
# ---------------------------------------------------------------------------


def softmax(scores: list[float]) -> list[float]:
    """Transforme des scores bruts en probabilités (somme = 1).

    Utilise le trick max-shift pour la stabilité numérique.
    """
    max_s = max(scores)
    exps = [math.exp(s - max_s) for s in scores]
    total = sum(exps)
    return [e / total for e in exps]


def mat_vec(mat: list[list[float]], vec: list[float]) -> list[float]:
    """Multiplication matrice x vecteur."""
    return [sum(mat[i][j] * vec[j] for j in range(len(vec))) for i in range(len(mat))]


def vec_add(a: list[float], b: list[float]) -> list[float]:
    """Addition élément par élément de deux vecteurs.

    Note: utilise strict=True (fail-fast sur tailles différentes).
    Le notebook utilise strict=False pour la pédagogie.
    """
    return [x + y for x, y in zip(a, b, strict=True)]


def relu(x: list[float]) -> list[float]:
    """ReLU : garde les positifs, met les négatifs à zéro."""
    return [max(0.0, v) for v in x]


def rand_matrix(rows: int, cols: int, scale: float = 0.3) -> list[list[float]]:
    """Génère une matrice aléatoire gaussienne."""
    return [[random.gauss(0, scale) for _ in range(cols)] for _ in range(rows)]


def rand_vector(size: int, scale: float = 0.3) -> list[float]:
    """Génère un vecteur aléatoire gaussien.

    Args:
        size: Nombre d'éléments dans le vecteur.
        scale: Écart-type de la distribution gaussienne.

    Returns:
        Liste de flottants tirés de N(0, scale).
    """
    return [random.gauss(0, scale) for _ in range(size)]


# ---------------------------------------------------------------------------
# Softmax sur dictionnaire (notebook 2)
# ---------------------------------------------------------------------------


def calculer_probas(
    poids: dict[str, dict[str, float]], lettre: str
) -> dict[str, float]:
    """Transforme les scores d'un bigramme en probabilités (softmax)."""
    scores = poids[lettre]
    exps = {b: math.exp(scores[b]) for b in scores}
    total = sum(exps.values())
    return {b: exps[b] / total for b in scores}


# ---------------------------------------------------------------------------
# Forward pass du mini-LLM (notebook 5)
# ---------------------------------------------------------------------------


def forward_llm(
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
) -> list[float]:
    """Passe une séquence dans le mini-LLM, retourne les probabilités."""
    n = len(sequence_ids)

    # 1. Embeddings : token + position
    hidden = []
    for i, tok_id in enumerate(sequence_ids):
        h = vec_add(tok_emb[tok_id], pos_emb[i % context])
        hidden.append(h)

    # 2. Self-Attention (dernière position uniquement)
    q = mat_vec(wq, hidden[-1])

    scores = []
    values = []
    for i in range(n):
        k = mat_vec(wk, hidden[i])
        v = mat_vec(wv, hidden[i])
        score = sum(q[d] * k[d] for d in range(embed_dim)) / math.sqrt(embed_dim)
        scores.append(score)
        values.append(v)

    attn_weights = softmax(scores)

    attn_out = [0.0] * embed_dim
    for i in range(n):
        for d in range(embed_dim):
            attn_out[d] += attn_weights[i] * values[i][d]

    # Connexion résiduelle
    x = vec_add(hidden[-1], attn_out)

    # 3. MLP
    h = relu(vec_add(mat_vec(w1, x), b1))
    mlp_out = vec_add(mat_vec(w2, h), b2)

    # Connexion résiduelle
    x = vec_add(x, mlp_out)

    # 4. Sortie
    logits = mat_vec(w_out, x)
    return softmax(logits)


# ---------------------------------------------------------------------------
# Génération (notebook 5)
# ---------------------------------------------------------------------------


def generer_llm(
    *,
    debut: str = ".",
    temperature: float = 1.0,
    max_len: int = 15,
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
) -> str:
    """Génère un prénom lettre par lettre avec le mini-LLM."""
    ids = [char_to_id[c] for c in debut]
    resultat = debut

    for _ in range(max_len):
        probas = forward_llm(
            ids[-context:],
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

        if temperature != 1.0:
            logits = [math.log(p + 1e-10) / temperature for p in probas]
            probas = softmax(logits)

        idx = random.choices(range(VOCAB_SIZE), weights=probas, k=1)[0]

        if idx == char_to_id["."]:
            break

        ids.append(idx)
        resultat += id_to_char[idx]

    return resultat[1:] if resultat.startswith(".") else resultat
