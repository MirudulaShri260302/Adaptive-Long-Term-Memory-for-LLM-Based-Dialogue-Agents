def evaluate_memory(memory, memory_facts):
    correct = 0
    total = len(memory_facts)

    for fact in memory_facts:
        key = fact["key"]
        value = fact["value"]

        if key in memory and memory[key] == value:
            correct += 1

    return {
        "correct": correct,
        "total": total,
        "accuracy": correct / total if total > 0 else 0
    }


def evaluate_test_query_response(response, expected_value):
    response_lower = response.lower()
    expected_lower = expected_value.lower()

    return expected_lower in response_lower