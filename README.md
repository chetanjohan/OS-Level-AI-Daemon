# OS-Level-AI-Daemon

[![Initial checks](https://github.com/chetanjohan/OS-Level-AI-Daemon/actions/workflows/initial.yml/badge.svg)](https://github.com/chetanjohan/OS-Level-AI-Daemon/actions/workflows/initial.yml)

## Overview
OS-Level-AI-Daemon is an experimental project that explores how lightweight AI models and automation scripts can run directly at the operating system level. The goal is to create a background service (daemon) capable of handling tasks like monitoring, automating workflows, and interacting with local applications.

## Features (Planned)
- Runs as a background daemon process  
- Integrates with local system commands  
- Uses AI models for intelligent task handling  
- Modular design for adding custom task handlers  
- Cross-platform support (Linux/Windows)  

## Getting Started
1. Clone the repository:  
   ```bash
   git clone https://github.com/chetanjohan/OS-Level-AI-Daemon.git
   cd OS-Level-AI-Daemon
## How to use

This project provides a small daemon and a testable `Daemon` class. The CLI supports multiple backends and a one-shot mode for development.

Quick CLI examples (PowerShell):

- Run a single mock invocation (fast, no model required):
```powershell
python .\main.py --once
```

- Run continuously (mock):
```powershell
python .\main.py
```

- Use a local llama-cpp model (requires `llama-cpp-python` and a converted ggml `.bin` model):
```powershell
$env:LLAMA_MODEL_PATH = 'C:\models\ggml-model.bin'

# OS-Level-AI-Daemon

[![Initial checks](https://github.com/chetanjohan/OS-Level-AI-Daemon/actions/workflows/initial.yml/badge.svg)](https://github.com/chetanjohan/OS-Level-AI-Daemon/actions/workflows/initial.yml)

## Overview

OS-Level-AI-Daemon is an experimental project that explores how lightweight AI models and automation scripts can run directly at the operating system level. The goal is to create a background service (daemon) capable of handling tasks like monitoring, automating workflows, and interacting with local applications.

## Features (Planned)

- Runs as a background daemon process
- Integrates with local system commands
- Uses AI models for intelligent task handling
- Modular design for adding custom task handlers
- Cross-platform support (Linux/Windows)

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/chetanjohan/OS-Level-AI-Daemon.git
cd OS-Level-AI-Daemon
```

2. Install dependencies (recommended inside a virtualenv):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## How to use

This project provides a small daemon and a testable `Daemon` class. The CLI supports multiple backends and a one-shot mode for development.

Quick CLI examples (PowerShell):

- Run a single mock invocation (fast, no model required):

```powershell
python .\main.py --once
```

- Run continuously (mock):

```powershell
python .\main.py
```

- Use a local llama-cpp model (requires `llama-cpp-python` and a converted ggml `.bin` model):

```powershell
$env:LLAMA_MODEL_PATH = 'C:\models\ggml-model.bin'
python .\main.py --backend llama_cpp --no-mock --once
```

- Use Hugging Face Inference API (requires HF token and HF model id):

```powershell
$env:HF_TOKEN = 'hf_xxx'
$env:HF_MODEL = 'meta-llama/Llama-2-7b-chat-hf'
python .\main.py --backend hf_api --once
```

- Use a local web UI (text-generation-webui / similar):

```powershell
$env:WEBUI_URL = 'http://127.0.0.1:7860'
python .\main.py --backend webui --once
```

- Use a remote inference server (simple POST JSON API):

```powershell
$env:REMOTE_API_URL = 'https://my-inference-host/api/generate'
python .\main.py --backend remote --once
```

### Environment variables used by the project

- `LLAMA_MODEL_PATH` — path to a local ggml/gguf `.bin` model for `llama_cpp` backend.
- `HF_TOKEN` — Hugging Face API token for `hf_api` backend.
- `HF_MODEL` — model id on Hugging Face (e.g. `meta-llama/Llama-2-7b-chat-hf`) used by `hf_api`.
- `WEBUI_URL` — base URL for a local web UI (defaults to `http://127.0.0.1:7860`).
- `REMOTE_API_URL` — URL for a remote inference endpoint used by the `remote` backend.

## Hugging Face Inference API

If you prefer to use a hosted model without downloading weights, the Hugging Face Inference API is a convenient option. Important points:

- You must accept the model license on Hugging Face for gated models (for example Llama/Llama-2) before you can call the Inference API for that model.
- Generate an access token on Hugging Face and set it as `HF_TOKEN` in your environment.
- Set `HF_MODEL` to the model id you want to use (for example `meta-llama/Llama-2-7b-chat-hf`).

Example (PowerShell):

```powershell
pip install -r requirements.txt
$env:HF_TOKEN = 'hf_xxx'
$env:HF_MODEL = 'meta-llama/Llama-2-7b-chat-hf'
python .\main.py --backend hf_api --once
```

Notes:

- The `hf_api` backend uses the Hugging Face Inference endpoint and will incur usage costs and rate limits according to your HF account and plan.
- Responses returned by the API can vary in shape; the adapter in `llm.py` tries common response formats.

## Downloading and converting LLaMA weights

If you want to run models locally with `llama_cpp`, you'll typically need to:

1. Obtain the PyTorch weights from Hugging Face (accept license, authenticate with `huggingface-cli login` or set `HF_TOKEN`).
2. Convert the PyTorch weights to a ggml/gguf `.bin` file using the `llama.cpp` conversion tools or community converters.

This repository includes a small helper to download model files from Hugging Face to `models/`:

```powershell
python .\scripts\download_model.py --repo-id meta-llama/Llama-2-7b-chat-hf --filenames pytorch_model.bin
```

Conversion to a `ggml`/`gguf` file is outside the scope of this script; follow the instructions in the `llama.cpp` project to convert PyTorch weights.

After conversion, set `LLAMA_MODEL_PATH` to the converted `.bin` file and run with `--backend llama_cpp`.

## Tests

Run unit tests with:

```powershell
pytest -q
```
