def run_window_baseline(dialogue, k=2):
    """
    Baseline that only looks at the last k turns of the dialogue.
    """

    memory = {}

    recent_turns = dialogue["turns"][-k:]

    for turn in recent_turns:
        if turn["role"] == "user":

            text = turn["text"].lower()

            if "vegetarian" in text:
                memory["diet"] = "vegetarian"

            if "vegan" in text:
                memory["diet"] = "vegan"

            if "allergic to peanuts" in text:
                memory["allergy"] = "peanuts"

            if "window seat" in text:
                memory["seat_preference"] = "window"

            if "3pm" in text:
                memory["meeting_time"] = "3pm"

            if "10am" in text:
                memory["meeting_time"] = "10am"

            if "painting" in text:
                memory["hobby"] = "painting"

            if "italian food" in text:
                memory["favorite_cuisine"] = "italian"

            if "budget hotel" in text or "budget hotels" in text:
                memory["hotel_type"] = "budget"

            if "decaf" in text:
                memory["drink_preference"] = "decaf"

            if "python" in text:
                memory["coding_language"] = "python"

    return memory