import os
from llm import generate_text


def test_generate_text_mock_default():
    # By default, in environments without llama-cpp, generate_text should return the mock prefix
    out = generate_text("Test prompt", max_tokens=10, force_mock=True)
    assert out.startswith("[mock-lm] Generated"), "Expected mock prefix when force_mock=True"


def test_generate_text_echoes_prompt():
    prompt = "Say hello"
    out = generate_text(prompt, max_tokens=5, force_mock=True)
    assert "Say hello" in out
