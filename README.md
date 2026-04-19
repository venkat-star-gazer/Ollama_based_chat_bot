# Local Ollama Chatbot with Gradio

This project provides a simple web-based chat interface for a locally installed Ollama model using `gradio`.

## Features

- Web UI chat interface powered by Gradio
- Uses local Ollama models via the `ollama` Python package
- Supports model selection and custom system prompts
- Includes a simple browser-based chat experience

## Requirements

- Python 3.13+
- Local Ollama installation with at least one model pulled
- `ollama` Python package
- `gradio` Python package

## Setup

1. Install the required dependencies:

```bash
python -m pip install ollama gradio
```

2. Verify Ollama is working locally and that models are available:

```bash
python ollam_chat.py --list-models
```

## Usage

Run the app with:

```bash
python ollam_chat.py
```

Then open the Gradio web UI in your browser. The default address is `http://127.0.0.1:7860`.

### Optional arguments

- `--model MODEL` - default Ollama model to use
- `--system SYSTEM` - default system prompt
- `--port PORT` - port for the Gradio UI
- `--list-models` - show installed Ollama models and exit

Example:

```bash
python ollam_chat.py --model qwen2.5-coder:1.5b --system "You are a helpful AI assistant." --port 7860
```

## Notes

- The script uses Ollama's `chat` API to send conversational messages to the selected local model.
- The app stores chat state in memory and does not persist conversations across restarts.
- If you encounter HTTP or Gradio warnings, ensure the local Ollama daemon and model are available.

## File

- `ollam_chat.py` - main Gradio chatbot application
