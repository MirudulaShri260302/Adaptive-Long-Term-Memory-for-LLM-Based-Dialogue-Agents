from collections import OrderedDict
from selector_llm import classify_turn_llm


def run_summary_baseline(dialogue, max_slots=3):
    """
    Lossy running-summary baseline.
    Keeps only the most recent few memory slots, so older details may be dropped.
    """
    summary_memory = OrderedDict()

    for turn in dialogue["turns"]:
        if turn["role"] != "user":
            continue

        action, key, value = classify_turn_llm(turn["text"])

        if action == "STORE" and key is not None:
            if key in summary_memory:
                del summary_memory[key]

            summary_memory[key] = value

            while len(summary_memory) > max_slots:
                summary_memory.popitem(last=False)

    return dict(summary_memory)