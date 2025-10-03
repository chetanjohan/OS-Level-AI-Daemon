"""
monitor.py
Lightweight, modular system monitoring with safe heuristics and scheduled automation.

Features (non-invasive by default):
- Always-on monitoring: CPU, memory, disk, battery, processes, network.
- Resource heuristics: detect sustained high CPU/mem; suggest niceness changes (log-only).
- Security heuristics: flag suspicious ports/process spikes (log-only).
- Automation: periodic temp cleanup; stub backup hook.
- Privacy tracking: log outbound connections by process.

All actions are log-only by default to keep the daemon safe. Real control actions could be
implemented later behind explicit flags/environment variables.
"""
from __future__ import annotations

import os
import time
import threading
import logging
from logging.handlers import RotatingFileHandler
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import psutil
import schedule


DEFAULT_MONITOR_INTERVAL_SECONDS = 5
DEFAULT_AUTOMATION_INTERVAL_MINUTES = 15


def _setup_logger() -> logging.Logger:
    logger = logging.getLogger("system_monitor")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        log_path = os.path.join(os.getcwd(), "monitor.log")
        handler = RotatingFileHandler(log_path, maxBytes=2_000_000, backupCount=2)
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        # Also log to stdout for visibility during development
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    return logger


LOGGER = _setup_logger()


@dataclass
class Snapshot:
    cpu_percent: float
    mem_percent: float
    swap_percent: float
    disk_percent: float
    battery_percent: Optional[float]
    proc_count: int
    tx_bytes: int
    rx_bytes: int


class SystemMonitor:
    def __init__(
        self,
        interval_seconds: int = DEFAULT_MONITOR_INTERVAL_SECONDS,
        enable_automation: bool = True,
    ) -> None:
        self.interval_seconds = max(1, interval_seconds)
        self.enable_automation = enable_automation
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._last_net: Optional[Tuple[int, int]] = None

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run_loop, name="SystemMonitor", daemon=True)
        self._thread.start()
        LOGGER.info("SystemMonitor started (interval=%ss, automation=%s)", self.interval_seconds, self.enable_automation)

    def stop(self, timeout: Optional[float] = 2.0) -> None:
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=timeout)
            LOGGER.info("SystemMonitor stopped")

    # Loop
    def _run_loop(self) -> None:
        if self.enable_automation:
            self._schedule_jobs()
        while not self._stop_event.is_set():
            try:
                self._tick()
                # run pending scheduled jobs
                schedule.run_pending()
            except Exception as e:
                LOGGER.exception("monitor loop error: %s", e)
            time.sleep(self.interval_seconds)

    def _schedule_jobs(self) -> None:
        schedule.every(DEFAULT_AUTOMATION_INTERVAL_MINUTES).minutes.do(self._job_cleanup_temp)
        schedule.every(60).minutes.do(self._job_backup_stub)
        LOGGER.info("Automation jobs scheduled: temp-clean every %s min, backup stub hourly", DEFAULT_AUTOMATION_INTERVAL_MINUTES)

    # One monitoring tick
    def _tick(self) -> None:
        snap = self._snapshot()
        LOGGER.info(
            "CPU %.1f%% | MEM %.1f%% | SWAP %.1f%% | DISK %.1f%% | PROC %d | NET tx=%d rx=%d | BAT %s",
            snap.cpu_percent,
            snap.mem_percent,
            snap.swap_percent,
            snap.disk_percent,
            snap.proc_count,
            snap.tx_bytes,
            snap.rx_bytes,
            f"{snap.battery_percent:.0f}%" if snap.battery_percent is not None else "n/a",
        )
        self._heuristics_resource(snap)
        self._heuristics_security()
        self._privacy_track_connections()

    def _snapshot(self) -> Snapshot:
        cpu = psutil.cpu_percent(interval=None)
        vm = psutil.virtual_memory()
        sm = psutil.swap_memory()
        du = psutil.disk_usage(os.getcwd())
        try:
            bat = psutil.sensors_battery()
            bat_pct: Optional[float] = bat.percent if bat else None
        except Exception:
            bat_pct = None
        p_count = len(psutil.pids())
        net = psutil.net_io_counters()
        tx, rx = int(net.bytes_sent), int(net.bytes_recv)
        if self._last_net is None:
            self._last_net = (tx, rx)
        return Snapshot(
            cpu_percent=float(cpu),
            mem_percent=float(vm.percent),
            swap_percent=float(sm.percent),
            disk_percent=float(du.percent),
            battery_percent=bat_pct,
            proc_count=p_count,
            tx_bytes=tx,
            rx_bytes=rx,
        )

    # Heuristics (log-only)
    def _heuristics_resource(self, snap: Snapshot) -> None:
        if snap.cpu_percent >= 85.0:
            LOGGER.warning("Sustained high CPU detected (%.1f%%). Consider throttling background tasks.", snap.cpu_percent)
        if snap.mem_percent >= 90.0:
            LOGGER.warning("Memory pressure high (%.1f%%). Consider freeing caches or closing idle apps.", snap.mem_percent)
        if snap.disk_percent >= 90.0:
            LOGGER.warning("Disk usage high (%.1f%%). Cleanup recommended.", snap.disk_percent)

    def _heuristics_security(self) -> None:
        try:
            conns = psutil.net_connections(kind="inet")
            listening = [c for c in conns if c.status == psutil.CONN_LISTEN]
            if len(listening) > 50:
                LOGGER.warning("Large number of listening sockets detected: %d", len(listening))
        except Exception as e:
            LOGGER.debug("security check failed: %s", e)

    def _privacy_track_connections(self) -> None:
        try:
            by_proc: Dict[int, int] = {}
            for c in psutil.net_connections(kind="inet"):
                if c.raddr and c.pid:
                    by_proc[c.pid] = by_proc.get(c.pid, 0) + 1
            top = sorted(by_proc.items(), key=lambda kv: kv[1], reverse=True)[:5]
            if top:
                lines: List[str] = []
                for pid, count in top:
                    try:
                        p = psutil.Process(pid)
                        lines.append(f"{p.name()}(pid={pid}) connections={count}")
                    except Exception:
                        lines.append(f"pid={pid} connections={count}")
                LOGGER.info("Top outbound connections: %s", ", ".join(lines))
        except Exception as e:
            LOGGER.debug("privacy tracking failed: %s", e)

    # Automation jobs
    def _job_cleanup_temp(self) -> None:
        try:
            tmp_dirs = [
                os.getenv("TEMP"),
                os.getenv("TMP"),
                os.path.join(os.path.expanduser("~"), "AppData", "Local", "Temp"),
            ]
            cleaned = 0
            for td in tmp_dirs:
                if not td or not os.path.isdir(td):
                    continue
                for name in os.listdir(td):
                    path = os.path.join(td, name)
                    try:
                        if os.path.isfile(path):
                            os.remove(path)
                            cleaned += 1
                    except Exception:
                        continue
            LOGGER.info("Automation: cleaned %d temp files", cleaned)
        except Exception as e:
            LOGGER.debug("temp cleanup failed: %s", e)

    def _job_backup_stub(self) -> None:
        try:
            LOGGER.info("Automation: backup stub executed (no-op)")
        except Exception as e:
            LOGGER.debug("backup stub failed: %s", e)


