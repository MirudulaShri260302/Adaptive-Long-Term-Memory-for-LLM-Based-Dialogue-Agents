"""
Interactive demo for Adaptive Long-Term Memory.

Run from project root:
    python3 src/demo.py

Then open http://localhost:7860 in your browser.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gradio as gr
from selector_llm import classify_turn_llm
from memory_slots import initialize_memory, update_memory
from prompt_builder import generate_memory_based_response

_memory = {}
_conversation = []   # list of strings for display


def reset():
    global _memory, _conversation
    _memory = initialize_memory()
    _conversation = []
    return format_conversation(), format_memory({}), ""


def format_memory(memory):
    if not memory:
        return "_(empty)_"
    lines = ["| Slot | Value |", "|------|-------|"]
    for k, v in memory.items():
        lines.append(f"| {k.replace('_',' ').title()} | **{v}** |")
    return "\n".join(lines)


def format_conversation():
    if not _conversation:
        return "_(no messages yet — type below and press Send)_"
    return "\n\n".join(_conversation)


def chat(user_message):
    global _memory, _conversation

    if not user_message.strip():
        return format_conversation(), format_memory(_memory), ""

    # Classify
    action, key, value = classify_turn_llm(user_message)

    # Update memory
    prev_value = _memory.get(key) if key else None
    if action == "STORE" and key:
        update_memory(_memory, key, value)
        if prev_value and prev_value != value:
            action_note = f"🟡 UPDATED `{key}`: {prev_value} → **{value}**"
        else:
            action_note = f"🟢 STORED `{key}` = **{value}**"
    elif action == "DROP":
        action_note = "🔴 DROPPED (irrelevant)"
    else:
        action_note = "🔵 KEPT in context"

    # Generate response
    response = generate_memory_based_response(_memory, user_message)
    if response == "I do not know.":
        response = "Got it, I'll remember that."

    # Append to conversation log
    _conversation.append(f"**You:** {user_message}  \n_{action_note}_")
    _conversation.append(f"**Agent:** {response}")

    return format_conversation(), format_memory(_memory), ""


with gr.Blocks(title="Adaptive Memory Demo") as demo:

    gr.Markdown("""
# 🧠 Adaptive Long-Term Memory — Live Demo
Type a message and press **Send**. The agent classifies each turn as **🟢 STORE**, **🔵 KEEP**, or **🔴 DROP**.

**Try this sequence:**
1. `I follow a vegan diet`
2. `I only drink decaf coffee`
3. `The weather is nice today` ← gets dropped
4. `What should I eat for dinner?`
5. `Actually I switched to vegetarian` ← diet slot updates 🟡
6. `What should I eat for dinner?` ← answer changes
""")

    with gr.Row():
        with gr.Column(scale=3):
            conversation_display = gr.Markdown(
                value="_(no messages yet — type below and press Send)_",
                label="Conversation"
            )
            gr.Markdown("---")
            with gr.Row():
                msg_input = gr.Textbox(
                    placeholder="Type a message...",
                    label="Your message",
                    scale=5,
                )
                send_btn = gr.Button("Send ▶", variant="primary", scale=1)
            reset_btn = gr.Button("🔄 Reset", variant="secondary")

        with gr.Column(scale=2):
            gr.Markdown("### 📦 Memory Slots (live)")
            memory_display = gr.Markdown(value="_(empty)_")

    send_btn.click(
        chat,
        inputs=[msg_input],
        outputs=[conversation_display, memory_display, msg_input],
    )

    msg_input.submit(
        chat,
        inputs=[msg_input],
        outputs=[conversation_display, memory_display, msg_input],
    )

    reset_btn.click(
        reset,
        outputs=[conversation_display, memory_display, msg_input],
    )


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)