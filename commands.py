"""
commands.py
Very small natural-language command parser and executors.
"""
from __future__ import annotations

import time
from typing import Any, Dict

from security import anomaly_score
from malware_scanner import virus_scan


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
        # Try to find a target directory in the command text (very simple heuristics)
        target = "."
        for token in q.split():
            if token.startswith("c:/") or token.startswith("d:/") or token.startswith("e:/"):
                target = token
                break
        res = virus_scan(target)
        # also compute anomaly score for network/process-level anomalies
        res_result = res.get("result", {})
        res_result["anomaly_score"] = max(float(res_result.get("anomaly_score", 0) or 0), float(anomaly_score()))
        res["result"] = res_result
        return res

    return {"intent": "unknown", "message": "No matching action. Try: 'check cpu stability' or 'do a virus scan'."}


