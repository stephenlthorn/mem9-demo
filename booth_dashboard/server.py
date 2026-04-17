"""FastAPI booth dashboard: static + server-side proxy to mnemo-server."""
from __future__ import annotations

import os
from pathlib import Path

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

# Auto-load repo-root .env so MINIMAX_API_KEY and friends are picked up
# regardless of how uvicorn was launched (demo.sh, manual, tests).
# Fails silently if dotenv isn't installed or .env doesn't exist.
try:
    from dotenv import load_dotenv

    _ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
    if _ENV_PATH.exists():
        load_dotenv(_ENV_PATH, override=False)
except ImportError:
    pass

STATIC_DIR = Path(__file__).parent / "static"

try:
    from .canned import CANNED as _CANNED, CANNED_CHAT as _CANNED_CHAT
    from .llm_client import LlmUnavailable, complete as _llm_complete
except ImportError:
    from canned import CANNED as _CANNED, CANNED_CHAT as _CANNED_CHAT  # type: ignore[no-redef]
    from llm_client import LlmUnavailable, complete as _llm_complete  # type: ignore[no-redef]


def _build_system_prompt(memories: list[dict]) -> str:
    mem_lines = [
        f"- [{m.get('id','?')}] {m.get('content','').strip()}"
        for m in memories
        if m.get("content")
    ]
    mem_block = "\n".join(mem_lines) if mem_lines else "(none retrieved)"
    return (
        "You are Sam Chen's AI assistant with persistent memory on TiDB Cloud Zero. "
        "You are stateless; every memory you know comes from the context plane "
        "retrieved pre-agent for this specific question.\n\n"
        "Rules:\n"
        "- Answer using ONLY the retrieved memories below.\n"
        "- Cite them inline with their ID in square brackets, e.g. [mem_026].\n"
        "- If the memories do not contain the answer, say so plainly. Do not fabricate.\n"
        "- Keep answers to 2-4 sentences.\n\n"
        f"Retrieved memories:\n{mem_block}"
    )


def _pick_canned_chat(user_msg: str) -> dict | None:
    """Fuzzy-match an incoming message to a canned chat turn."""
    lowered = user_msg.lower()
    for key, turn in _CANNED_CHAT.items():
        if key.lower() in lowered or lowered in key.lower():
            return turn
    # Default: return the first canned turn so offline mode always has *something*.
    return next(iter(_CANNED_CHAT.values()), None)


def build_app(mem9_url: str, tenant_id: str | None) -> FastAPI:
    app = FastAPI(title="mem9-demo booth dashboard")

    @app.get("/healthz")
    def healthz() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/meta")
    def meta() -> dict[str, str | int | None]:
        provision_ms_raw = os.environ.get("MEM9_PROVISION_MS")
        return {
            "tenant_id": tenant_id,
            "provision_ms": int(provision_ms_raw) if provision_ms_raw else None,
            "region": os.environ.get("MEM9_REGION") or None,
        }

    @app.get("/canned")
    def canned() -> dict:
        return _CANNED

    @app.post("/chat")
    async def chat(request: Request) -> JSONResponse:
        """Chat with the agent: retrieve → prompt → LLM → graceful fallback.

        Response shape: {answer, memories, mode, error}
          mode="live"            → MiniMax answered using retrieved memories
          mode="retrieval-only"  → retrieval worked, LLM unavailable (showing memories only)
          mode="canned"          → offline / tenant missing; using canned turn
        """
        try:
            body = await request.json()
        except ValueError:
            return JSONResponse({"error": "invalid JSON body"}, status_code=400)

        user_msg = (body.get("message") or "").strip()
        if not user_msg:
            return JSONResponse({"error": "message is required"}, status_code=400)

        # No tenant provisioned → canned path only (demo offline scenario).
        if not tenant_id:
            canned = _pick_canned_chat(user_msg)
            return JSONResponse({
                "answer": canned["answer"] if canned else None,
                "memories": canned["memories"] if canned else [],
                "mode": "canned",
                "error": None,
            })

        # 1. Retrieve memories from mem9.
        memories: list[dict] = []
        retrieval_error: str | None = None
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                r = await client.get(
                    f"{mem9_url.rstrip('/')}/v1alpha2/mem9s/memories",
                    params={"q": user_msg, "limit": 5},
                    headers={"X-API-Key": tenant_id},
                )
            if r.status_code == 200:
                memories = r.json().get("hits", [])
            else:
                retrieval_error = f"mem9 returned {r.status_code}"
        except httpx.HTTPError as exc:
            retrieval_error = f"mem9 unreachable: {exc}"

        # If retrieval failed entirely, fall back to canned.
        if not memories and retrieval_error:
            canned = _pick_canned_chat(user_msg)
            return JSONResponse({
                "answer": canned["answer"] if canned else None,
                "memories": canned["memories"] if canned else [],
                "mode": "canned",
                "error": retrieval_error,
            })

        # 2. Call MiniMax with memories as context.
        messages = [
            {"role": "system", "content": _build_system_prompt(memories)},
            {"role": "user", "content": user_msg},
        ]
        try:
            answer = await _llm_complete(messages)
            return JSONResponse({
                "answer": answer,
                "memories": memories,
                "mode": "live",
                "error": None,
            })
        except LlmUnavailable as exc:
            # Retrieval succeeded but LLM is down — show memories only.
            return JSONResponse({
                "answer": None,
                "memories": memories,
                "mode": "retrieval-only",
                "error": str(exc),
            })

    @app.api_route(
        "/api/{path:path}",
        methods=["GET", "POST", "DELETE"],
    )
    async def proxy(path: str, request: Request) -> JSONResponse:
        if not tenant_id:
            return JSONResponse(
                {"error": "tenant not provisioned; run seed_memories.py"},
                status_code=503,
            )
        url = f"{mem9_url.rstrip('/')}/{path}"
        headers = {"X-API-Key": tenant_id}
        if ct := request.headers.get("content-type"):
            headers["content-type"] = ct
        async with httpx.AsyncClient() as client:
            upstream = await client.request(
                method=request.method,
                url=url,
                params=dict(request.query_params),
                headers=headers,
                content=await request.body(),
            )
        try:
            body = upstream.json()
        except ValueError:
            body = {"raw": upstream.text}
        return JSONResponse(body, status_code=upstream.status_code)

    if STATIC_DIR.exists():
        app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

        @app.get("/")
        def root() -> FileResponse:
            return FileResponse(STATIC_DIR / "index.html")

    return app


def _app_from_env() -> FastAPI:
    return build_app(
        mem9_url=os.environ.get("MEM9_API_URL", "http://localhost:8080"),
        tenant_id=os.environ.get("MEM9_TENANT_ID"),
    )


app = _app_from_env()
