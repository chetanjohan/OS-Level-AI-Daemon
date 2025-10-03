"""
context.py
Heuristic context inference (idle/work/gaming) using available signals.
"""
from __future__ import annotations

from typing import Literal
import psutil

Context = Literal["idle", "work", "gaming", "unknown"]


def infer_context() -> Context:
    try:
        proc_names = set()
        for pid in psutil.pids()[:500]:
            try:
                p = psutil.Process(pid)
                proc_names.add(p.name().lower())
            except Exception:
                continue
        # simple heuristics
        if not proc_names:
            return "unknown"
        game_markers = {"steam.exe", "epicgameslauncher.exe", "battle.net.exe", "fortnite.exe", "valorant.exe"}
        work_markers = {"code.exe", "pycharm64.exe", "idea64.exe", "chrome.exe", "firefox.exe", "word.exe", "excel.exe"}
        cpu = psutil.cpu_percent(interval=None)
        if proc_names & game_markers and cpu >= 40:
            return "gaming"
        if proc_names & work_markers:
            return "work"
        if cpu < 5:
            return "idle"
        return "unknown"
    except Exception:
        return "unknown"


