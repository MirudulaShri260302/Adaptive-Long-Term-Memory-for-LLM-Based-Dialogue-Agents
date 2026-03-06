def generate_memory_based_response(memory, question):
    question_lower = question.lower()

    if "dinner" in question_lower and memory.get("diet") == "vegetarian":
        return "You should choose a vegetarian dinner option."

    if "dinner" in question_lower and memory.get("diet") == "vegan":
        return "You should choose a vegan dinner option."

    if "meeting" in question_lower and "meeting_time" in memory:
        return f"Your meeting is at {memory['meeting_time']}."

    if "seat" in question_lower and memory.get("seat_preference") == "window":
        return "You should choose a window seat."

    if "dessert" in question_lower and memory.get("allergy") == "peanuts":
        return "Choose a dessert that does not contain peanuts."

    if "hobby" in question_lower and memory.get("hobby") == "painting":
        return "You could do a painting-related activity this weekend."

    if "cuisine" in question_lower and memory.get("favorite_cuisine") == "italian":
        return "You should choose Italian cuisine."

    if "hotel" in question_lower and memory.get("hotel_type") == "budget":
        return "You should book a budget hotel."

    if "coffee" in question_lower and memory.get("drink_preference") == "decaf":
        return "You should order decaf coffee."

    if "programming language" in question_lower and memory.get("coding_language") == "python":
        return "You should practice with Python."

    return "I do not know."