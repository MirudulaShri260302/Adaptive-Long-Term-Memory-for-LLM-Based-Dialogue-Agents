"""
Embedding-based retrieval baseline (RAG).

Uses sentence-transformers to encode all user turns and each test query,
then retrieves the top-k most semantically similar turns and extracts
memory from them.  This matches the proposal's description of
"top-k past snippets via embedding similarity."
"""

import numpy as np
from sentence_transformers import SentenceTransformer

# Load once at module level so repeated calls don't reload the model
_model = None

def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))


# ── Memory extraction from a single retrieved turn ────────────────────────────

def extract_memory_from_text(text: str) -> tuple:
    t = text.lower()

    if "vegan" in t or "plant-based" in t or "no animal products" in t:
        return "diet", "vegan"
    if ("vegetarian" in t or "do not eat meat" in t or "meat-free" in t) and "vegan" not in t:
        return "diet", "vegetarian"
    if "allergic to peanuts" in t or "cannot eat peanuts" in t or "peanuts are something i am allergic to" in t or "peanut allergy" in t:
        return "allergy", "peanuts"
    if "window seat" in t or "by the window" in t or "near the window" in t or "sit near the window" in t:
        return "seat_preference", "window"
    if "4pm" in t or "4 in the afternoon" in t:
        return "meeting_time", "4pm"
    if "3pm" in t or "3 in the afternoon" in t:
        return "meeting_time", "3pm"
    if "10am" in t or "10 in the morning" in t:
        return "meeting_time", "10am"
    if "painting" in t or "doing art" in t or "making art" in t or "creative artwork" in t:
        return "hobby", "painting"
    if "italian" in t and ("food" in t or "cuisine" in t or "like" in t or "enjoy" in t):
        return "favorite_cuisine", "italian"
    if "budget hotel" in t or "cheap hotel" in t or "affordable place to stay" in t or "cheaper places to stay" in t:
        return "hotel_type", "budget"
    if "decaf" in t or "avoid caffeine" in t or "caffeine-free" in t or "no caffeine" in t:
        return "drink_preference", "decaf"
    if "python" in t and ("coding" in t or "programming" in t or "interview" in t or "practice" in t):
        return "coding_language", "python"

    return None, None


# ── Baseline ──────────────────────────────────────────────────────────────────

def run_retrieval_baseline(dialogue: dict, top_k: int = 3) -> dict:
    """
    For each test query, embed the query and all user turns, retrieve the
    top-k most similar turns by cosine similarity, and extract memory from them.
    Later queries overwrite earlier ones for the same key (recency bias).
    """
    memory: dict = {}

    if not dialogue.get("test_queries"):
        return memory

    model = _get_model()

    user_turns = [
        turn for turn in dialogue["turns"] if turn["role"] == "user"
    ]
    if not user_turns:
        return memory

    turn_texts    = [t["text"] for t in user_turns]
    turn_embeddings = model.encode(turn_texts, convert_to_numpy=True)

    for test_query in dialogue["test_queries"]:
        query        = test_query["question"]
        query_emb    = model.encode([query], convert_to_numpy=True)[0]

        scored = sorted(
            enumerate(turn_texts),
            key=lambda x: cosine_similarity(query_emb, turn_embeddings[x[0]]),
            reverse=True,
        )

        for idx, text in scored[:top_k]:
            key, value = extract_memory_from_text(text)
            if key is not None:
                memory[key] = value

    return memory