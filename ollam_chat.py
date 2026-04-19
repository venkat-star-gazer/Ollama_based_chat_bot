"""Web-based local Ollama chat bot using Gradio."""

import argparse
import os
import sys
from typing import List, Optional

# Suppress Gradio telemetry and warnings
os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"
os.environ["GRADIO_SERVER_PORT"] = "7860"

import gradio as gr
import ollama

DEFAULT_MODEL = "qwen2.5-coder:1.5b"
DEFAULT_SYSTEM = "You are a helpful assistant."
DEFAULT_PORT = 7860


def list_installed_models() -> List[str]:
    try:
        response = ollama.list()
    except Exception as exc:
        print("Could not list available Ollama models:", exc, file=sys.stderr)
        return []

    models = []
    for model in getattr(response, "models", []):
        model_name = getattr(model, "model", None)
        if model_name:
            models.append(model_name)
    return models


def format_chat_response(response) -> str:
    message = getattr(response, "message", None)
    if message is None:
        return ""
    return getattr(message, "content", "") or ""


def ollama_chat(
    user_input: str,
    chatbot: List[dict],
    messages: List[dict],
    model_name: str,
    system_prompt: str,
) -> tuple[List[dict], List[dict], str]:
    """Generate a chat response using Ollama."""
    # Initialize messages if empty
    if not messages:
        messages = [{"role": "system", "content": system_prompt}]
    # Initialize chatbot display if empty
    if chatbot is None:
        chatbot = []

    user_input = user_input.strip()
    if not user_input:
        return chatbot, messages, ""

    # Add user message to both the display and the message history
    user_message = {"role": "user", "content": user_input}
    chatbot.append(user_message)
    messages.append(user_message)

    try:
        response = ollama.chat(model=model_name, messages=messages)
        assistant_text = format_chat_response(response)
    except Exception as exc:
        assistant_text = f"Error: {exc}"

    assistant_message = {"role": "assistant", "content": assistant_text}
    chatbot.append(assistant_message)
    messages.append(assistant_message)

    return chatbot, messages, ""


def reset_chat(system_prompt: str) -> tuple[List[List[str]], List[dict]]:
    return [], [{"role": "system", "content": system_prompt}]


def create_ui(default_model: str, default_system: str) -> gr.Blocks:
    available_models = list_installed_models() or [default_model]
    if default_model not in available_models:
        available_models.insert(0, default_model)

    with gr.Blocks(title="Local Ollama Chat Bot") as demo:
        gr.Markdown(
            "## Local Ollama Chat Bot\nInteract with a local Ollama model through a web interface."
        )

        with gr.Row():
            model_input = gr.Dropdown(
                choices=available_models,
                value=default_model,
                label="Model",
            )
            system_input = gr.Textbox(
                value=default_system,
                label="System Prompt",
                lines=2,
            )

        chatbot = gr.Chatbot(label="Conversation")
        user_input = gr.Textbox(
            placeholder="Type your message here...",
            label="Your Message",
            lines=2,
        )
        submit_button = gr.Button("Send")
        reset_button = gr.Button("Reset Conversation")

        # Store messages in internal state (Ollama format: role/content dicts)
        messages_state = gr.State(value=[{"role": "system", "content": default_system}])

        try:
            submit_button.click(
                ollama_chat,
                inputs=[user_input, chatbot, messages_state, model_input, system_input],
                outputs=[chatbot, messages_state, user_input]
            )
        except Exception as exc:
            print("Error setting up submit button:", exc, file=sys.stderr)

        reset_button.click(
            reset_chat,
            inputs=[system_input],
            outputs=[chatbot, messages_state]
        )

    return demo


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Web-based local Ollama chatbot")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Default local Ollama model to use")
    parser.add_argument("--system", default=DEFAULT_SYSTEM, help="Default system prompt")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port for Gradio web UI")
    parser.add_argument("--list-models", action="store_true", help="Show installed local Ollama models and exit")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.list_models:
        models = list_installed_models()
        if models:
            print("\n".join(models))
        else:
            print("No local Ollama models found.")
        return

    demo = create_ui(args.model, args.system)
    demo.launch(
        server_name="127.0.0.1",
        server_port=args.port,
        show_error=True,
        quiet=True,
    )


if __name__ == "__main__":
    main()
