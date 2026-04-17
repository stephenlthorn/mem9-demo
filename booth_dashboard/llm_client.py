"""MiniMax chat client using the OpenAI-compatible endpoint.

Thin async wrapper around httpx; no SDK dependency. The booth dashboard
reads MINIMAX_API_KEY from the environment — if it's missing, callers
raise LlmUnavailable and the /chat route falls back to retrieval-only.
"""
from __future__ import annotations

import os
import re
from typing import Sequence

import httpx

DEFAULT_BASE_URL = "https://api.minimax.io/v1"
DEFAULT_MODEL = "MiniMax-M2.7"

# MiniMax-M2.7 (and other reasoning models) can emit <think>...</think>
# blocks before the actual answer. Strip them before returning so the UI
# shows only the user-facing response.
_THINK_BLOCK = re.compile(r"<think>.*?</think>\s*", re.DOTALL | re.IGNORECASE)


def _strip_reasoning(text: str) -> str:
    """Remove <think>...</think> blocks and trim surrounding whitespace."""
    return _THINK_BLOCK.sub("", text).strip()


class LlmUnavailable(RuntimeError):
    """Raised when the LLM cannot be called (missing key, network failure, bad response)."""


async def complete(
    messages: Sequence[dict[str, str]],
    timeout: float = 15.0,
    temperature: float = 0.2,
    max_tokens: int = 400,
) -> str:
    """Send a chat completion request to MiniMax and return the assistant text.

    Raises LlmUnavailable if MINIMAX_API_KEY is unset or the upstream call fails.
    """
    api_key = os.environ.get("MINIMAX_API_KEY")
    if not api_key:
        raise LlmUnavailable("MINIMAX_API_KEY not set")

    base_url = os.environ.get("MINIMAX_BASE_URL", DEFAULT_BASE_URL)
    model = os.environ.get("MINIMAX_MODEL", DEFAULT_MODEL)

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                f"{base_url.rstrip('/')}/chat/completions",
                json={
                    "model": model,
                    "messages": list(messages),
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                },
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
            )
    except httpx.HTTPError as exc:
        raise LlmUnavailable(f"network error calling MiniMax: {exc}") from exc

    if response.status_code != 200:
        raise LlmUnavailable(
            f"MiniMax returned {response.status_code}: {response.text[:200]}"
        )

    try:
        body = response.json()
    except ValueError as exc:
        raise LlmUnavailable(f"MiniMax returned non-JSON: {response.text[:200]}") from exc

    choices = body.get("choices") or []
    if not choices:
        raise LlmUnavailable(f"MiniMax returned no choices: {body}")

    content = (choices[0].get("message") or {}).get("content")
    if not content:
        raise LlmUnavailable(f"MiniMax response missing content: {body}")

    cleaned = _strip_reasoning(content)
    if not cleaned:
        raise LlmUnavailable("MiniMax response was entirely reasoning with no answer")
    return cleaned
