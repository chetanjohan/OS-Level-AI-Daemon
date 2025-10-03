"""
api.py
Simple Flask server exposing a text generation endpoint and serving a static UI.
"""
from __future__ import annotations

import os
from flask import Flask, request, jsonify, send_from_directory

from llm import generate_text
from assistant import build_suggestions
from monitor import SystemMonitor
from privacy import normalize_level


def create_app() -> Flask:
    app = Flask(__name__, static_folder="web", static_url_path="")

    @app.route("/")
    def index():
        return send_from_directory(app.static_folder, "index.html")

    @app.post("/api/generate")
    def api_generate():
        data = request.get_json(silent=True) or {}
        prompt = str(data.get("prompt", "")).strip()
        max_tokens = int(data.get("max_tokens", 50))
        backend = str(data.get("backend", os.getenv("WEB_BACKEND", "auto")))
        force_mock = bool(data.get("force_mock", False))

        if not prompt:
            return jsonify({"error": "prompt is required"}), 400

        text = generate_text(
            prompt,
            max_tokens=max_tokens,
            backend=backend,
            force_mock=force_mock,
        )
        return jsonify({"text": text})

    @app.get("/api/suggest")
    def api_suggest():
        # Build a small snapshot using psutil via a short-lived SystemMonitor tick
        try:
            import psutil

            cpu = psutil.cpu_percent(interval=0.0)
            vm = psutil.virtual_memory()
            du = psutil.disk_usage(os.getcwd())
            snapshot = {
                "cpu_percent": float(cpu),
                "mem_percent": float(vm.percent),
                "disk_percent": float(du.percent),
            }
        except Exception:
            snapshot = {"cpu_percent": 0.0, "mem_percent": 0.0, "disk_percent": 0.0}

        privacy = normalize_level(request.args.get("privacy"))
        tips = build_suggestions(snapshot, privacy)
        return jsonify({"suggestions": tips})

    return app


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "127.0.0.1")
    create_app().run(host=host, port=port, debug=True)


