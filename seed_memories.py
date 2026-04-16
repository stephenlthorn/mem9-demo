"""Seed the booth demo: provision a tenant, write 50 memories, capture timings."""
from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import dotenv_values

from corpus import MEMORIES
from env_writer import append_env_var
from mem9_client import Mem9Client


@dataclass
class SeedReport:
    tenant_id: str
    provision_ms: int
    memories_written: int
    fleet_timings: list[int] = field(default_factory=list)


def run_seed(env_path: Path) -> SeedReport:
    env = dotenv_values(env_path)
    base_url = env.get("MEM9_API_URL_HOST") or os.environ.get("MEM9_API_URL_HOST")
    if not base_url:
        raise RuntimeError("MEM9_API_URL_HOST not set in .env")
    fleet_n = int(env.get("SEED_FLEET_TENANTS", "0") or "0")

    client = Mem9Client(base_url=base_url)

    primary = client.provision_tenant(utm_source="gcn-booth")
    append_env_var(env_path, "MEM9_TENANT_ID", primary.tenant_id)
    append_env_var(env_path, "MEM9_PROVISION_MS", str(primary.provision_ms))

    for mem in MEMORIES:
        client.create_memory(
            tenant_id=primary.tenant_id,
            content=mem["content"],
            tags=mem["tags"],
        )

    fleet_timings: list[int] = []
    for _ in range(fleet_n):
        extra = client.provision_tenant(utm_source="gcn-booth-fleet")
        fleet_timings.append(extra.provision_ms)
        # Phase 0.4: mnemo-server has no DELETE endpoint — cleanup is best-effort
        try:
            client._http.delete(
                f"/v1alpha1/mem9s/{extra.tenant_id}",
                headers={"X-API-Key": extra.tenant_id},
            )
        except Exception:
            pass

    if fleet_timings:
        _write_fleet_measurements(fleet_timings + [primary.provision_ms])

    return SeedReport(
        tenant_id=primary.tenant_id,
        provision_ms=primary.provision_ms,
        memories_written=len(MEMORIES),
        fleet_timings=fleet_timings,
    )


def _write_fleet_measurements(ms_list: list[int]) -> None:
    import json

    out = Path("booth_dashboard/static/fleet_measurements.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"measurements_ms": ms_list}, indent=2) + "\n")


if __name__ == "__main__":
    env = Path(".env")
    report = run_seed(env)
    print(
        f"tenant_id={report.tenant_id} "
        f"provision_ms={report.provision_ms} "
        f"memories={report.memories_written} "
        f"fleet={report.fleet_timings}"
    )
