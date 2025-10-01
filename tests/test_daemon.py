import builtins
from main import Daemon

# MCP test


def test_daemon_run_once(monkeypatch):
    # Force fetch_task to return a predictable prompt
    monkeypatch.setattr('main.fetch_task', lambda: 'Unit test prompt')
    d = Daemon(interval=1, max_tokens=10, force_mock=True)
    resp = d.run_once()
    assert resp is not None
    assert 'Unit test prompt' in resp
