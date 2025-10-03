"""
privacy.py
Simple privacy preference levels and redaction helpers.
"""
from __future__ import annotations

from typing import Any, Dict


class PrivacyLevel:
    STRICT = "strict"
    BALANCED = "balanced"
    OPEN = "open"


def normalize_level(level: str | None) -> str:
    val = (level or PrivacyLevel.BALANCED).lower()
    if val not in {PrivacyLevel.STRICT, PrivacyLevel.BALANCED, PrivacyLevel.OPEN}:
        return PrivacyLevel.BALANCED
    return val


def redact_payload(payload: Dict[str, Any], level: str) -> Dict[str, Any]:
    lvl = normalize_level(level)
    redacted: Dict[str, Any] = dict(payload)
    if lvl == PrivacyLevel.STRICT:
        redacted.pop("process_list", None)
        redacted.pop("connections", None)
    elif lvl == PrivacyLevel.BALANCED:
        # keep counts but drop names/hosts
        if "process_list" in redacted:
            redacted["process_count"] = len(redacted["process_list"]) if isinstance(redacted["process_list"], list) else 0
            redacted.pop("process_list", None)
        if "connections" in redacted:
            redacted["connection_count"] = len(redacted["connections"]) if isinstance(redacted["connections"], list) else 0
            redacted.pop("connections", None)
    else:
        # OPEN: leave as-is
        pass
    return redacted


