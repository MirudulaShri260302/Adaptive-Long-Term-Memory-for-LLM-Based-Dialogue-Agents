def generate_memory_based_response(memory, question):
    question_lower = question.lower()

    # cuisine questions must be checked before dinner/meal questions
    if "cuisine" in question_lower:
        if "favorite_cuisine" in memory:
            return f"You should choose {memory['favorite_cuisine'].capitalize()} cuisine."
        return "I do not know."

    if "dessert" in question_lower or "safe for me" in question_lower:
        if "allergy" in memory:
            return f"Choose a dessert that does not contain {memory['allergy']}."
        return "I do not know."

    if "coffee" in question_lower or "drink" in question_lower:
        if "drink_preference" in memory:
            return f"You should order {memory['drink_preference']} coffee."
        return "I do not know."

    if "seat" in question_lower or "flight" in question_lower:
        if "seat_preference" in memory:
            return f"You should choose a {memory['seat_preference']} seat."
        return "I do not know."

    if "hotel" in question_lower:
        if "hotel_type" in memory:
            return f"You should book a {memory['hotel_type']} hotel."
        return "I do not know."

    if "programming language" in question_lower or "practice with" in question_lower or "coding" in question_lower:
        if "coding_language" in memory:
            return f"You should practice with {memory['coding_language'].capitalize()}."
        return "I do not know."

    if "hobby" in question_lower or "activity should i do" in question_lower:
        if "hobby" in memory:
            return f"You could do a {memory['hobby']}-related activity this weekend."
        return "I do not know."

    if "meeting" in question_lower or "what time" in question_lower:
        if "meeting_time" in memory:
            return f"Your meeting is at {memory['meeting_time']}."
        return "I do not know."

    if "dinner" in question_lower or "eat tonight" in question_lower or "meal" in question_lower:
        if "diet" in memory:
            return f"You should choose a {memory['diet']} dinner option."
        return "I do not know."

    return "I do not know."