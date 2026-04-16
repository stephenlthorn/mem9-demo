"""Thin httpx wrapper around mnemo-server's REST API."""
from __future__ import annotations

import time
from dataclasses import dataclass

import httpx


@dataclass(frozen=True)
class ProvisionResult:
    tenant_id: str
    provision_ms: int


@dataclass(frozen=True)
class Scores:
    vector: float
    fts: float
    hybrid: float


@dataclass(frozen=True)
class Hit:
    id: str
    content: str
    tags: list[str]
    scores: Scores


class Mem9Client:
    def __init__(self, base_url: str, timeout: float = 10.0) -> None:
        self._base_url = base_url.rstrip("/")
        self._http = httpx.Client(base_url=self._base_url, timeout=timeout)

    def provision_tenant(self, utm_source: str | None = None) -> ProvisionResult:
        payload = {"utm_source": utm_source} if utm_source else {}
        t0 = time.perf_counter()
        r = self._http.post("/v1alpha1/mem9s", json=payload)
        elapsed_ms = int((time.perf_counter() - t0) * 1000)
        r.raise_for_status()
        return ProvisionResult(tenant_id=r.json()["id"], provision_ms=elapsed_ms)

    def create_memory(self, tenant_id: str, content: str, tags: list[str]) -> str:
        r = self._http.post(
            "/v1alpha2/mem9s/memories",
            json={"content": content, "tags": tags},
            headers={"X-API-Key": tenant_id},
        )
        r.raise_for_status()
        return r.json().get("id", "")

    def search(self, tenant_id: str, q: str, limit: int = 3) -> list[Hit]:
        r = self._http.get(
            "/v1alpha2/mem9s/memories",
            params={"q": q, "limit": limit},
            headers={"X-API-Key": tenant_id},
        )
        r.raise_for_status()
        hits = []
        for raw in r.json().get("hits", []):
            s = raw["scores"]
            hits.append(
                Hit(
                    id=raw["id"],
                    content=raw["content"],
                    tags=raw.get("tags", []),
                    scores=Scores(vector=s["vector"], fts=s["fts"], hybrid=s["hybrid"]),
                )
            )
        return hits
