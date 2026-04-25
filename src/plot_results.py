"""
Generate all plots for the final report.

Run from project root:
    python3 src/plot_results.py

Saves to results/:
    accuracy_comparison.png      – memory & query accuracy bar chart
    error_type_breakdown.png     – stacked bar: slot_extraction vs update_failure
    error_by_key_llm_vs_rule.png – per-slot error counts, LLM vs rule-based
    accuracy_by_domain.png       – per-domain accuracy heatmap
"""

import os
import csv
import ast
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT        = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_CSV = os.path.join(ROOT, "results", "results.csv")
OUT_DIR     = os.path.join(ROOT, "results")

METHODS       = ["adaptive_rule", "adaptive_llm", "window", "summary", "retrieval"]
METHOD_LABELS = ["Rule-based\nSelector", "LLM\nSelector", "Window\nBaseline",
                 "Summary\nBaseline", "Retrieval\nBaseline"]
COLORS        = ["#4C72B0", "#DD8452", "#C44E52", "#8172B2", "#64B5CD"]

# ── Load CSV ──────────────────────────────────────────────────────────────────

def load_csv(path):
    rows = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return rows


# ─────────────────────────────────────────────────────────────────────────────
# Plot 1 — Accuracy comparison (memory + query)
# ─────────────────────────────────────────────────────────────────────────────

def plot_accuracy_comparison(rows):
    # Average memory accuracy per method (one row already has per-dialogue acc)
    mem_acc   = {m: [] for m in METHODS}
    query_acc = {m: [] for m in METHODS}

    for row in rows:
        for m in METHODS:
            mem_acc[m].append(float(row[f"{m}_mem_acc"]))
            query_acc[m].append(int(row[f"{m}_q_correct"]))

    mem_means   = [np.mean(mem_acc[m])   for m in METHODS]
    query_means = [np.mean(query_acc[m]) for m in METHODS]

    x     = np.arange(len(METHODS))
    width = 0.35
    fig, ax = plt.subplots(figsize=(10, 6))

    bars1 = ax.bar(x - width/2, mem_means,   width, label="Memory Accuracy",
                   color=COLORS, alpha=0.9)
    bars2 = ax.bar(x + width/2, query_means, width, label="Query Accuracy",
                   color=COLORS, alpha=0.5, hatch="//")

    ax.set_ylabel("Accuracy", fontsize=13)
    ax.set_title("Memory & Query Accuracy by Method", fontsize=14, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(METHOD_LABELS, fontsize=11)
    ax.set_ylim(0, 1.1)
    ax.legend(fontsize=11)
    ax.yaxis.grid(True, linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)

    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                f"{bar.get_height():.2f}", ha="center", va="bottom", fontsize=9)
    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                f"{bar.get_height():.2f}", ha="center", va="bottom", fontsize=9)

    plt.tight_layout()
    out = os.path.join(OUT_DIR, "accuracy_comparison.png")
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"Saved {out}")


# ─────────────────────────────────────────────────────────────────────────────
# Plot 2 — Error type breakdown (stacked bar)
# ─────────────────────────────────────────────────────────────────────────────

# Hard-coded from the experiment output (error counts per method)
ERROR_DATA = {
    "adaptive_rule": {"slot_extraction_failure": 67, "update_failure": 15},
    "adaptive_llm":  {"slot_extraction_failure": 24, "update_failure": 12},
    "window":        {"slot_extraction_failure": 150, "update_failure": 0},
    "summary":       {"slot_extraction_failure": 67, "update_failure": 9},
    "retrieval":     {"slot_extraction_failure": 48, "update_failure": 10},
}

def plot_error_type_breakdown():
    x      = np.arange(len(METHODS))
    slot   = [ERROR_DATA[m]["slot_extraction_failure"] for m in METHODS]
    update = [ERROR_DATA[m]["update_failure"]          for m in METHODS]

    fig, ax = plt.subplots(figsize=(10, 7))
    b1 = ax.bar(x, slot,   color="#C44E52", label="Slot Extraction Failure")
    b2 = ax.bar(x, update, bottom=slot, color="#4C72B0", label="Update Failure")

    ax.set_ylabel("Number of Errors", fontsize=13)
    ax.set_title("Error Type Breakdown by Method", fontsize=14, fontweight="bold", pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(METHOD_LABELS, fontsize=11)
    ax.set_ylim(0, max(slot[i] + update[i] for i in range(len(slot))) * 1.2)
    ax.legend(fontsize=11)
    ax.yaxis.grid(True, linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)

    for i, (s, u) in enumerate(zip(slot, update)):
        total = s + u
        ax.text(i, total + 2, str(total), ha="center", fontsize=10, fontweight="bold")

    plt.tight_layout()
    out = os.path.join(OUT_DIR, "error_type_breakdown.png")
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"Saved {out}")


# ─────────────────────────────────────────────────────────────────────────────
# Plot 3 — Per-slot extraction failures: LLM vs Rule-based
# ─────────────────────────────────────────────────────────────────────────────

SLOT_ERRORS = {
    "adaptive_rule": {
        "allergy": 13, "coding_language": 9, "diet": 7,
        "drink_preference": 14, "favorite_cuisine": 6,
        "hobby": 10, "hotel_type": 3, "meeting_time": 1, "seat_preference": 4,
    },
    "adaptive_llm": {
        "allergy": 4, "coding_language": 0, "diet": 1,
        "drink_preference": 7, "favorite_cuisine": 4,
        "hobby": 7, "hotel_type": 0, "meeting_time": 1, "seat_preference": 0,
    },
}

def plot_error_by_key():
    keys    = sorted(SLOT_ERRORS["adaptive_rule"].keys())
    rule_v  = [SLOT_ERRORS["adaptive_rule"].get(k, 0) for k in keys]
    llm_v   = [SLOT_ERRORS["adaptive_llm"].get(k, 0)  for k in keys]

    x     = np.arange(len(keys))
    width = 0.35
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.bar(x - width/2, rule_v, width, label="Rule-based Selector",
           color="#4C72B0", alpha=0.9)
    ax.bar(x + width/2, llm_v,  width, label="LLM Selector",
           color="#DD8452", alpha=0.9)

    ax.set_ylabel("Slot Extraction Failures", fontsize=13)
    ax.set_title("Slot Extraction Failures: Rule-based vs LLM Selector",
                 fontsize=14, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels([k.replace("_", "\n") for k in keys], fontsize=10)
    ax.legend(fontsize=11)
    ax.yaxis.grid(True, linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)

    plt.tight_layout()
    out = os.path.join(OUT_DIR, "error_by_key_llm_vs_rule.png")
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"Saved {out}")


# ─────────────────────────────────────────────────────────────────────────────
# Plot 4 — Accuracy by domain (heatmap)
# ─────────────────────────────────────────────────────────────────────────────

def plot_accuracy_by_domain(rows):
    domain_mem = defaultdict(lambda: defaultdict(list))

    for row in rows:
        domain = row["domain"]
        for m in METHODS:
            domain_mem[domain][m].append(float(row[f"{m}_mem_acc"]))

    domains = sorted(domain_mem.keys())
    matrix  = np.array([
        [np.mean(domain_mem[d][m]) for m in METHODS]
        for d in domains
    ])

    fig, ax = plt.subplots(figsize=(12, max(5, len(domains) * 0.7)))
    im = ax.imshow(matrix, cmap="RdYlGn", vmin=0, vmax=1, aspect="auto")

    ax.set_xticks(range(len(METHODS)))
    ax.set_xticklabels(METHOD_LABELS, fontsize=10)
    ax.set_yticks(range(len(domains)))
    ax.set_yticklabels([d.replace("_", " ") for d in domains], fontsize=10)
    ax.set_title("Memory Accuracy by Domain and Method", fontsize=14, fontweight="bold")

    for i in range(len(domains)):
        for j in range(len(METHODS)):
            ax.text(j, i, f"{matrix[i, j]:.2f}",
                    ha="center", va="center", fontsize=9,
                    color="black" if 0.3 < matrix[i, j] < 0.8 else "white")

    plt.colorbar(im, ax=ax, label="Memory Accuracy")
    plt.tight_layout()
    out = os.path.join(OUT_DIR, "accuracy_by_domain.png")
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"Saved {out}")


# ─────────────────────────────────────────────────────────────────────────────
# Plot 5 — Token efficiency vs accuracy scatter
# ─────────────────────────────────────────────────────────────────────────────

def plot_token_efficiency(rows):
    token_cols = [f"{m}_prompt_tokens" for m in METHODS]
    # Check if token data exists in CSV
    if token_cols[0] not in rows[0]:
        print("Skipping token efficiency plot — no token data in CSV.")
        return

    avg_tokens = []
    avg_acc    = []
    for m in METHODS:
        tokens = [float(r[f"{m}_prompt_tokens"]) for r in rows]
        accs   = [float(r[f"{m}_mem_acc"])       for r in rows]
        avg_tokens.append(np.mean(tokens))
        avg_acc.append(np.mean(accs))

    fig, ax = plt.subplots(figsize=(8, 6))
    for i, (tok, acc, label, color) in enumerate(
            zip(avg_tokens, avg_acc, METHOD_LABELS, COLORS)):
        ax.scatter(tok, acc, s=200, color=color, zorder=3)
        ax.annotate(label.replace("\n", " "), (tok, acc),
                    textcoords="offset points", xytext=(8, 4), fontsize=10)

    ax.set_xlabel("Avg Prompt Tokens (memory + question)", fontsize=12)
    ax.set_ylabel("Memory Accuracy", fontsize=12)
    ax.set_title("Accuracy vs Prompt Token Usage", fontsize=14, fontweight="bold")
    ax.yaxis.grid(True, linestyle="--", alpha=0.5)
    ax.xaxis.grid(True, linestyle="--", alpha=0.5)
    ax.set_axisbelow(True)

    plt.tight_layout()
    out = os.path.join(OUT_DIR, "token_efficiency.png")
    plt.savefig(out, dpi=150)
    plt.close()
    print(f"Saved {out}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    rows = load_csv(RESULTS_CSV)
    plot_accuracy_comparison(rows)
    plot_error_type_breakdown()
    plot_error_by_key()
    plot_accuracy_by_domain(rows)
    plot_token_efficiency(rows)
    print("\nAll plots saved to results/")


if __name__ == "__main__":
    main()