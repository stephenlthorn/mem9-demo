"""Tests for booth_dashboard.llm_client helpers."""
from __future__ import annotations

import pytest

from booth_dashboard.llm_client import (
    LlmUnavailable,
    _strip_reasoning,
    complete,
)


# ---------------------------------------------------------------------------
# _strip_reasoning
# ---------------------------------------------------------------------------


def test_strip_reasoning_removes_think_block():
    raw = "<think>\nLet me consider...\n</think>\n\nSam reports to Priya."
    assert _strip_reasoning(raw) == "Sam reports to Priya."


def test_strip_reasoning_removes_multiple_blocks():
    raw = "<think>one</think>A <think>two</think>B"
    assert _strip_reasoning(raw) == "A B"


def test_strip_reasoning_passes_through_plain_text():
    raw = "Just an answer with [mem_026] citations."
    assert _strip_reasoning(raw) == raw


def test_strip_reasoning_handles_empty_string():
    assert _strip_reasoning("") == ""


def test_strip_reasoning_trims_surrounding_whitespace():
    raw = "  <think>noise</think>\n\nreal answer\n\n"
    assert _strip_reasoning(raw) == "real answer"


# ---------------------------------------------------------------------------
# complete() — env-gated
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_complete_raises_when_api_key_missing(monkeypatch):
    monkeypatch.delenv("MINIMAX_API_KEY", raising=False)
    with pytest.raises(LlmUnavailable, match="MINIMAX_API_KEY"):
        await complete([{"role": "user", "content": "hi"}])


@pytest.mark.asyncio
async def test_complete_strips_reasoning_from_response(httpx_mock, monkeypatch):
    monkeypatch.setenv("MINIMAX_API_KEY", "fake-key")
    httpx_mock.add_response(
        method="POST",
        url="https://api.minimax.io/v1/chat/completions",
        json={
            "choices": [
                {
                    "message": {
                        "content": (
                            "<think>\nReasoning about the question...\n</think>\n"
                            "Sam reports to [mem_026] Priya Menon."
                        )
                    }
                }
            ]
        },
    )
    result = await complete([{"role": "user", "content": "who does sam report to"}])
    assert result == "Sam reports to [mem_026] Priya Menon."


@pytest.mark.asyncio
async def test_complete_raises_when_only_reasoning_returned(httpx_mock, monkeypatch):
    monkeypatch.setenv("MINIMAX_API_KEY", "fake-key")
    httpx_mock.add_response(
        method="POST",
        url="https://api.minimax.io/v1/chat/completions",
        json={"choices": [{"message": {"content": "<think>no real answer</think>"}}]},
    )
    with pytest.raises(LlmUnavailable, match="entirely reasoning"):
        await complete([{"role": "user", "content": "hi"}])
