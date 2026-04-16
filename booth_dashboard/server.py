"""FastAPI booth dashboard: static + server-side proxy to mnemo-server."""
from __future__ import annotations

import os
from pathlib import Path

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

STATIC_DIR = Path(__file__).parent / "static"

try:
    from .canned import CANNED as _CANNED
except ImportError:
    from canned import CANNED as _CANNED  # type: ignore[no-redef]


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
