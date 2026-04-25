import json
import random

PARAPHRASES = {
    # diet
    "vegan":           ["plant-based", "no animal products", "strictly plant-based"],
    "vegetarian":      ["meat-free", "no meat diet", "I do not eat meat"],
    # drink
    "decaf":           ["no caffeine", "caffeine-free", "avoid caffeine"],
    # travel
    "window seat":     ["sit near the window", "seat by the window", "near the window on flights"],
    "budget hotel":    ["cheap hotel", "affordable place to stay", "cheaper places to stay"],
    # food
    "italian":         ["Italian cuisine", "food from Italy", "Italian meals"],
    # hobby / work
    "painting":        ["doing art", "creative artwork", "making art"],
    "python":          ["Python programming", "coding in Python", "practice coding in Python"],
    # times
    "4pm":             ["around 4pm", "later in the afternoon", "4 in the afternoon"],
    "3pm":             ["around 3pm", "mid-afternoon", "3 in the afternoon"],
    "10am":            ["around 10am", "mid-morning", "10 in the morning"],
    # allergy
    "peanuts":         ["nuts like peanuts", "peanut ingredients", "anything with peanuts"],
    # extra surfaces
    "allergic to":     ["have an allergy to", "cannot have"],
    "I prefer":        ["I tend to choose", "I usually go with", "My preference is"],
    "I really like":   ["I enjoy", "I love", "I am a big fan of"],
    "I only drink":    ["I exclusively drink", "I stick to", "I always choose"],
}


def paraphrase_text(text: str) -> str:
    result = text.lower()
    for key, options in PARAPHRASES.items():
        if key in result and random.random() < 0.7:
            result = result.replace(key, random.choice(options), 1)
    return result


def augment_dialogues(input_file: str, output_file: str) -> None:
    with open(input_file) as f:
        data = json.load(f)

    for dialogue in data:
        for turn in dialogue["turns"]:
            if turn["role"] == "user":
                turn["text"] = paraphrase_text(turn["text"])

    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Augmented {len(data)} dialogues → {output_file}")


if __name__ == "__main__":
    random.seed(42)
    augment_dialogues(
        "data/dialogues_harder.json",
        "data/dialogues_harder_augmented.json",
    )