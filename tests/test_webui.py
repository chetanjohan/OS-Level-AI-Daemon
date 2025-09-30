import json
import types
from unittest.mock import patch

from llm import generate_text


class DummyResponse:
    def __init__(self, text, status_code=200, json_data=None):
        self._text = text
        self.status_code = status_code
        self._json = json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}")

    def json(self):
        if self._json is None:
            raise ValueError("No JSON")
        return self._json

    @property
    def text(self):
        return self._text


def test_webui_json_shape_results():
    prompt = "Hello"
    json_data = {"results": [{"text": "webui response"}]}

    def fake_post(url, json, timeout):
        return DummyResponse(text="", json_data=json_data)

    with patch("requests.post", fake_post):
        out = generate_text(prompt, backend="webui")
        assert "webui response" in out


def test_webui_plain_text():
    prompt = "Hello"

    def fake_post(url, json, timeout):
        return DummyResponse(text="plain text response", json_data=None)

    with patch("requests.post", fake_post):
        out = generate_text(prompt, backend="webui")
        assert "plain text response" in out
