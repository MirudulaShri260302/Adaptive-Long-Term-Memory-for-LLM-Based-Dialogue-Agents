import json
import random


DISTRACTOR_USER_TURNS = [
    "I watched a movie yesterday.",
    "The weather has been nice this week.",
    "I have been busy with classes lately.",
    "Do you think weekends go by too fast?",
    "I want to travel somewhere new this year.",
    "I spent time cleaning my room today.",
    "I enjoy listening to music while studying.",
    "I need to finish some work later today.",
    "I was talking to my friend about vacation plans.",
    "I want to be more productive this month.",
    "I have been trying to sleep earlier.",
    "I was reading about different career options.",
    "I might go for a walk this evening.",
    "I have a lot of assignments this week.",
    "Sometimes I just want a quiet day at home."
]

DISTRACTOR_ASSISTANT_TURNS = [
    "That sounds interesting.",
    "I understand.",
    "That makes sense.",
    "Sounds like a good plan.",
    "I hope it goes well.",
    "That seems nice.",
    "I can see why you feel that way.",
    "That sounds productive.",
    "Hopefully that works out well.",
    "It's good to hear that."
]

# Paraphrase pools
DIET_PHRASES = [
    "I recently became vegetarian.",
    "I do not eat meat anymore.",
    "I only eat vegetarian meals now."
]

VEGAN_UPDATE_PHRASES = [
    "Actually, now I am vegan.",
    "I switched to vegan recently.",
    "I do not eat any animal products now."
]

MEETING_3PM_PHRASES = [
    "Let's schedule our meeting at 3pm tomorrow.",
    "Can we meet tomorrow at 3pm?",
    "Please set the meeting for 3pm."
]

MEETING_4PM_UPDATE_PHRASES = [
    "Actually, let's change the meeting time to 4pm.",
    "Can we move it to 4pm instead?",
    "Please update the meeting to 4pm."
]

WINDOW_SEAT_PHRASES = [
    "I always prefer a window seat when I fly.",
    "I like sitting by the window on flights.",
    "Window seats are my preference."
]

PEANUT_ALLERGY_PHRASES = [
    "I am allergic to peanuts.",
    "Peanuts are something I am allergic to.",
    "I cannot eat peanuts because of an allergy."
]

ITALIAN_FOOD_PHRASES = [
    "I really like Italian food.",
    "Italian food is my favorite.",
    "I usually prefer Italian meals."
]

BUDGET_HOTEL_PHRASES = [
    "I usually prefer budget hotels when I travel.",
    "I like staying in budget hotels.",
    "Budget hotels are usually my preference."
]

DECAF_PHRASES = [
    "I only drink decaf coffee now.",
    "These days I stick to decaf coffee.",
    "I prefer decaf coffee."
]

PYTHON_PHRASES = [
    "I prefer using Python for coding interviews.",
    "Python is my preferred language for interview prep.",
    "I usually practice coding interviews in Python."
]

PAINTING_PHRASES = [
    "My favorite hobby is painting.",
    "I really enjoy painting in my free time.",
    "Painting is my favorite thing to do as a hobby."
]

MEETING_10AM_PHRASES = [
    "Let's move the meeting to 10am on Friday.",
    "Can we reschedule the meeting to 10am on Friday?",
    "Please set the Friday meeting for 10am."
]


MEMORY_TEMPLATES = [
    {
        "domain": "food_preferences",
        "memory_fact": {"type": "preference", "key": "diet", "value": "vegetarian"},
        "user_fact_text": random.choice(DIET_PHRASES),
        "assistant_ack": "That's great! I'll keep that in mind.",
        "test_query": {
            "question": "What kind of dinner should I eat tonight?",
            "expected_key": "diet",
            "expected_value": "vegetarian"
        }
    },
    {
        "domain": "scheduling",
        "memory_fact": {"type": "commitment", "key": "meeting_time", "value": "3pm"},
        "user_fact_text": random.choice(MEETING_3PM_PHRASES),
        "assistant_ack": "Sure, I'll remember that.",
        "test_query": {
            "question": "What time is my meeting tomorrow?",
            "expected_key": "meeting_time",
            "expected_value": "3pm"
        }
    },
    {
        "domain": "travel_preferences",
        "memory_fact": {"type": "preference", "key": "seat_preference", "value": "window"},
        "user_fact_text": random.choice(WINDOW_SEAT_PHRASES),
        "assistant_ack": "Got it, I'll remember that.",
        "test_query": {
            "question": "What kind of seat should I choose for my flight?",
            "expected_key": "seat_preference",
            "expected_value": "window"
        }
    },
    {
        "domain": "allergy",
        "memory_fact": {"type": "constraint", "key": "allergy", "value": "peanuts"},
        "user_fact_text": random.choice(PEANUT_ALLERGY_PHRASES),
        "assistant_ack": "Thanks for telling me. I'll keep that in mind.",
        "test_query": {
            "question": "What dessert would be safe for me?",
            "expected_key": "allergy",
            "expected_value": "peanuts"
        }
    },
    {
        "domain": "hobbies",
        "memory_fact": {"type": "preference", "key": "hobby", "value": "painting"},
        "user_fact_text": random.choice(PAINTING_PHRASES),
        "assistant_ack": "That sounds creative. I'll remember that.",
        "test_query": {
            "question": "What hobby-related activity should I do this weekend?",
            "expected_key": "hobby",
            "expected_value": "painting"
        }
    },
    {
        "domain": "food_preferences",
        "memory_fact": {"type": "preference", "key": "favorite_cuisine", "value": "italian"},
        "user_fact_text": random.choice(ITALIAN_FOOD_PHRASES),
        "assistant_ack": "Nice, I'll keep that in mind.",
        "test_query": {
            "question": "What kind of cuisine should I choose for dinner?",
            "expected_key": "favorite_cuisine",
            "expected_value": "italian"
        }
    },
    {
        "domain": "scheduling",
        "memory_fact": {"type": "commitment", "key": "meeting_time", "value": "10am"},
        "user_fact_text": random.choice(MEETING_10AM_PHRASES),
        "assistant_ack": "Okay, I'll remember that.",
        "test_query": {
            "question": "What time is my meeting on Friday?",
            "expected_key": "meeting_time",
            "expected_value": "10am"
        }
    },
    {
        "domain": "travel_preferences",
        "memory_fact": {"type": "preference", "key": "hotel_type", "value": "budget"},
        "user_fact_text": random.choice(BUDGET_HOTEL_PHRASES),
        "assistant_ack": "Understood, I'll remember that.",
        "test_query": {
            "question": "What kind of hotel should I book?",
            "expected_key": "hotel_type",
            "expected_value": "budget"
        }
    },
    {
        "domain": "health_constraints",
        "memory_fact": {"type": "constraint", "key": "drink_preference", "value": "decaf"},
        "user_fact_text": random.choice(DECAF_PHRASES),
        "assistant_ack": "Got it, I'll remember that.",
        "test_query": {
            "question": "What coffee should I order?",
            "expected_key": "drink_preference",
            "expected_value": "decaf"
        }
    },
    {
        "domain": "work_preferences",
        "memory_fact": {"type": "preference", "key": "coding_language", "value": "python"},
        "user_fact_text": random.choice(PYTHON_PHRASES),
        "assistant_ack": "Makes sense, I'll keep that in mind.",
        "test_query": {
            "question": "Which programming language should I practice with?",
            "expected_key": "coding_language",
            "expected_value": "python"
        }
    }
]


UPDATE_TEMPLATES = [
    {
        "domain": "food_preferences_update",
        "initial_fact": {"type": "preference", "key": "diet", "value": "vegetarian"},
        "initial_user_text": random.choice(DIET_PHRASES),
        "initial_ack": "That's great! I'll keep that in mind.",
        "updated_fact": {"type": "preference", "key": "diet", "value": "vegan"},
        "update_user_text": random.choice(VEGAN_UPDATE_PHRASES),
        "update_ack": "Got it, I'll update that.",
        "test_query": {
            "question": "What kind of dinner should I eat tonight?",
            "expected_key": "diet",
            "expected_value": "vegan"
        }
    },
    {
        "domain": "schedule_update",
        "initial_fact": {"type": "commitment", "key": "meeting_time", "value": "3pm"},
        "initial_user_text": random.choice(MEETING_3PM_PHRASES),
        "initial_ack": "Sure, I'll remember that.",
        "updated_fact": {"type": "commitment", "key": "meeting_time", "value": "4pm"},
        "update_user_text": random.choice(MEETING_4PM_UPDATE_PHRASES),
        "update_ack": "Okay, I'll update the meeting time.",
        "test_query": {
            "question": "What time is my meeting now?",
            "expected_key": "meeting_time",
            "expected_value": "4pm"
        }
    }
]


def generate_distractor_pair():
    user_turn = random.choice(DISTRACTOR_USER_TURNS)
    assistant_turn = random.choice(DISTRACTOR_ASSISTANT_TURNS)

    return [
        {"role": "user", "text": user_turn},
        {"role": "assistant", "text": assistant_turn}
    ]


def generate_long_dialogue(dialogue_id, template, num_turns=60):
    turns = []

    turns.append({"role": "user", "text": template["user_fact_text"]})
    turns.append({"role": "assistant", "text": template["assistant_ack"]})

    while len(turns) < num_turns - 2:
        turns.extend(generate_distractor_pair())

    turns = turns[:num_turns - 2]

    turns.append({"role": "user", "text": template["test_query"]["question"]})
    turns.append({"role": "assistant", "text": "TEST_RESPONSE_PLACEHOLDER"})

    dialogue = {
        "id": f"dialogue_{dialogue_id}",
        "domain": template["domain"],
        "memory_facts": [template["memory_fact"]],
        "turns": turns,
        "test_queries": [template["test_query"]]
    }

    return dialogue


def generate_update_dialogue(dialogue_id, template, num_turns=60):
    turns = []

    turns.append({"role": "user", "text": template["initial_user_text"]})
    turns.append({"role": "assistant", "text": template["initial_ack"]})

    # Add distractors before update
    while len(turns) < (num_turns // 2) - 2:
        turns.extend(generate_distractor_pair())

    turns = turns[:(num_turns // 2) - 2]

    # Add updated fact later
    turns.append({"role": "user", "text": template["update_user_text"]})
    turns.append({"role": "assistant", "text": template["update_ack"]})

    # Add more distractors until final query
    while len(turns) < num_turns - 2:
        turns.extend(generate_distractor_pair())

    turns = turns[:num_turns - 2]

    turns.append({"role": "user", "text": template["test_query"]["question"]})
    turns.append({"role": "assistant", "text": "TEST_RESPONSE_PLACEHOLDER"})

    dialogue = {
        "id": f"dialogue_{dialogue_id}",
        "domain": template["domain"],
        "memory_facts": [template["updated_fact"]],
        "turns": turns,
        "test_queries": [template["test_query"]]
    }

    return dialogue


def generate_dataset(num_regular=20, num_update=2, min_turns=50, max_turns=100):
    dialogues = []

    dialogue_id = 1

    for i in range(num_regular):
        template = MEMORY_TEMPLATES[i % len(MEMORY_TEMPLATES)]
        num_turns = random.randint(min_turns, max_turns)
        dialogue = generate_long_dialogue(dialogue_id, template, num_turns=num_turns)
        dialogues.append(dialogue)
        dialogue_id += 1

    for i in range(num_update):
        template = UPDATE_TEMPLATES[i % len(UPDATE_TEMPLATES)]
        num_turns = random.randint(min_turns, max_turns)
        dialogue = generate_update_dialogue(dialogue_id, template, num_turns=num_turns)
        dialogues.append(dialogue)
        dialogue_id += 1

    return dialogues


def save_dataset(dialogues, output_path="data/dialogues_long.json"):
    with open(output_path, "w") as f:
        json.dump(dialogues, f, indent=2)


def main():
    random.seed(42)

    dialogues = generate_dataset(num_regular=20, num_update=2, min_turns=50, max_turns=100)
    save_dataset(dialogues, "data/dialogues_long.json")

    print(f"Generated {len(dialogues)} dialogues.")
    print("Saved to data/dialogues_long.json")


if __name__ == "__main__":
    main()