# Adaptive Long-Term Memory for LLM-Based Dialogue Agents

> NeurIPS 2024 Format: Northeastern University

## Overview

LLM dialogue agents fail in long conversations because important user preferences and commitments fall outside the active context window. This project studies an **adaptive long-term memory mechanism** that selectively stores salient information in structured key-value memory slots while discarding low-utility dialogue.

Instead of treating all history equally, the system decides per turn whether to **STORE**, **KEEP**, or **DROP** each user statement — and when a user updates a preference, the memory slot is overwritten with the latest value.

---

## Key Results

| Method | Memory Accuracy | Query Accuracy | Avg Prompt Tokens |
|---|---|---|---|
| **LLM Selector (ours)** | **0.760** | **0.760** | 27.5 |
| Retrieval (RAG) | 0.613 | 0.613 | 18.3 |
| Summary Baseline | 0.493 | 0.493 | 21.5 |
| Rule-based Selector | 0.453 | 0.453 | 21.9 |
| Window Baseline | 0.000 | 0.000 | 10.7 |

The LLM-based selector reduces slot extraction failures by **64%** relative to the rule-based selector by understanding paraphrases that keyword rules miss.

---

## Project Structure

```
├── data/
│   ├── dialogues_harder.json            # Generated dialogues (pre-augmentation)
│   └── dialogues_harder_augmented.json  # Paraphrase-augmented dialogues (used in experiments)
├── results/
│   ├── results.csv                      # Per-dialogue experiment results
│   ├── accuracy_comparison.png          # Memory & query accuracy bar chart
│   ├── error_type_breakdown.png         # Slot extraction vs update failure breakdown
│   ├── error_by_key_llm_vs_rule.png     # Per-slot errors: LLM vs rule-based
│   ├── accuracy_by_domain.png           # Per-domain accuracy heatmap
│   ├── token_efficiency.png             # Accuracy vs prompt token usage scatter
│   └── forgetting_curve.png             # Accuracy vs fact-to-query distance
├── src/
│   ├── selector.py                      # Rule-based KEEP/STORE/DROP selector
│   ├── selector_llm.py                  # LLM-based selector (Claude API)
│   ├── memory_slots.py                  # Memory slot initialization and updates
│   ├── dialogue_generator.py            # Synthetic long-horizon dialogue generator
│   ├── augment_dialogues.py             # Paraphrase augmentation pipeline
│   ├── baseline_window.py               # Sliding-window baseline
│   ├── baseline_summary.py              # Lossy summary baseline (3-slot cap)
│   ├── baseline_retrieval.py            # Embedding-based RAG baseline
│   ├── prompt_builder.py                # Query response generation from memory
│   ├── evaluator.py                     # Memory + query accuracy + error analysis
│   ├── experiment_runner.py             # Main experiment: all 5 methods compared
│   ├── plot_results.py                  # Generate all result figures
│   └── forgetting_curve.py              # Forgetting curve analysis
└── README.md
```

---

## Methods

### Adaptive Memory Pipeline
At each user turn, a selector classifies the turn into one of three actions:
- **STORE** — extract a structured key-value memory slot (e.g., `diet=vegan`)
- **KEEP** — retain in the recent dialogue buffer
- **DROP** — discard as irrelevant

When a later turn conflicts with an existing slot, the newer value **overwrites** the older one (recency-based conflict resolution).

### Two Selector Variants
**Rule-based selector** — hand-written keyword patterns. Fast but brittle under paraphrase variation.

**LLM-based selector** — prompts Claude to classify each user turn as STORE/KEEP/DROP and extract the key-value pair. Generalizes to paraphrases the rules miss (e.g., "I only drink caffeine-free beverages" → `drink_preference=decaf`).

### Three Baselines
- **Window** — retains only the last k=2 turns
- **Summary** — same LLM selector but caps memory at 3 slots with oldest-first eviction
- **Retrieval (RAG)** — encodes all user turns with `all-MiniLM-L6-v2`, retrieves top-3 most similar turns per query via cosine similarity

---

## Dataset

75 synthetic long-horizon dialogues across 15 domain templates:
- **Domains:** food preferences, scheduling, travel, health constraints, hobbies, work
- **Length:** 60–100 turns per dialogue
- **Features:** multi-step preference updates, paraphrase augmentation (70% probability), tricky third-party distractors (e.g., "My friend is vegetarian")
- **Evaluation:** deterministic ground-truth memory facts + test queries per dialogue

---

## Error Analysis

Two failure modes are identified and tracked:

| Error Type | Description |
|---|---|
| **Slot extraction failure** | A key was never stored (fact missed entirely) |
| **Update failure** | Key stored but holds a stale value from an earlier turn |

The LLM selector has 24 extraction failures vs 67 for the rule-based selector — a **64% reduction**. Update failures (12 vs 15) remain a challenge across all methods, concentrated on multi-hop update chains for `diet` and `meeting_time`.

---

## Forgetting Curve

Memory accuracy measured as a function of how far back (in turns) a fact was stated:

| Method | 0–20 turns | 21–40 turns | 41–60 turns | 61+ turns |
|---|---|---|---|---|
| LLM Selector | 1.000 | 0.929 | 0.905 | 0.860 |
| Rule-based | 0.778 | 0.429 | 0.476 | 0.721 |
| Summary | 1.000 | 0.857 | 0.381 | 0.349 |
| Retrieval | 0.500 | 0.571 | 0.905 | 0.674 |
| Window | 0.000 | 0.000 | 0.000 | 0.000 |

The LLM selector is the only method that stays above 0.85 at all distances — demonstrating that structured memory with semantic classification is **distance-invariant**.

---
## Interactive Demo

Run the live memory demo in your browser:
```bash
pip3 install gradio
export ANTHROPIC_API_KEY=sk-ant-...
python3 src/demo.py
```

Then open http://localhost:7860

## Setup

### Requirements
```bash
pip3 install anthropic sentence-transformers matplotlib numpy
```

### Environment
```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

### Reproduce experiments

```bash
# 1. Generate dataset
python3 src/dialogue_generator.py

# 2. Augment with paraphrases
python3 src/augment_dialogues.py

# 3. Run all experiments (takes ~5 min due to LLM API calls)
cd src
python3 experiment_runner.py

# 4. Generate plots
cd ..
python3 src/plot_results.py

# 5. Generate forgetting curve
python3 src/forgetting_curve.py
```

---

