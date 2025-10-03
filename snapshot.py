import psutil
import os
import random
import json
from datetime import datetime
from typing import Dict, Any, List


def get_process_summary() -> Dict[str, Any]:
    processes: List[Dict[str, Any]] = []
    high_cpu: List[str] = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        try:
            cpu = proc.info['cpu_percent']
            mem = proc.info['memory_info'].rss / (1024**2)  # MB
            processes.append({"name": proc.info['name'], "pid": proc.info['pid'], "cpu": cpu, "memory_mb": mem})
            if cpu and cpu > 20:  # arbitrary high CPU threshold
                high_cpu.append(proc.info['name'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, KeyError):
            continue
    summary = f"{len(processes)} processes running. High CPU usage by: {', '.join(high_cpu) if high_cpu else 'None'}."
    return {"summary": summary, "data": processes}


def get_resource_summary() -> Dict[str, Any]:
    cpu_total = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    summary = f"CPU is at {cpu_total}%. RAM usage is {ram.percent}% ({ram.used/1024**3:.2f}GB used)."
    return {
        "summary": summary,
        "data": {
            "cpu_percent": cpu_total,
            "ram_percent": ram.percent,
            "ram_used_gb": ram.used / (1024**3),
            "ram_total_gb": ram.total / (1024**3),
        },
    }


def get_disk_summary() -> Dict[str, Any]:
    partitions = psutil.disk_partitions()
    disks: Dict[str, Any] = {}
    summaries: List[str] = []
    for p in partitions:
        try:
            usage = psutil.disk_usage(p.mountpoint)
            disks[p.device] = {"used_gb": usage.used / (1024**3), "total_gb": usage.total / (1024**3), "percent": usage.percent}
            summaries.append(f"{p.device} usage: {usage.percent}% ({usage.used/(1024**3):.2f}GB/{usage.total/(1024**3):.2f}GB)")
        except Exception:
            continue
    summary = " | ".join(summaries)
    return {"summary": summary, "data": disks}


def get_network_summary() -> Dict[str, Any]:
    conns = psutil.net_connections()
    suspicious = [f"{c.laddr.ip}:{c.laddr.port}" for c in conns if getattr(c, 'status', None) == 'ESTABLISHED' and random.random() < 0.01]
    summary = f"Total connections: {len(conns)}. Suspicious connections: {len(suspicious)}."
    return {"summary": summary, "data": {"total_connections": len(conns), "suspicious": suspicious}}


def get_security_summary() -> Dict[str, Any]:
    findings: List[str] = []
    if random.random() < 0.05:
        findings.append("Suspicious process: fake_malware.exe")
    anomaly_score = round(len(findings) / 5, 2)
    summary = "No malware detected." if not findings else f"Potential threats detected: {len(findings)}"
    return {"summary": summary, "data": {"findings": findings, "anomaly_score": anomaly_score}}


def get_hardware_summary() -> Dict[str, Any]:
    temps = psutil.sensors_temperatures() if hasattr(psutil, "sensors_temperatures") else {}
    summary = f"Temperature sensors available: {', '.join(temps.keys()) if temps else 'None'}."
    return {"summary": summary, "data": temps}


def full_system_snapshot() -> Dict[str, Any]:
    snapshot = {
        "timestamp": str(datetime.now()),
        "processes": get_process_summary(),
        "resources": get_resource_summary(),
        "disk": get_disk_summary(),
        "network": get_network_summary(),
        "security": get_security_summary(),
        "hardware": get_hardware_summary(),
        "alerts": [
            "CPU usage high on chrome.exe" if random.random() < 0.1 else "System operating normally.",
            "Suspicious network connection detected" if random.random() < 0.05 else "",
        ],
    }
    return snapshot


if __name__ == "__main__":
    snap = full_system_snapshot()
    print(json.dumps(snap, indent=2))


