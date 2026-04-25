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
    "Sometimes I just want a quiet day at home.",
    # Tricky distractors — facts about OTHER people, not the user
    "My friend is vegetarian, but I am not talking about myself.",
    "I saw a vegan restaurant downtown yesterday.",
    "Someone in my class likes Italian food.",
    "My roommate drinks regular coffee every morning.",
    "I read an article about budget hotels last night.",
    "My colleague prefers Python but I have not decided yet.",
    "A friend of mine is allergic to tree nuts.",
    "I heard that painting is a relaxing hobby.",
    "My sister just rescheduled her meeting to 3pm.",
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
    "It is good to hear that.",
]

# ── Templates ─────────────────────────────────────────────────────────────────
# Each template has:
#   important_turns  – ordered list; index 0 is inserted early, rest are later
#   memory_facts     – the FINAL expected state after all updates
#   test_queries     – one per memory fact
#
# Update templates: important_turns[0] sets an initial value that is later
# overwritten by a subsequent turn.  memory_facts reflects the FINAL value.

HARD_TEMPLATES = [
    # ── Original 5 ────────────────────────────────────────────────────────────
    {
        "id_prefix": "diet_update_multi",
        "domain": "food_preferences",
        "memory_facts": [
            {"type": "preference", "key": "diet",             "value": "vegan"},
            {"type": "constraint", "key": "drink_preference", "value": "decaf"},
        ],
        "important_turns": [
            "I recently became vegetarian.",
            "I only drink decaf coffee now.",
            "Actually, I switched to vegan meals recently.",
        ],
        "test_queries": [
            {"question": "What kind of dinner should I eat tonight?",
             "expected_key": "diet", "expected_value": "vegan"},
            {"question": "What coffee should I order?",
             "expected_key": "drink_preference", "expected_value": "decaf"},
        ],
    },
    {
        "id_prefix": "meeting_update_multi",
        "domain": "scheduling",
        "memory_facts": [
            {"type": "commitment", "key": "meeting_time",    "value": "4pm"},
            {"type": "preference", "key": "seat_preference", "value": "window"},
        ],
        "important_turns": [
            "Let us schedule the meeting at 3pm tomorrow.",
            "I always prefer a window seat when I fly.",
            "Actually, please move the meeting to 4pm.",
        ],
        "test_queries": [
            {"question": "What time is my meeting now?",
             "expected_key": "meeting_time", "expected_value": "4pm"},
            {"question": "What kind of seat should I choose for my flight?",
             "expected_key": "seat_preference", "expected_value": "window"},
        ],
    },
    {
        "id_prefix": "travel_food_combo",
        "domain": "travel_food",
        "memory_facts": [
            {"type": "preference", "key": "hotel_type",       "value": "budget"},
            {"type": "preference", "key": "favorite_cuisine", "value": "italian"},
        ],
        "important_turns": [
            "I usually prefer budget hotels when I travel.",
            "I really like Italian food.",
        ],
        "test_queries": [
            {"question": "What kind of hotel should I book?",
             "expected_key": "hotel_type", "expected_value": "budget"},
            {"question": "What kind of cuisine should I choose for dinner?",
             "expected_key": "favorite_cuisine", "expected_value": "italian"},
        ],
    },
    {
        "id_prefix": "health_allergy_combo",
        "domain": "health_constraints",
        "memory_facts": [
            {"type": "constraint", "key": "allergy",          "value": "peanuts"},
            {"type": "constraint", "key": "drink_preference", "value": "decaf"},
        ],
        "important_turns": [
            "Peanuts are something I am allergic to.",
            "I prefer decaf coffee these days.",
        ],
        "test_queries": [
            {"question": "What dessert would be safe for me?",
             "expected_key": "allergy", "expected_value": "peanuts"},
            {"question": "What coffee should I order?",
             "expected_key": "drink_preference", "expected_value": "decaf"},
        ],
    },
    {
        "id_prefix": "coding_hobby_combo",
        "domain": "work_and_hobbies",
        "memory_facts": [
            {"type": "preference", "key": "coding_language", "value": "python"},
            {"type": "preference", "key": "hobby",           "value": "painting"},
        ],
        "important_turns": [
            "I prefer using Python for coding interviews.",
            "My favorite hobby is painting.",
        ],
        "test_queries": [
            {"question": "Which programming language should I practice with?",
             "expected_key": "coding_language", "expected_value": "python"},
            {"question": "What hobby-related activity should I do this weekend?",
             "expected_key": "hobby", "expected_value": "painting"},
        ],
    },

    # ── New: triple diet update chain ─────────────────────────────────────────
    {
        "id_prefix": "diet_triple_update",
        "domain": "food_preferences",
        "memory_facts": [
            {"type": "preference", "key": "diet", "value": "vegan"},
        ],
        "important_turns": [
            "I have started eating less meat lately.",
            "I am fully vegetarian now, no meat at all.",
            "I have gone fully vegan this month.",
        ],
        "test_queries": [
            {"question": "What kind of dinner should I eat tonight?",
             "expected_key": "diet", "expected_value": "vegan"},
        ],
    },

    # ── New: meeting rescheduled twice ────────────────────────────────────────
    {
        "id_prefix": "meeting_triple_update",
        "domain": "scheduling",
        "memory_facts": [
            {"type": "commitment", "key": "meeting_time", "value": "4pm"},
        ],
        "important_turns": [
            "The meeting is set for 10am.",
            "We moved the meeting to 3pm.",
            "Actually the meeting is now at 4pm.",
        ],
        "test_queries": [
            {"question": "What time is my meeting now?",
             "expected_key": "meeting_time", "expected_value": "4pm"},
        ],
    },

    # ── New: allergy + diet combo with update ─────────────────────────────────
    {
        "id_prefix": "allergy_diet_update",
        "domain": "health_constraints",
        "memory_facts": [
            {"type": "constraint", "key": "allergy", "value": "peanuts"},
            {"type": "preference", "key": "diet",    "value": "vegan"},
        ],
        "important_turns": [
            "I cannot eat peanuts, I am allergic.",
            "I have been eating vegetarian for a while.",
            "I recently went fully vegan.",
        ],
        "test_queries": [
            {"question": "What dessert would be safe for me?",
             "expected_key": "allergy", "expected_value": "peanuts"},
            {"question": "What kind of meal should I order tonight?",
             "expected_key": "diet", "expected_value": "vegan"},
        ],
    },

    # ── New: travel preferences triple combo ──────────────────────────────────
    {
        "id_prefix": "travel_triple_combo",
        "domain": "travel_preferences",
        "memory_facts": [
            {"type": "preference", "key": "seat_preference", "value": "window"},
            {"type": "preference", "key": "hotel_type",      "value": "budget"},
            {"type": "preference", "key": "drink_preference","value": "decaf"},
        ],
        "important_turns": [
            "I like sitting by the window on flights.",
            "I tend to book budget hotels to save money.",
            "I switched to decaf coffee a few months ago.",
        ],
        "test_queries": [
            {"question": "What kind of seat should I choose for my flight?",
             "expected_key": "seat_preference", "expected_value": "window"},
            {"question": "What kind of hotel should I book?",
             "expected_key": "hotel_type", "expected_value": "budget"},
            {"question": "What coffee should I order?",
             "expected_key": "drink_preference", "expected_value": "decaf"},
        ],
    },

    # ── New: work combo with update ───────────────────────────────────────────
    {
        "id_prefix": "work_combo_update",
        "domain": "work_and_scheduling",
        "memory_facts": [
            {"type": "preference", "key": "coding_language", "value": "python"},
            {"type": "commitment", "key": "meeting_time",    "value": "4pm"},
        ],
        "important_turns": [
            "I have been using Python for all my projects.",
            "Can we schedule the meeting at 3pm?",
            "On second thought, let us move the meeting to 4pm.",
        ],
        "test_queries": [
            {"question": "Which programming language should I practice with?",
             "expected_key": "coding_language", "expected_value": "python"},
            {"question": "What time is my meeting now?",
             "expected_key": "meeting_time", "expected_value": "4pm"},
        ],
    },

    # ── New: hobby + diet combo ───────────────────────────────────────────────
    {
        "id_prefix": "hobby_diet_combo",
        "domain": "lifestyle",
        "memory_facts": [
            {"type": "preference", "key": "hobby", "value": "painting"},
            {"type": "preference", "key": "diet",  "value": "vegetarian"},
        ],
        "important_turns": [
            "I love painting in my free time.",
            "I do not eat meat anymore.",
        ],
        "test_queries": [
            {"question": "What hobby-related activity should I do this weekend?",
             "expected_key": "hobby", "expected_value": "painting"},
            {"question": "What kind of dinner should I eat tonight?",
             "expected_key": "diet", "expected_value": "vegetarian"},
        ],
    },

    # ── New: cuisine + allergy combo ──────────────────────────────────────────
    {
        "id_prefix": "cuisine_allergy_combo",
        "domain": "food_and_health",
        "memory_facts": [
            {"type": "preference", "key": "favorite_cuisine", "value": "italian"},
            {"type": "constraint", "key": "allergy",          "value": "peanuts"},
        ],
        "important_turns": [
            "I really enjoy Italian food.",
            "I have a peanut allergy so I need to be careful.",
        ],
        "test_queries": [
            {"question": "What kind of cuisine should I choose for dinner?",
             "expected_key": "favorite_cuisine", "expected_value": "italian"},
            {"question": "What dessert would be safe for me?",
             "expected_key": "allergy", "expected_value": "peanuts"},
        ],
    },

    # ── New: single slot, very long dialogue, heavy distractor load ───────────
    {
        "id_prefix": "single_slot_heavy_distractor",
        "domain": "food_preferences",
        "memory_facts": [
            {"type": "preference", "key": "diet", "value": "vegan"},
        ],
        "important_turns": [
            "I follow a vegan diet.",
        ],
        "test_queries": [
            {"question": "What kind of dinner should I eat tonight?",
             "expected_key": "diet", "expected_value": "vegan"},
        ],
    },

    # ── New: drink + coding combo ─────────────────────────────────────────────
    {
        "id_prefix": "drink_coding_combo",
        "domain": "work_lifestyle",
        "memory_facts": [
            {"type": "constraint", "key": "drink_preference", "value": "decaf"},
            {"type": "preference", "key": "coding_language",  "value": "python"},
        ],
        "important_turns": [
            "I only drink decaf these days.",
            "I prefer coding in Python.",
        ],
        "test_queries": [
            {"question": "What coffee should I order?",
             "expected_key": "drink_preference", "expected_value": "decaf"},
            {"question": "Which programming language should I practice with?",
             "expected_key": "coding_language", "expected_value": "python"},
        ],
    },

    # ── New: four-slot combo, no updates ─────────────────────────────────────
    {
        "id_prefix": "four_slot_combo",
        "domain": "mixed",
        "memory_facts": [
            {"type": "preference", "key": "diet",             "value": "vegetarian"},
            {"type": "preference", "key": "seat_preference",  "value": "window"},
            {"type": "preference", "key": "favorite_cuisine", "value": "italian"},
            {"type": "preference", "key": "hobby",            "value": "painting"},
        ],
        "important_turns": [
            "I am vegetarian.",
            "I always book window seats on flights.",
            "I enjoy Italian food the most.",
            "Painting is my favorite way to relax.",
        ],
        "test_queries": [
            {"question": "What kind of dinner should I eat tonight?",
             "expected_key": "diet", "expected_value": "vegetarian"},
            {"question": "What kind of seat should I choose for my flight?",
             "expected_key": "seat_preference", "expected_value": "window"},
            {"question": "What kind of cuisine should I choose for dinner?",
             "expected_key": "favorite_cuisine", "expected_value": "italian"},
            {"question": "What hobby-related activity should I do this weekend?",
             "expected_key": "hobby", "expected_value": "painting"},
        ],
    },
]


# ── Dialogue builder ──────────────────────────────────────────────────────────

def generate_distractor_pair():
    return [
        {"role": "user",      "text": random.choice(DISTRACTOR_USER_TURNS)},
        {"role": "assistant", "text": random.choice(DISTRACTOR_ASSISTANT_TURNS)},
    ]


def generate_hard_dialogue(dialogue_id, template, min_turns=60, max_turns=100):
    total_turns = random.randint(min_turns, max_turns)
    turns = []

    # Insert first important turn early
    turns.append({"role": "user",      "text": template["important_turns"][0]})
    turns.append({"role": "assistant", "text": "Got it, I will remember that."})

    # Fill ~1/3 of dialogue with distractors
    while len(turns) < total_turns // 3:
        turns.extend(generate_distractor_pair())

    # Insert remaining important turns, separated by distractors
    for important_text in template["important_turns"][1:]:
        turns.append({"role": "user",      "text": important_text})
        turns.append({"role": "assistant", "text": "Okay, I will keep that in mind."})
        while len(turns) < min(total_turns - 10, len(turns) + 8):
            turns.extend(generate_distractor_pair())

    # Trim before final queries
    max_before_queries = total_turns - (2 * len(template["test_queries"]))
    turns = turns[:max_before_queries]

    # Append test queries
    for query in template["test_queries"]:
        turns.append({"role": "user",      "text": query["question"]})
        turns.append({"role": "assistant", "text": "TEST_RESPONSE_PLACEHOLDER"})

    return {
        "id":           f"hard_dialogue_{dialogue_id}",
        "domain":       template["domain"],
        "memory_facts": template["memory_facts"],
        "turns":        turns,
        "test_queries": template["test_queries"],
    }


def generate_hard_dataset(num_dialogues=75):
    dialogues = []
    for i in range(num_dialogues):
        template = HARD_TEMPLATES[i % len(HARD_TEMPLATES)]
        dialogue = generate_hard_dialogue(i + 1, template)
        dialogues.append(dialogue)
    return dialogues


def save_dataset(dialogues, output_path):
    with open(output_path, "w") as f:
        json.dump(dialogues, f, indent=2)


def main():
    random.seed(42)
    dialogues = generate_hard_dataset(num_dialogues=75)
    save_dataset(dialogues, "data/dialogues_harder.json")
    print(f"Generated {len(dialogues)} harder dialogues across {len(HARD_TEMPLATES)} templates.")
    print("Saved to data/dialogues_harder.json")


if __name__ == "__main__":
    main()