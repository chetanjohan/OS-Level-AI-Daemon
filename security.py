"""
security.py
Security anomaly scoring and malware scan stubs (log-only).
"""
from __future__ import annotations

from typing import Dict, Any, List
import psutil
from malware_scanner import virus_scan as run_virus_scan


def anomaly_score() -> float:
    try:
        conns = psutil.net_connections(kind="inet")
        listening = len([c for c in conns if c.status == psutil.CONN_LISTEN])
        proc = len(psutil.pids())
        score = 0.0
        if listening > 50:
            score += 0.5
        if proc > 500:
            score += 0.5
        return min(1.0, score)
    except Exception:
        return 0.0


def malware_scan_stub() -> List[str]:
    # Backwards compatible stub: run the new scanner in current dir
    result = run_virus_scan(".")
    r = result.get("result", {})
    return list(r.get("findings", []))


