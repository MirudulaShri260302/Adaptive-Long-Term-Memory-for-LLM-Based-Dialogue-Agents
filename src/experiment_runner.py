import json
import csv
import os

def count_tokens(text: str) -> int:
    """Approximate token count (1 token ≈ 4 characters, standard estimate)."""
    return max(1, len(text) // 4)

def memory_to_prompt_text(memory: dict) -> str:
    """Serialize memory dict as it would appear in a prompt."""
    return " ".join(f"{k}={v}" for k, v in memory.items())

def compute_prompt_tokens(memory: dict, question: str) -> int:
    """Estimate tokens used in the prompt: memory slots + question."""
    return count_tokens(memory_to_prompt_text(memory)) + count_tokens(question)

from selector import classify_turn                      # rule-based
from selector_llm import classify_turn_llm              # LLM-based
from memory_slots import initialize_memory, update_memory
from evaluator import (
    evaluate_memory,
    evaluate_test_query_response,
    aggregate_errors,
    print_error_summary,
)
from baseline_window import run_window_baseline
from baseline_summary import run_summary_baseline
from baseline_retrieval import run_retrieval_baseline
from prompt_builder import generate_memory_based_response


def load_dialogues(path: str) -> list:
    # resolve path relative to this file so the script works from any directory
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(base, path)
    with open(full_path) as f:
        return json.load(f)


def run_adaptive_memory(dialogue: dict, selector_fn) -> dict:
    memory = initialize_memory()
    for turn in dialogue["turns"]:
        if turn["role"] == "user":
            action, key, value = selector_fn(turn["text"])
            if action == "STORE" and key:
                update_memory(memory, key, value)
    return memory


def main():
    dialogues = load_dialogues("data/dialogues_harder_augmented.json")

    # ── Counters ──────────────────────────────────────────────────────────────
    methods = ["adaptive_rule", "adaptive_llm", "window", "summary", "retrieval"]
    mem_correct   = {m: 0 for m in methods}
    mem_total     = {m: 0 for m in methods}
    q_correct     = {m: 0 for m in methods}
    prompt_tokens = {m: [] for m in methods}   # token efficiency tracking
    total_queries = 0

    all_errors   = {m: [] for m in methods}   # for error analysis
    rows         = []

    for dialogue in dialogues:
        # ── Run all methods ───────────────────────────────────────────────────
        memories = {
            "adaptive_rule": run_adaptive_memory(dialogue, classify_turn),
            "adaptive_llm":  run_adaptive_memory(dialogue, classify_turn_llm),
            "window":        run_window_baseline(dialogue, k=2),
            "summary":       run_summary_baseline(dialogue),
            "retrieval":     run_retrieval_baseline(dialogue),
        }

        # ── Memory accuracy ───────────────────────────────────────────────────
        evals = {m: evaluate_memory(memories[m], dialogue["memory_facts"])
                 for m in methods}

        for m in methods:
            mem_correct[m] += evals[m]["correct"]
            mem_total[m]   += evals[m]["total"]
            all_errors[m].append(evals[m]["errors"])

        print("=" * 60)
        print("Dialogue:", dialogue["id"])
        for m in methods:
            print(f"  {m:<18} memory={memories[m]}  acc={evals[m]['accuracy']:.2f}")

        # ── Query accuracy ─────────────────────────────────────────────────────
        for test_query in dialogue["test_queries"]:
            question       = test_query["question"]
            expected_value = test_query["expected_value"]

            responses = {m: generate_memory_based_response(memories[m], question)
                         for m in methods}
            ok        = {m: evaluate_test_query_response(responses[m], expected_value)
                         for m in methods}

            for m in methods:
                if ok[m]:
                    q_correct[m] += 1
                prompt_tokens[m].append(compute_prompt_tokens(memories[m], question))
            total_queries += 1

            print(f"  Q: {question}")
            for m in methods:
                print(f"    {m:<18} → {responses[m]}  correct={ok[m]}")

            rows.append({
                "dialogue_id":    dialogue["id"],
                "domain":         dialogue["domain"],
                "question":       question,
                "expected_value": expected_value,
                **{f"{m}_mem_acc":      evals[m]["accuracy"]                          for m in methods},
                **{f"{m}_q_correct":    int(ok[m])                                    for m in methods},
                **{f"{m}_response":     responses[m]                                  for m in methods},
                **{f"{m}_errors":       str(evals[m]["errors"])                       for m in methods},
                **{f"{m}_prompt_tokens": compute_prompt_tokens(memories[m], question) for m in methods},
            })

    # ── Final results ─────────────────────────────────────────────────────────
    print("\nFINAL RESULTS")
    print("=" * 60)
    print(f"\n{'Method':<18} {'Mem Acc':>8} {'Query Acc':>10} {'Avg Prompt Tokens':>18}")
    print("-" * 58)
    for m in methods:
        mem_acc   = mem_correct[m] / mem_total[m]  if mem_total[m]  else 0
        q_acc     = q_correct[m]  / total_queries  if total_queries else 0
        avg_tok   = sum(prompt_tokens[m]) / len(prompt_tokens[m]) if prompt_tokens[m] else 0
        print(f"{m:<18} {mem_acc:>8.3f} {q_acc:>10.3f} {avg_tok:>18.1f}")

    # ── Error analysis ────────────────────────────────────────────────────────
    print("\nERROR ANALYSIS")
    for m in methods:
        agg = aggregate_errors(all_errors[m])
        print_error_summary(m, agg)

    # ── Save CSV ──────────────────────────────────────────────────────────────
    fieldnames = (
        ["dialogue_id", "domain", "question", "expected_value"]
        + [f"{m}_mem_acc"       for m in methods]
        + [f"{m}_q_correct"     for m in methods]
        + [f"{m}_response"      for m in methods]
        + [f"{m}_errors"        for m in methods]
        + [f"{m}_prompt_tokens" for m in methods]
    )
    results_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results", "results.csv")
    with open(results_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("\nSaved detailed results to results/results.csv")


if __name__ == "__main__":
    main()