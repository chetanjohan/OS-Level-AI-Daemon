# OS-Level AI Daemon

Local-first AI daemon with system monitoring, lightweight heuristics, and a simple web UI.

## Quickstart

```bash
python -m venv .venv
# PowerShell
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Run the daemon (mock LLM by default)
```bash
python main.py --once              # single cycle
python main.py --monitor           # continuous with system monitor logs
```

### Run the web UI
```bash
python api.py
# Open http://127.0.0.1:8000
```

## Web UI
- Prompt text generation with selectable backend: `auto | mock | llama_cpp | hf_api | webui | remote`
- Suggestions panel with privacy levels: `strict | balanced | open`

Endpoints served by the UI server:
- POST `/api/generate` → `{ text }`
- GET  `/api/suggest?privacy=<level>` → `{ suggestions: string[] }`
- GET  `/api/optimize` → `{ optimizations: string[] }`
- GET  `/api/scan` → `{ anomaly_score: number, findings: string[] }`
- GET  `/api/maintain` → `{ maintenance: string[] }`

## CLI options
`main.py`:
- `--interval <seconds>` polling interval (default 5)
- `--max-tokens <n>` generation limit (default 50)
- `--backend <name>` LLM backend selection
- `--no-mock` use real backends when configured
- `--monitor` start lightweight system monitoring (logs to `monitor.log`)

## Modules
- `llm.py` — backend routing to mock/llama.cpp/HF/webui/remote
- `monitor.py` — CPU/MEM/DISK/NET snapshots, privacy-aware logs, basic heuristics, automation (temp cleanup, backup stub)
- `assistant.py` — builds user suggestions (context + snapshot)
- `context.py` — simple context inference (`idle|work|gaming` heuristics)
- `privacy.py` — privacy levels and redaction
- `optimizer.py` — resource optimization recommendations (log-only)
- `security.py` — anomaly scoring + malware scan stub
- `maintenance.py` — predictive maintenance tips (stub)
- `learning.py` — tiny on-disk store for preferences/patterns
- `api.py` — Flask server and static UI

## LLM backends
- `mock` (default unless `--no-mock`): deterministic echo for development
- `llama_cpp`: set `LLAMA_MODEL_PATH` to a local GGUF model
- `hf_api`: set `HF_TOKEN` and `HF_MODEL`
- `webui`: set `WEBUI_URL` if not default `http://127.0.0.1:7860`
- `remote`: set `REMOTE_API_URL`

## Development
```bash
pytest -q
```

## License
MIT
