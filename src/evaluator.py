"""
Evaluator with error categorization for the final report's error analysis.

Error types
-----------
slot_extraction_failure : the key was never stored at all (fact completely missed)
update_failure          : the key exists but holds a stale/wrong value
                          (e.g., memory has "vegetarian" when it should be "vegan")
"""

from collections import Counter


# ── Per-dialogue evaluation ───────────────────────────────────────────────────

def evaluate_memory(memory: dict, memory_facts: list[dict]) -> dict:
    """
    Compare the stored memory against expected facts.
    Returns accuracy + a list of categorized errors.
    """
    correct = 0
    errors  = []

    for fact in memory_facts:
        key      = fact["key"]
        expected = fact["value"]

        if key not in memory:
            errors.append({
                "error_type": "slot_extraction_failure",
                "key":        key,
                "expected":   expected,
                "got":        None,
            })
        elif memory[key] != expected:
            errors.append({
                "error_type": "update_failure",
                "key":        key,
                "expected":   expected,
                "got":        memory[key],
            })
        else:
            correct += 1

    total = len(memory_facts)
    return {
        "correct":  correct,
        "total":    total,
        "accuracy": correct / total if total > 0 else 0.0,
        "errors":   errors,
    }


def evaluate_test_query_response(response: str, expected_value: str) -> bool:
    return expected_value.lower() in response.lower()


# ── Aggregate error analysis across all dialogues ────────────────────────────

def aggregate_errors(all_error_lists: list[list[dict]]) -> dict:
    """
    Flatten per-dialogue error lists and count by type and key.

    Parameters
    ----------
    all_error_lists : list of error lists, one per dialogue.

    Returns
    -------
    dict with:
        by_type   – Counter of error_type strings
        by_key    – Counter of (key, error_type) pairs
        raw       – flat list of all error dicts
    """
    flat   = [e for errors in all_error_lists for e in errors]
    by_type = Counter(e["error_type"] for e in flat)
    by_key  = Counter((e["key"], e["error_type"]) for e in flat)
    return {"by_type": by_type, "by_key": by_key, "raw": flat}


def print_error_summary(label: str, error_agg: dict) -> None:
    print(f"\n── Error summary: {label} ──")
    print("  By type:")
    for etype, count in sorted(error_agg["by_type"].items()):
        print(f"    {etype:<30} {count}")
    print("  By key + type:")
    for (key, etype), count in sorted(error_agg["by_key"].items()):
        print(f"    {key:<22} {etype:<30} {count}")