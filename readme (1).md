# Adaptive Long-Term Memory for LLM-Based Dialogue Agents

**Uttapreksha Patel & Mirudula Shri Muthukumaran — Northeastern University**

---

## Overview

Large Language Model (LLM) dialogue agents struggle to maintain consistency in long conversations. Because LLMs operate within a limited context window, important information from earlier turns can be lost as the conversation grows.

This project investigates whether **adaptive long-term memory** mechanisms can improve dialogue coherence by selectively storing important user information while discarding irrelevant context. The adaptive approach is evaluated against two simpler baselines — sliding window context and summary-based memory — on a synthetic long-dialogue dataset.

---

## The Problem

In long conversations, LLMs often forget earlier facts that remain relevant later. Consider the following example:

```
User: I recently became vegetarian.
... many turns later ...
User: Actually I'm vegan now.
... many turns later ...
User: What should I eat tonight?
```

| Approach | Behavior |
|---|---|
| **Window baseline** | May forget both facts entirely |
| **Summary baseline** | May retain the outdated fact |
| **Adaptive memory** | Stores and updates to the latest constraint |

---

## System Pipeline

```
Synthetic Dialogue Generator
        ↓
Long Dialogue Dataset
        ↓
Adaptive Selector
 (detect important facts)
        ↓
Structured Memory Slots
 (store + update facts)
        ↓
Query Answering
        ↓
Evaluation (memory accuracy + query accuracy)
        ↓
Baseline Comparison
```

---

## Project Structure

```
project/
│
├── data/
│   └── dialogues_long.json
│
├── results/
│   ├── results.csv
│   ├── memory_accuracy.png
│   └── query_accuracy.png
│
├── selector.py
├── memory_slots.py
├── baseline_window.py
├── baseline_summary.py
├── evaluator.py
├── prompt_builder.py
│
├── run_experiments.py
└── README.md
```

---

## Dataset

The dataset consists of **synthetic long dialogues** designed to test long-horizon memory. Each dialogue contains:

- One or more important user facts
- Multiple distractor turns
- Optional updates to earlier facts
- A final query requiring memory recall

**Example dialogue structure:**

```
User: I recently became vegetarian.
Assistant: That's great!

... many unrelated turns ...

User: Actually I'm vegan now.

... more turns ...

User: What should I eat tonight?
```

The correct response should reflect the **latest** user preference.

---

## Adaptive Memory Mechanism

The adaptive memory system extracts and stores important facts from dialogue turns into **structured key-value memory slots**. Tracked information includes user preferences, commitments, constraints, and personal attributes.

**Example memory slots:**

```
diet           = vegan
meeting_time   = 4pm
allergy        = peanuts
seat_preference = window
```

### Conflict Resolution

When a user updates a previously stated fact, the system **overwrites** the stored value with the most recent information.

```
diet = vegetarian  →  diet = vegan
```

---

## Baselines

### Sliding Window
Retains only the last *k* dialogue turns. Earlier information is lost if it falls outside the window.

### Summary
Compresses dialogue history into a summary representation. This can silently discard small but important facts or fail to apply updates correctly.

---

## Evaluation Metrics

### Memory Accuracy
Measures whether the correct fact is stored in memory.

```
correct stored facts / total expected facts
```

### Query Accuracy
Measures whether the system answers the final query correctly.

```
Query:    What should I eat tonight?
Expected: A vegan meal
```

---

## Results

| Method | Memory Accuracy | Query Accuracy |
|---|---|---|
| **Adaptive Memory** | **1.00** | **1.00** |
| Summary Baseline | 0.91 | 0.91 |
| Window Baseline | 0.00 | 0.00 |

Initial experiments show that adaptive memory significantly improves long-horizon recall, correctly preserving user constraints and handling updates that summary and window approaches miss.

---

## Getting Started

### 1. Install Requirements

```bash
pip install matplotlib pandas
```

### 2. Run the Experiment Pipeline

```bash
python run_experiments.py
```

This script loads the dialogue dataset, runs the adaptive memory system and both baselines, evaluates memory and query accuracy, and saves all results.

---

## Output

**Console output** — per-dialogue breakdown, for example:

```
============================================================
Dialogue: diet_update_1

Adaptive memory: {'diet': 'vegan'}
Adaptive evaluation: {'correct': 1, 'total': 1, 'accuracy': 1.0}

Window memory: {}
Window evaluation: {'correct': 0, 'total': 1, 'accuracy': 0.0}
```

**CSV results** — saved to `results/results.csv`. Each row contains the dialogue ID, domain, expected value, memory accuracy, query accuracy, and model responses.

**Plots** — `memory_accuracy.png` and `query_accuracy.png` visualize performance differences across all three methods.

---

## Limitations

- The selector is rule-based rather than LLM-based
- The dataset is synthetic rather than drawn from real conversations
- The number of dialogue scenarios is currently limited

---

## Future Work

- **LLM-based selector** — replace rule-based detection with model-based classification
- **Larger datasets** — more domains and more complex update scenarios
- **Additional baselines** — retrieval-based memory, hierarchical memory systems
- **Deeper analysis** — failure case studies and memory capacity experiments

---

## Reproducibility

All experiments are fully reproducible. Running the following command regenerates all reported results and plots:

```bash
python run_experiments.py
```
