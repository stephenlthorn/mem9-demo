"""Tests for the /chat route.

Covers the three response modes of booth_dashboard.server.chat:
  - live:            mem9 retrieval + MiniMax LLM both succeed
  - retrieval-only:  mem9 retrieval succeeds but MiniMax is unavailable
  - canned:          mem9 unreachable OR tenant not provisioned
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from booth_dashboard import server as server_module
from booth_dashboard.llm_client import LlmUnavailable
from booth_dashboard.server import build_app


MEM9_URL = "http://mnemo-server:8080"
TENANT = "mnm_test"
SAMPLE_HITS = [
    {
        "id": "mem_026",
        "content": "Reports to Priya Menon, Director of Platform at Lumos AI.",
        "tags": ["relation", "manager"],
        "scores": {"vector": 0.91, "fts": 0.88, "hybrid": 0.94},
    },
    {
        "id": "mem_028",
        "content": "Ana Ruiz is the skip-level VP of Engineering.",
        "tags": ["relation", "skip-level"],
        "scores": {"vector": 0.62, "fts": 0.21, "hybrid": 0.55},
    },
]


# ---------------------------------------------------------------------------
# canned mode
# ---------------------------------------------------------------------------


def test_chat_no_tenant_falls_back_to_canned():
    """When no tenant is provisioned, respond with a canned turn."""
    app = build_app(mem9_url=MEM9_URL, tenant_id=None)
    client = TestClient(app)

    r = client.post("/chat", json={"message": "Who does Sam report to?"})
    assert r.status_code == 200
    body = r.json()
    assert body["mode"] == "canned"
    assert body["answer"] is not None
    assert "Priya" in body["answer"]
    assert any(m["id"] == "mem_026" for m in body["memories"])


def test_chat_retrieval_failure_falls_back_to_canned(httpx_mock):
    """When mem9 is unreachable, fall back to canned and surface error."""
    import httpx

    httpx_mock.add_exception(httpx.ConnectError("connection refused"))

    app = build_app(mem9_url=MEM9_URL, tenant_id=TENANT)
    client = TestClient(app)

    r = client.post("/chat", json={"message": "Who does Sam report to?"})
    assert r.status_code == 200
    body = r.json()
    assert body["mode"] == "canned"
    assert body["error"] is not None
    assert "mem9 unreachable" in body["error"]
    assert body["answer"] is not None


# ---------------------------------------------------------------------------
# retrieval-only mode
# ---------------------------------------------------------------------------


def test_chat_retrieval_only_when_llm_unavailable(httpx_mock, monkeypatch):
    """Retrieval succeeds, MiniMax absent → mode=retrieval-only, answer=None."""
    monkeypatch.delenv("MINIMAX_API_KEY", raising=False)

    httpx_mock.add_response(
        method="GET",
        url=f"{MEM9_URL}/v1alpha2/mem9s/memories?q=who+does+sam+report+to&limit=5",
        match_headers={"X-API-Key": TENANT},
        json={"hits": SAMPLE_HITS},
    )

    app = build_app(mem9_url=MEM9_URL, tenant_id=TENANT)
    client = TestClient(app)

    r = client.post("/chat", json={"message": "who does sam report to"})
    assert r.status_code == 200
    body = r.json()
    assert body["mode"] == "retrieval-only"
    assert body["answer"] is None
    assert body["memories"] == SAMPLE_HITS
    assert body["error"] is not None
    assert "MINIMAX_API_KEY" in body["error"]


# ---------------------------------------------------------------------------
# live mode
# ---------------------------------------------------------------------------


def test_chat_accepts_memories_key_from_api_mem9_ai(httpx_mock, monkeypatch):
    """api.mem9.ai returns {"memories": [...]} rather than {"hits": [...]}."""
    monkeypatch.delenv("MINIMAX_API_KEY", raising=False)

    httpx_mock.add_response(
        method="GET",
        url=f"{MEM9_URL}/v1alpha2/mem9s/memories?q=who+does+sam+report+to&limit=5",
        match_headers={"X-API-Key": TENANT},
        json={"memories": SAMPLE_HITS, "total": 2, "limit": 5, "offset": 0},
    )

    app = build_app(mem9_url=MEM9_URL, tenant_id=TENANT)
    client = TestClient(app)

    r = client.post("/chat", json={"message": "who does sam report to"})
    assert r.status_code == 200
    body = r.json()
    assert body["mode"] == "retrieval-only"
    assert body["memories"] == SAMPLE_HITS


def test_chat_live_mode_wires_retrieval_and_llm(httpx_mock, monkeypatch):
    """Retrieval + LLM both succeed → mode=live with answer from MiniMax."""
    monkeypatch.setenv("MINIMAX_API_KEY", "fake-key-for-test")

    httpx_mock.add_response(
        method="GET",
        url=f"{MEM9_URL}/v1alpha2/mem9s/memories?q=who+does+sam+report+to&limit=5",
        match_headers={"X-API-Key": TENANT},
        json={"hits": SAMPLE_HITS},
    )

    async def fake_complete(messages, **_kwargs):
        # Verify the system prompt contains the retrieved memory IDs.
        system = messages[0]["content"]
        assert "mem_026" in system
        assert "Priya Menon" in system
        user = messages[1]["content"]
        assert user == "who does sam report to"
        return "Sam reports to [mem_026] Priya Menon."

    monkeypatch.setattr(server_module, "_llm_complete", fake_complete)

    app = build_app(mem9_url=MEM9_URL, tenant_id=TENANT)
    client = TestClient(app)

    r = client.post("/chat", json={"message": "who does sam report to"})
    assert r.status_code == 200
    body = r.json()
    assert body["mode"] == "live"
    assert body["answer"] == "Sam reports to [mem_026] Priya Menon."
    assert body["memories"] == SAMPLE_HITS
    assert body["error"] is None


def test_chat_llm_error_after_retrieval_downgrades_to_retrieval_only(
    httpx_mock, monkeypatch
):
    """Retrieval succeeds but LLM raises → mode=retrieval-only with error."""
    monkeypatch.setenv("MINIMAX_API_KEY", "fake-key-for-test")

    httpx_mock.add_response(
        method="GET",
        url=f"{MEM9_URL}/v1alpha2/mem9s/memories?q=who+does+sam+report+to&limit=5",
        match_headers={"X-API-Key": TENANT},
        json={"hits": SAMPLE_HITS},
    )

    async def boom(messages, **_kwargs):
        raise LlmUnavailable("MiniMax returned 503")

    monkeypatch.setattr(server_module, "_llm_complete", boom)

    app = build_app(mem9_url=MEM9_URL, tenant_id=TENANT)
    client = TestClient(app)

    r = client.post("/chat", json={"message": "who does sam report to"})
    assert r.status_code == 200
    body = r.json()
    assert body["mode"] == "retrieval-only"
    assert body["answer"] is None
    assert body["memories"] == SAMPLE_HITS
    assert "503" in body["error"]


# ---------------------------------------------------------------------------
# input validation
# ---------------------------------------------------------------------------


def test_chat_rejects_empty_message():
    app = build_app(mem9_url=MEM9_URL, tenant_id=TENANT)
    client = TestClient(app)

    r = client.post("/chat", json={"message": "   "})
    assert r.status_code == 400
    assert "required" in r.json()["error"]


def test_chat_rejects_invalid_json():
    app = build_app(mem9_url=MEM9_URL, tenant_id=TENANT)
    client = TestClient(app)

    r = client.post(
        "/chat",
        content="not json",
        headers={"content-type": "application/json"},
    )
    assert r.status_code == 400
