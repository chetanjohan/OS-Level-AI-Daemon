"""
optimizer.py
Heuristics for resource optimization (log-only recommendations).
"""
from __future__ import annotations

from typing import Dict, Any, List


def recommend_optimizations(snapshot: Dict[str, Any]) -> List[str]:
    tips: List[str] = []
    cpu = float(snapshot.get("cpu_percent", 0))
    mem = float(snapshot.get("mem_percent", 0))
    disk = float(snapshot.get("disk_percent", 0))

    if cpu > 80:
        tips.append("Lower priority of background processes and pause heavy indexing.")
    if mem > 85:
        tips.append("Free caches, close unused tabs, or expand swap.")
    if disk > 85:
        tips.append("Limit background writes and offload logs to slower intervals.")
    if not tips:
        tips.append("No optimization needed right now.")
    return tips


