"""
llm.py
Lightweight wrapper used by `main.py`.

Provides a generate_text(prompt, max_tokens) function. If
`llama-cpp-python` is installed and the environment variable
`LLAMA_MODEL_PATH` points to a model file, it will use that. Otherwise
it falls back to a safe mock response so the daemon can run for local
development and testing.
"""
from typing import Any
import os

_HAS_LLAMA = False
_LLAMA_ERR: Any = None

try:
    from llama_cpp import Llama  # type: ignore
    _HAS_LLAMA = True
except Exception as e:
    _HAS_LLAMA = False
    _LLAMA_ERR = e


def generate_text(
    prompt: str,
    max_tokens: int = 50,
    backend: str = "auto",
    force_mock: bool = False,
    hf_model: str | None = None,
    remote_url: str | None = None,
    timeout: int = 30,
) -> str:
    """Generate text for `prompt`.

    If `llama-cpp-python` is available and `LLAMA_MODEL_PATH` env var is
    set to a valid model file, this will call into that library. If not,
    returns a deterministic mock response suitable for development.

    Inputs:
      - prompt: text prompt
      - max_tokens: maximum tokens to generate (best-effort)

    Output: generated string
    """
    # Backwards compatibility: if force_mock is True, always use mock
    if force_mock or backend == "mock":
        head = prompt.strip().replace("\n", " ")[:200]
        return f"[mock-lm] Generated (max_tokens={max_tokens}): Hello! (echo) {head}"

    # Backend selection for 'auto' mode: prefer llama-cpp if available and path set
    chosen = backend
    if backend == "auto":
        if _HAS_LLAMA and os.getenv("LLAMA_MODEL_PATH"):
            chosen = "llama_cpp"
        else:
            chosen = "mock"

    if chosen == "llama_cpp":
        model_path = os.getenv("LLAMA_MODEL_PATH")
        if not model_path:
            return (
                "[llm] llama-cpp-python backend selected but LLAMA_MODEL_PATH is not set. "
                "Set the LLAMA_MODEL_PATH environment variable to a local .bin model file."
            )
        try:
            llm = Llama(model_path=model_path)
            result = llm(prompt=prompt, max_tokens=max_tokens)
            try:
                return result["choices"][0]["text"]
            except Exception:
                return str(result)
        except Exception as e:
            return f"[llm] error invoking llama-cpp-python: {e}"

    if chosen == "hf_api":
        # Use the Hugging Face Inference API via requests. Requires HF_TOKEN and optional HF_MODEL env var.
        try:
            import requests

            token = os.getenv("HF_TOKEN")
            model = hf_model or os.getenv("HF_MODEL")
            if not token:
                return "[llm] HF API backend selected but HF_TOKEN is not set in the environment."
            if not model:
                return "[llm] HF API backend selected but no model specified (pass hf_model or set HF_MODEL)."
            url = f"https://api-inference.huggingface.co/models/{model}"
            headers = {"Authorization": f"Bearer {token}"}
            payload = {"inputs": prompt, "parameters": {"max_new_tokens": max_tokens}}
            resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
            resp.raise_for_status()
            data = resp.json()
            # HF inference can return different shapes; try common ones
            if isinstance(data, dict) and "generated_text" in data:
                return data["generated_text"]
            if isinstance(data, list) and len(data) > 0:
                first = data[0]
                if isinstance(first, dict) and "generated_text" in first:
                    return first["generated_text"]
                if isinstance(first, dict) and "text" in first:
                    return first["text"]
            # Fallback to string
            return str(data)
        except Exception as e:
            return f"[llm] error calling HF Inference API: {e}"

    if chosen == "remote":
        try:
            import requests

            url = remote_url or os.getenv("REMOTE_API_URL")
            if not url:
                return "[llm] remote backend selected but REMOTE_API_URL not configured."
            payload = {"prompt": prompt, "max_tokens": max_tokens}
            resp = requests.post(url, json=payload, timeout=timeout)
            resp.raise_for_status()
            # Try to parse common response shapes
            try:
                data = resp.json()
                if isinstance(data, dict) and "text" in data:
                    return data["text"]
                if isinstance(data, dict) and "result" in data:
                    return data["result"]
                return str(data)
            except Exception:
                return resp.text
        except Exception as e:
            return f"[llm] error calling remote inference endpoint: {e}"

    if chosen == "webui":
        # Adapter for local text-generation-webui / oobabooga-like APIs.
        try:
            import requests

            base = remote_url or os.getenv("WEBUI_URL") or "http://127.0.0.1:7860"
            # Try a list of common endpoints used by different web UI projects
            endpoints = [
                "/api/generate",
                "/api/v1/generate",
                "/generate",
                "/api/textgen",
                "/api/v1/textgen",
            ]
            last_exc = None
            for ep in endpoints:
                url = base.rstrip("/") + ep
                try:
                    payload = {"prompt": prompt, "max_new_tokens": max_tokens}
                    resp = requests.post(url, json=payload, timeout=timeout)
                    resp.raise_for_status()
                    # Try to parse common JSON shapes
                    try:
                        data = resp.json()
                        # common shapes: {"results":[{"text":...}]}, [{"generated_text":...}]
                        if isinstance(data, dict):
                            if "results" in data and isinstance(data["results"], list) and len(data["results"])>0:
                                r0 = data["results"][0]
                                if isinstance(r0, dict) and "text" in r0:
                                    return r0["text"]
                                if isinstance(r0, dict) and "generated_text" in r0:
                                    return r0["generated_text"]
                            if "generated_text" in data:
                                return data["generated_text"]
                            if "text" in data:
                                return data["text"]
                        if isinstance(data, list) and len(data) > 0:
                            first = data[0]
                            if isinstance(first, dict) and "generated_text" in first:
                                return first["generated_text"]
                            if isinstance(first, dict) and "text" in first:
                                return first["text"]
                        # Fallback to whole JSON
                        return str(data)
                    except ValueError:
                        # Not JSON — return raw text
                        return resp.text
                except Exception as e:
                    last_exc = e
                    continue
            return f"[llm] webui adapter failed to contact endpoints. Last error: {last_exc}"
        except Exception as e:
            return f"[llm] error using webui adapter: {e}"

    # Fallback mock responder for any other case
    head = prompt.strip().replace("\n", " ")[:200]
    return f"[mock-lm] Generated (max_tokens={max_tokens}): Hello! (echo) {head}"
