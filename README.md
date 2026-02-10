# OS-Level AI Daemon

A **local-first AI daemon** that runs alongside your operating system, observes system state, applies lightweight heuristics, and exposes a simple web UI + API for suggestions, monitoring, and automation.

No cloud dependency by default. No surveillance cosplay. Mocked LLMs until you explicitly opt into real ones.

---

## What This Is

This project is an **OS-resident assistant service**, not a chatbot app.

It is designed to:

- Run continuously or on demand
- Observe **CPU, memory, disk, and network state**
- Infer **high-level context** like `idle`, `work`, or `gaming`
- Generate **suggestions and optimizations** based on that context
- Respect **privacy levels** and redact aggressively by default
- Expose everything through a **local web UI + JSON API**
- Support **multiple LLM backends**, including zero-LLM mock mode

Think “background systems brain,” not “AI friend.”

---

## What This Is Not

- Not a cloud service  
- Not a kernel module  
- Not spyware  
- Not a full automation engine (yet)  
- Not dependent on any single LLM vendor  

---

## Architecture Overview

┌─────────────┐
│ OS Metrics │ CPU / MEM / DISK / NET
└─────┬───────┘
↓
┌─────────────┐
│ monitor.py │ snapshots + heuristics
└─────┬───────┘
↓
┌─────────────┐
│ context.py │ idle | work | gaming
└─────┬───────┘
↓
┌─────────────┐
│ assistant │ suggestions + prompts
└─────┬───────┘
↓
┌─────────────┐
│ llm.py │ mock / local / remote
└─────┬───────┘
↓
┌─────────────┐
│ api.py │ Web UI + JSON API
└─────────────┘


---

## Features

### Core
- Local daemon loop with configurable interval
- Deterministic **mock LLM** for development
- Privacy-aware logging
- Context inference from system state
- On-disk lightweight learning store

### Monitoring
- CPU, memory, disk, network snapshots
- Anomaly scoring (stub, expandable)
- Monitor logs written to `monitor.log`

### Suggestions & Intelligence
- Contextual suggestions
- Resource optimization hints (log-only)
- Predictive maintenance stubs
- Malware / anomaly scan stub

### Interfaces
- CLI
- REST API
- Local web UI

---

## Quickstart

### Environment Setup

```bash
python -m venv .venv
# PowerShell
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

Run the Daemon

Mock LLM is enabled by default.

python main.py --once        # single execution cycle
python main.py --monitor     # continuous loop + system monitoring

Run the Web UI
python api.py


Open:

http://127.0.0.1:8000

CLI Options

main.py supports:

Option	Description
--interval <seconds>	Polling interval (default: 5)
--max-tokens <n>	LLM generation cap (default: 50)
--backend <name>	LLM backend selection
--no-mock	Disable mock and use real backends
--monitor	Enable continuous monitoring + logging
Web UI Capabilities

Prompt-based text generation

Backend switching:
auto | mock | llama_cpp | hf_api | webui | remote

Suggestions panel with privacy levels:
strict | balanced | open

API Endpoints

All endpoints are local-only by default.

Method	Endpoint	Description
POST	/api/generate	Generate text
GET	/api/suggest?privacy=<level>	Contextual suggestions
GET	/api/optimize	Optimization recommendations
GET	/api/scan	Anomaly scan
GET	/api/maintain	Maintenance suggestions
LLM Backends
mock (default)

Deterministic echo backend

Zero network calls

Ideal for development and testing

llama_cpp

Local GGUF model

Requires:

export LLAMA_MODEL_PATH=/path/to/model.gguf

hf_api

Hugging Face Inference API

Requires:

export HF_TOKEN=...
export HF_MODEL=...

webui

Stable Diffusion / text web UI compatible

Default:

http://127.0.0.1:7860

remote

Generic remote LLM endpoint

Requires:

export REMOTE_API_URL=...

Module Breakdown
File	Responsibility
llm.py	Backend routing and abstraction
monitor.py	System snapshots, heuristics, automation hooks
assistant.py	Suggestion and prompt assembly
context.py	Context inference logic
privacy.py	Privacy levels and redaction
optimizer.py	Resource optimization (log-only)
security.py	Anomaly scoring + malware stub
maintenance.py	Predictive maintenance stub
learning.py	On-disk preference store
api.py	Flask server + static UI
main.py	Daemon entry point
Testing
pytest -q

Design Principles

Local first

Privacy by default

Pluggable intelligence

Graceful stubs over fake promises

Everything inspectable

License

MIT
