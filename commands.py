"""
commands.py
Very small natural-language command parser and executors.
"""
from __future__ import annotations

import time
from typing import Any, Dict

from security import anomaly_score, malware_scan_stub


def _check_cpu_stability(samples: int = 5, interval_sec: float = 0.3) -> Dict[str, Any]:
    try:
        import psutil

        readings = []
        for _ in range(max(1, samples)):
            readings.append(float(psutil.cpu_percent(interval=interval_sec)))
        avg = sum(readings) / len(readings)
        variance = sum((x - avg) ** 2 for x in readings) / len(readings)
        return {
            "samples": readings,
            "average_percent": round(avg, 2),
            "variance": round(variance, 2),
            "stable": variance < 100.0,  # loose heuristic
        }
    except Exception as e:
        return {"error": f"cpu check failed: {e}"}


def execute_command(text: str) -> Dict[str, Any]:
    q = (text or "").strip().lower()
    if not q:
        return {"error": "empty command"}

    # intents
    if "cpu" in q and ("stability" in q or "stable" in q or "check" in q):
        cpu = _check_cpu_stability()
        return {"intent": "cpu_stability", "result": cpu}

    if ("virus" in q) or ("malware" in q) or ("scan" in q):
        score = anomaly_score()
        findings = malware_scan_stub()
        return {"intent": "virus_scan", "result": {"anomaly_score": score, "findings": findings}}

    return {"intent": "unknown", "message": "No matching action. Try: 'check cpu stability' or 'do a virus scan'."}


