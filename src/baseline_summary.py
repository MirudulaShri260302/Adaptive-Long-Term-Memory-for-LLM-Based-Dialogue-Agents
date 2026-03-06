def run_summary_baseline(dialogue):
    """
    Weak summary baseline that simulates imperfect summarization.
    Earlier facts may override later ones (common summarization error).
    """

    summary = {}

    for turn in dialogue["turns"]:
        if turn["role"] != "user":
            continue

        text = turn["text"].lower()

        # diet
        if "vegetarian" in text and "diet" not in summary:
            summary["diet"] = "vegetarian"

        if "vegan" in text:
            summary["diet"] = "vegan"

        # allergy
        if "peanut" in text and "allergy" not in summary:
            summary["allergy"] = "peanuts"

        # meeting times (keep first seen sometimes)
        if "3pm" in text and "meeting_time" not in summary:
            summary["meeting_time"] = "3pm"

        if "10am" in text and "meeting_time" not in summary:
            summary["meeting_time"] = "10am"

        if "4pm" in text:
            summary["meeting_time"] = "4pm"

        # seat
        if "window" in text and "seat_preference" not in summary:
            summary["seat_preference"] = "window"

        # hobby
        if "painting" in text and "hobby" not in summary:
            summary["hobby"] = "painting"

        # cuisine
        if "italian" in text and "favorite_cuisine" not in summary:
            summary["favorite_cuisine"] = "italian"

        # hotel
        if "budget hotel" in text and "hotel_type" not in summary:
            summary["hotel_type"] = "budget"

        # drink
        if "decaf" in text and "drink_preference" not in summary:
            summary["drink_preference"] = "decaf"

        # coding
        if "python" in text and "coding_language" not in summary:
            summary["coding_language"] = "python"

    return summary