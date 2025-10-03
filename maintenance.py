"""
maintenance.py
Predictive maintenance and health checks (stub, log-only).
"""
from __future__ import annotations

from typing import Dict, Any, List


def health_summary(snapshot: Dict[str, Any]) -> List[str]:
    tips: List[str] = []
    cpu = float(snapshot.get("cpu_percent", 0))
    mem = float(snapshot.get("mem_percent", 0))
    disk = float(snapshot.get("disk_percent", 0))
    if disk > 90:
        tips.append("Disk failure risk increases when near full; consider cleanup or expansion.")
    if mem > 90:
        tips.append("System may become unstable under memory pressure; close apps or add RAM/swap.")
    if cpu > 95:
        tips.append("Sustained CPU saturation can cause throttling; improve cooling or limit workloads.")
    if not tips:
        tips.append("No maintenance concerns detected.")
    return tips


