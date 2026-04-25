import json
import anthropic

_client = None

def _get_client():
    global _client
    if _client is None:
        _client = anthropic.Anthropic()   # reads ANTHROPIC_API_KEY from env
    return _client


SYSTEM_PROMPT = """\
You are a memory classification assistant for a dialogue agent.

Analyze the user turn and decide what to do with it.
Respond ONLY with a single valid JSON object — no explanation, no extra text.

Rules:
- STORE  → the turn contains a stable fact, preference, constraint, or commitment
           that belongs to THE USER THEMSELVES (not their friend, roommate, or classmate)
- DROP   → irrelevant small talk, or the fact belongs to someone else
- KEEP   → relevant to the conversation but not a stable storable fact

If action is STORE you must also provide "key" and "value".

Allowed keys and their normalized values:
  diet              → "vegan" | "vegetarian"
  allergy           → "peanuts"
  drink_preference  → "decaf"
  meeting_time      → "3pm" | "4pm" | "10am"
  seat_preference   → "window"
  hotel_type        → "budget"
  favorite_cuisine  → "italian"
  hobby             → "painting"
  coding_language   → "python"

Examples:
  "I recently switched to a vegan diet."
  → {"action": "STORE", "key": "diet", "value": "vegan"}

  "My friend is vegetarian, but I am not talking about myself."
  → {"action": "DROP"}

  "I was watching a movie last night."
  → {"action": "DROP"}

  "Actually, please move the meeting to 4pm."
  → {"action": "STORE", "key": "meeting_time", "value": "4pm"}

  "Can you help me with something?"
  → {"action": "KEEP"}
"""


def classify_turn_llm(text: str) -> tuple[str, str | None, str | None]:
    """
    True LLM-based selector. Calls Claude to classify a user turn.
    Returns (action, key, value).
    Falls back to rule-based logic if the API call fails.
    """
    try:
        client = _get_client()
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=60,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": f"User turn: {text}"}]
        )
        raw = response.content[0].text.strip()
        result = json.loads(raw)

        action = result.get("action", "KEEP")
        key    = result.get("key")
        value  = result.get("value")
        return action, key, value

    except Exception:
        return _rule_based_fallback(text)


# ── Fallback (used only when the API call fails) ──────────────────────────────

def _rule_based_fallback(text: str) -> tuple[str, str | None, str | None]:
    t = text.lower()

    drop_patterns = [
        "weather", "movie", "cleaning my room", "music while studying",
        "walk this evening", "vacation plans", "assignments this week",
        "quiet day at home", "my friend", "my roommate", "someone in my class",
    ]
    if any(p in t for p in drop_patterns):
        return "DROP", None, None

    if "vegan" in t or "plant-based" in t:
        return "STORE", "diet", "vegan"
    if "vegetarian" in t or "meat-free" in t or "don't eat meat" in t or "do not eat meat" in t:
        return "STORE", "diet", "vegetarian"
    if "decaf" in t or "avoid caffeine" in t or "caffeine-free" in t:
        return "STORE", "drink_preference", "decaf"
    if "peanut" in t and ("allergic" in t or "allergy" in t or "cannot eat" in t):
        return "STORE", "allergy", "peanuts"
    if "4pm" in t:
        return "STORE", "meeting_time", "4pm"
    if "3pm" in t:
        return "STORE", "meeting_time", "3pm"
    if "10am" in t:
        return "STORE", "meeting_time", "10am"
    if "window seat" in t or "by the window" in t or "near the window" in t:
        return "STORE", "seat_preference", "window"
    if "budget hotel" in t or "cheap hotel" in t or "affordable place to stay" in t:
        return "STORE", "hotel_type", "budget"
    if "italian" in t and ("food" in t or "cuisine" in t or "like" in t or "enjoy" in t):
        return "STORE", "favorite_cuisine", "italian"
    if "painting" in t or "doing art" in t:
        return "STORE", "hobby", "painting"
    if "python" in t and ("coding" in t or "programming" in t or "interview" in t or "practice" in t):
        return "STORE", "coding_language", "python"

    return "KEEP", None, None