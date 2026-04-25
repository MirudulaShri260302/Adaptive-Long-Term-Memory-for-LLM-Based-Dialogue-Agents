def classify_turn(text):
    text_lower = text.lower()

    if ("vegetarian" in text_lower or "do not eat meat" in text_lower or "vegetarian meals" in text_lower) and "vegan" not in text_lower:
        return ("STORE", "diet", "vegetarian")

    if ("now i am vegan" in text_lower or "switched to vegan" in text_lower or
        "i am vegan" in text_lower or "animal products" in text_lower):
        return ("STORE", "diet", "vegan")

    if "allergic to peanuts" in text_lower or "peanuts are something i am allergic to" in text_lower or "cannot eat peanuts" in text_lower:
        return ("STORE", "allergy", "peanuts")

    if "window seat" in text_lower or "by the window" in text_lower or "window seats are my preference" in text_lower:
        return ("STORE", "seat_preference", "window")

    if "3pm" in text_lower:
        return ("STORE", "meeting_time", "3pm")

    if "10am" in text_lower:
        return ("STORE", "meeting_time", "10am")

    if "4pm" in text_lower:
        return ("STORE", "meeting_time", "4pm")

    if "painting" in text_lower:
        return ("STORE", "hobby", "painting")

    if "italian food" in text_lower:
        return ("STORE", "favorite_cuisine", "italian")

    if "budget hotels" in text_lower or "budget hotel" in text_lower:
        return ("STORE", "hotel_type", "budget")

    if "decaf coffee" in text_lower or "drink decaf" in text_lower:
        return ("STORE", "drink_preference", "decaf")

    if "prefer using python" in text_lower or "using python" in text_lower:
        return ("STORE", "coding_language", "python")

    return ("DROP", None, None)