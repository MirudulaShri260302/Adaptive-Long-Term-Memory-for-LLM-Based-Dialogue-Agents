import json

def load_dialogues(path):
    with open(path, "r") as f:
        return json.load(f)

def main():

    dialogues = load_dialogues("data/dialogues.json")

    for d in dialogues:
        print("Dialogue ID:", d["id"])
        print("Memory facts:", d["memory_facts"])
        print()

if __name__ == "__main__":
    main()
