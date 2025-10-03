"""
assistant.py
Generates user-facing suggestions based on system Snapshot and context.
"""
from __future__ import annotations

from typing import List, Dict, Any

from context import infer_context
from privacy import normalize_level, redact_payload


def build_suggestions(snapshot: Dict[str, Any], privacy_level: str | None = None) -> List[str]:
    level = normalize_level(privacy_level)
    context = infer_context()

    snap = dict(snapshot)
    snap["context"] = context
    snap = redact_payload(snap, level)

    tips: List[str] = []
    cpu = float(snapshot.get("cpu_percent", 0))
    mem = float(snapshot.get("mem_percent", 0))
    disk = float(snapshot.get("disk_percent", 0))

    if context == "gaming":
        tips.append("Gaming detected: enable high-performance mode and pause non-essential updates.")
    elif context == "work":
        tips.append("Work mode: prioritize editor/IDE and browser tabs; pause large background downloads.")
    elif context == "idle":
        tips.append("Idle detected: good time to run cleanup, backups, and updates.")

    if cpu > 85:
        tips.append("High CPU usage: consider closing heavy apps or lowering background task priority.")
    if mem > 90:
        tips.append("Memory pressure: close unused tabs/apps or add swap.")
    if disk > 90:
        tips.append("Disk near full: clean temporary files and large unused files.")

    if not tips:
        tips.append("System looks healthy. No action recommended right now.")
    return tips


