"""
Forgetting curve analysis.

For each dialogue, finds how far back (in turns) each important fact was
stated relative to the final test query. Groups dialogues into distance
buckets and plots memory accuracy per method per bucket.

Run from project root:
    python3 src/forgetting_curve.py
"""

import json
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from selector import classify_turn
from selector_llm import classify_turn_llm
from memory_slots import initialize_memory, update_memory
from evaluator import evaluate_memory
from baseline_window import run_window_baseline
from baseline_summary import run_summary_baseline
from baseline_retrieval import run_retrieval_baseline

ROOT      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(ROOT, "data", "dialogues_harder_augmented.json")
OUT_PATH  = os.path.join(ROOT, "results", "forgetting_curve.png")

METHODS       = ["adaptive_rule", "adaptive_llm", "window", "summary", "retrieval"]
METHOD_LABELS = ["Rule-based", "LLM Selector", "Window", "Summary", "Retrieval"]
COLORS        = ["#4C72B0", "#DD8452", "#C44E52", "#8172B2", "#64B5CD"]
BUCKETS       = [(0, 20), (21, 40), (41, 60), (61, 200)]
BUCKET_LABELS = ["0–20", "21–40", "41–60", "61+"]


def load_dialogues(path):
    with open(path) as f:
        return json.load(f)


def run_adaptive_memory(dialogue, selector_fn):
    memory = initialize_memory()
    for turn in dialogue["turns"]:
        if turn["role"] == "user":
            action, key, value = selector_fn(turn["text"])
            if action == "STORE" and key:
                update_memory(memory, key, value)
    return memory


def find_fact_distance(dialogue, fact_key):
    """
    Find the turn index where the given fact key was first mentioned
    as a user turn containing the expected value keyword.
    Returns distance = total_turns - fact_turn_index.
    Returns None if not found.
    """
    turns = dialogue["turns"]
    total = len(turns)
    expected_value = None

    for fact in dialogue["memory_facts"]:
        if fact["key"] == fact_key:
            expected_value = fact["value"].lower()
            break

    if expected_value is None:
        return None

    for i, turn in enumerate(turns):
        if turn["role"] == "user" and expected_value in turn["text"].lower():
            return total - i   # distance from fact to end of dialogue

    return None


def bucket_index(distance):
    for i, (lo, hi) in enumerate(BUCKETS):
        if lo <= distance <= hi:
            return i
    return len(BUCKETS) - 1


def main():
    dialogues = load_dialogues(DATA_PATH)

    # bucket_accs[method][bucket] = list of accuracy values
    bucket_accs = {m: [[] for _ in BUCKETS] for m in METHODS}

    for dialogue in dialogues:
        memories = {
            "adaptive_rule": run_adaptive_memory(dialogue, classify_turn),
            "adaptive_llm":  run_adaptive_memory(dialogue, classify_turn_llm),
            "window":        run_window_baseline(dialogue, k=2),
            "summary":       run_summary_baseline(dialogue),
            "retrieval":     run_retrieval_baseline(dialogue),
        }
        evals = {m: evaluate_memory(memories[m], dialogue["memory_facts"])
                 for m in METHODS}

        for fact in dialogue["memory_facts"]:
            dist = find_fact_distance(dialogue, fact["key"])
            if dist is None:
                continue
            b = bucket_index(dist)

            for m in METHODS:
                # per-fact accuracy: 1 if this key is correct, 0 otherwise
                mem = memories[m]
                correct = int(
                    fact["key"] in mem and mem[fact["key"]] == fact["value"]
                )
                bucket_accs[m][b].append(correct)

    # ── Plot ──────────────────────────────────────────────────────────────────
    x     = np.arange(len(BUCKETS))
    width = 0.15
    fig, ax = plt.subplots(figsize=(12, 6))

    for i, (m, label, color) in enumerate(zip(METHODS, METHOD_LABELS, COLORS)):
        means = [np.mean(bucket_accs[m][b]) if bucket_accs[m][b] else 0
                 for b in range(len(BUCKETS))]
        offset = (i - len(METHODS) / 2) * width + width / 2
        bars = ax.bar(x + offset, means, width, label=label,
                      color=color, alpha=0.9)

    ax.set_xlabel("Distance from Fact to Query (turns)", fontsize=13)
    ax.set_ylabel("Memory Accuracy", fontsize=13)
    ax.set_title("Forgetting Curve: Memory Accuracy vs. Fact Distance",
                 fontsize=14, fontweight="bold", pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(BUCKET_LABELS, fontsize=12)
    ax.set_ylim(0, 1.15)
    ax.legend(fontsize=10)
    ax.yaxis.grid(True, linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig(OUT_PATH, dpi=150)
    plt.close()
    print(f"Saved forgetting curve → {OUT_PATH}")

    # ── Print summary table ───────────────────────────────────────────────────
    print(f"\n{'Method':<18}", end="")
    for label in BUCKET_LABELS:
        print(f"  {label:>8}", end="")
    print()
    print("-" * 55)
    for m, label in zip(METHODS, METHOD_LABELS):
        print(f"{label:<18}", end="")
        for b in range(len(BUCKETS)):
            vals = bucket_accs[m][b]
            mean = np.mean(vals) if vals else 0
            print(f"  {mean:>8.3f}", end="")
        print()


if __name__ == "__main__":
    main()