
"""
OS-Level-AI-Daemon
Simple daemon to interact with your offline LLaMA model
"""

"""
main.py
Daemon entrypoint with a testable Daemon class and a small CLI.

Usage examples:
  python main.py                  # run with defaults (mock mode)
  python main.py --interval 10    # poll every 10s
  python main.py --no-mock        # try to use local LLM (requires LLAMA_MODEL_PATH)

For tests, the Daemon exposes `run_once()` which executes one task cycle.
"""

import time
import argparse
from typing import Optional

from llm import generate_text


def fetch_task() -> Optional[str]:
    """Simulate fetching a task. Replace with real integration later."""
    return "Hello, OS-Level-AI-Daemon! Generate a small greeting."


class Daemon:
    def __init__(self, interval: int = 5, max_tokens: int = 50, backend: str = "auto", force_mock: bool = True):
        self.interval = interval
        self.max_tokens = max_tokens
        self.backend = backend
        self.force_mock = force_mock

    def process_task(self, prompt: str) -> str:
        print("[Daemon] Processing task...")
        response = generate_text(
            prompt,
            max_tokens=self.max_tokens,
            backend=self.backend,
            force_mock=self.force_mock,
        )
        print(f"[Daemon] Response:\n{response}\n")
        return response

    def run_once(self) -> Optional[str]:
        """Run a single fetch/process cycle. Returns the response or None if no task."""
        task = fetch_task()
        if not task:
            print("[Daemon] No tasks found.")
            return None
        return self.process_task(task)

    def run_forever(self):
        print("[Daemon] OS-Level-AI-Daemon started. Press Ctrl+C to stop.")
        try:
            while True:
                self.run_once()
                time.sleep(self.interval)
        except KeyboardInterrupt:
            print("\n[Daemon] Shutting down...")


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="OS-Level-AI-Daemon")
    p.add_argument("--interval", type=int, default=5, help="Seconds between polls")
    p.add_argument("--max-tokens", type=int, default=50, help="Max tokens for generation")
    p.add_argument("--no-mock", dest="no_mock", action="store_true", help="Disable mock LLM (use local model) and require LLAMA_MODEL_PATH")
    p.add_argument(
        "--backend",
        choices=["auto", "mock", "llama_cpp", "hf_api", "webui", "remote"],
        default="auto",
        help="Which backend to use for generation (auto chooses llama_cpp when available)",
    )
    p.add_argument("--once", action="store_true", help="Run a single fetch/process cycle and exit")
    return p


def main():
    parser = build_arg_parser()
    args = parser.parse_args()
    daemon = Daemon(interval=args.interval, max_tokens=args.max_tokens, backend=args.backend, force_mock=not args.no_mock)
    if args.once:
        daemon.run_once()
    else:
        daemon.run_forever()


if __name__ == "__main__":
    main()
