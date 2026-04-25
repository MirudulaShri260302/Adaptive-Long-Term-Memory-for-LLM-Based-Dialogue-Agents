import json
import csv

from selector import classify_turn
from memory_slots import initialize_memory, update_memory
from evaluator import evaluate_memory, evaluate_test_query_response
from baseline_window import run_window_baseline
from baseline_summary import run_summary_baseline
from prompt_builder import generate_memory_based_response


def load_dialogues(path):
    with open(path, "r") as f:
        return json.load(f)


def run_adaptive_memory(dialogue):
    memory = initialize_memory()

    for turn in dialogue["turns"]:
        if turn["role"] == "user":
            action, key, value = classify_turn(turn["text"])
            if action == "STORE":
                update_memory(memory, key, value)

    return memory


def main():
    dialogues = load_dialogues("data/dialogues_long.json")

    adaptive_correct = 0
    adaptive_total = 0

    window_correct = 0
    window_total = 0

    summary_correct = 0
    summary_total = 0

    adaptive_query_correct = 0
    window_query_correct = 0
    summary_query_correct = 0
    total_queries = 0

    rows = []

    for dialogue in dialogues:
        adaptive_memory = run_adaptive_memory(dialogue)
        adaptive_eval = evaluate_memory(adaptive_memory, dialogue["memory_facts"])

        window_memory = run_window_baseline(dialogue, k=2)
        window_eval = evaluate_memory(window_memory, dialogue["memory_facts"])

        summary_memory = run_summary_baseline(dialogue)
        summary_eval = evaluate_memory(summary_memory, dialogue["memory_facts"])

        adaptive_correct += adaptive_eval["correct"]
        adaptive_total += adaptive_eval["total"]

        window_correct += window_eval["correct"]
        window_total += window_eval["total"]

        summary_correct += summary_eval["correct"]
        summary_total += summary_eval["total"]

        print("=" * 60)
        print("Dialogue:", dialogue["id"])

        print("Adaptive memory:", adaptive_memory)
        print("Adaptive evaluation:", adaptive_eval)

        print("Window memory:", window_memory)
        print("Window evaluation:", window_eval)

        print("Summary memory:", summary_memory)
        print("Summary evaluation:", summary_eval)

        for test_query in dialogue["test_queries"]:
            question = test_query["question"]
            expected_value = test_query["expected_value"]

            adaptive_response = generate_memory_based_response(adaptive_memory, question)
            window_response = generate_memory_based_response(window_memory, question)
            summary_response = generate_memory_based_response(summary_memory, question)

            adaptive_ok = evaluate_test_query_response(adaptive_response, expected_value)
            window_ok = evaluate_test_query_response(window_response, expected_value)
            summary_ok = evaluate_test_query_response(summary_response, expected_value)

            if adaptive_ok:
                adaptive_query_correct += 1
            if window_ok:
                window_query_correct += 1
            if summary_ok:
                summary_query_correct += 1

            total_queries += 1

            print("Question:", question)
            print("Adaptive response:", adaptive_response, "| Correct:", adaptive_ok)
            print("Window response:", window_response, "| Correct:", window_ok)
            print("Summary response:", summary_response, "| Correct:", summary_ok)

            rows.append({
                "dialogue_id": dialogue["id"],
                "domain": dialogue["domain"],
                "expected_value": expected_value,
                "adaptive_memory_accuracy": adaptive_eval["accuracy"],
                "window_memory_accuracy": window_eval["accuracy"],
                "summary_memory_accuracy": summary_eval["accuracy"],
                "adaptive_query_correct": int(adaptive_ok),
                "window_query_correct": int(window_ok),
                "summary_query_correct": int(summary_ok),
                "adaptive_response": adaptive_response,
                "window_response": window_response,
                "summary_response": summary_response
            })

    print("\nFINAL RESULTS")
    print("=" * 60)

    adaptive_memory_acc = adaptive_correct / adaptive_total if adaptive_total else 0
    window_memory_acc = window_correct / window_total if window_total else 0
    summary_memory_acc = summary_correct / summary_total if summary_total else 0

    adaptive_query_acc = adaptive_query_correct / total_queries if total_queries else 0
    window_query_acc = window_query_correct / total_queries if total_queries else 0
    summary_query_acc = summary_query_correct / total_queries if total_queries else 0

    print("Adaptive memory accuracy:", adaptive_memory_acc)
    print("Window memory accuracy:", window_memory_acc)
    print("Summary memory accuracy:", summary_memory_acc)

    print("Adaptive query accuracy:", adaptive_query_acc)
    print("Window query accuracy:", window_query_acc)
    print("Summary query accuracy:", summary_query_acc)

    with open("results/results.csv", "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "dialogue_id",
                "domain",
                "expected_value",
                "adaptive_memory_accuracy",
                "window_memory_accuracy",
                "summary_memory_accuracy",
                "adaptive_query_correct",
                "window_query_correct",
                "summary_query_correct",
                "adaptive_response",
                "window_response",
                "summary_response"
            ]
        )
        writer.writeheader()
        writer.writerows(rows)

    print("Saved detailed results to results/results.csv")


if __name__ == "__main__":
    main()