# OS-Level AI Daemon (OSAD)
OS-Level AI Daemon (OSAD)A local-first system intelligence daemon that runs in the background of your OS. It observes system state, applies lightweight heuristics, and exposes a private API for contextual suggestions and automation.No cloud dependency. No surveillance. Mocked LLMs by default.🧠 The PhilosophyMost "AI Assistants" are just fancy wrappers for a chat box. OSAD is different. It is designed to be a "background systems brain" that understands the difference between you compiling code, playing a game, or idling, providing optimizations without needing an internet connection.Privacy First: Aggressive redaction of sensitive data before it ever hits an LLM.Resource Aware: Runs with low priority to ensure it never steals cycles from your actual work.Pluggable: Swap between a zero-resource "Mock" mode, local GGUF models, or remote APIs.🏗️

## ArchitectureCode snippetgraph TD
    A[OS Metrics: CPU/RAM/Disk] --> B[monitor.py: Snapshots]
    B --> C[context.py: Inference]
    C --> D[assistant.py: Prompt Assembly]
    D --> E{llm.py: Router}
    E -->|Default| F[Mock / Deterministic]
    E -->|Local| G[llama.cpp / GGUF]
    E -->|Remote| H[HF / Custom API]
    F/G/H --> I[api.py: Web UI & JSON API]

## 🚀 Quickstart1. Environment SetupBash# Clone the repository
git clone https://github.com/yourutils/os-ai-daemon.git
cd os-ai-daemon

## Setup Virtual Environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

## Install Dependencies
pip install -r requirements.txt

### Running the Daemon
The daemon handles the system monitoring and background logic.Bash# Run a single check-in cycle
python main.py --once

python main.py --monitor

### Launching the Interface
In a separate terminal, start the local web server:Bashpython api.py
View the dashboard at: http://127.0.0.1:8000⚙️ 

## Configuration
OSAD uses environment variables for sensitive backend configurations.
Variable,Description,Default
LLM_BACKEND,"mock, llama_cpp, hf_api, remote",mock
LOG_LEVEL,"DEBUG, INFO, WARNING",INFO
LLAMA_MODEL_PATH,Path to your .gguf file,None
HF_TOKEN,Hugging Face API Token,None
DAEMON_INTERVAL,Seconds between system snapshots,5

## 🛠️ Features & ModulesCore
Intelligencecontext.py: Infers high-level states (idle, work, gaming, streaming).privacy.py: Filters process names and logs based on user-defined sensitivity levels.learning.py: A local-only SQLite/JSON store that remembers your preferences over time.Monitoring & Securitymonitor.py: Real-time snapshots of CPU, Memory, Disk, and Network IO.security.py: Heuristic-based anomaly detection (e.g., "Why is a calculator using 40% CPU?").maintenance.py: Stubs for predictive disk failure and cache cleanup alerts.

## 📡 API Endpoints (Local Only)
MethodEndpointDescriptionGET/api/suggestReturns AI suggestions based on current system context.GET/api/metricsReturns the latest raw system snapshots.POST/api/generateDirect interaction with the configured LLM backend.GET/api/scanRuns a quick heuristic security/anomaly scan.

## 🤝 Contributing
Fork the ProjectCreate your Feature Branch (git checkout -b feature/AmazingFeature)Commit your Changes (git commit -m 'Add some AmazingFeature')Push to the Branch (git push origin feature/AmazingFeature)Open a Pull Request

## 📄 License
Distributed under the MIT License. See LICENSE for more information.
