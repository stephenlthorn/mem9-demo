from pathlib import Path

from pytest_httpx import HTTPXMock

from seed_memories import run_seed


def test_run_seed_provisions_then_writes_all_memories(
    httpx_mock: HTTPXMock, tmp_path: Path, monkeypatch
):
    env = tmp_path / ".env"
    env.write_text(
        "MEM9_API_URL_HOST=http://localhost:8080\n"
        "SEED_FLEET_TENANTS=0\n"
    )

    httpx_mock.add_response(
        method="POST",
        url="http://localhost:8080/v1alpha1/mem9s",
        json={"id": "mnm_abc123"},
        status_code=201,
    )
    for i in range(50):
        httpx_mock.add_response(
            method="POST",
            url="http://localhost:8080/v1alpha2/mem9s/memories",
            json={"id": f"mem_{i:03d}"},
            status_code=201,
        )

    report = run_seed(env_path=env)

    assert report.tenant_id == "mnm_abc123"
    assert report.memories_written == 50
    assert report.fleet_timings == []
    assert "MEM9_TENANT_ID=mnm_abc123" in env.read_text()
    assert "MEM9_PROVISION_MS=" in env.read_text()


def test_run_seed_with_fleet_tenants_writes_measurements(
    httpx_mock: HTTPXMock, tmp_path: Path, monkeypatch
):
    env = tmp_path / ".env"
    env.write_text(
        "MEM9_API_URL_HOST=http://localhost:8080\n"
        "SEED_FLEET_TENANTS=2\n"
    )
    monkeypatch.chdir(tmp_path)

    # Primary provision
    httpx_mock.add_response(method="POST", url="http://localhost:8080/v1alpha1/mem9s",
                            json={"id": "mnm_primary"}, status_code=201)
    # 50 memory writes
    for i in range(50):
        httpx_mock.add_response(method="POST",
                                url="http://localhost:8080/v1alpha2/mem9s/memories",
                                json={"id": f"mem_{i:03d}"}, status_code=201)
    # Fleet tenant 1
    httpx_mock.add_response(method="POST", url="http://localhost:8080/v1alpha1/mem9s",
                            json={"id": "mnm_extra1"}, status_code=201)
    # DELETE attempt — returns 404 (no delete endpoint in upstream)
    httpx_mock.add_response(method="DELETE",
                            url="http://localhost:8080/v1alpha1/mem9s/mnm_extra1",
                            status_code=404)
    # Fleet tenant 2
    httpx_mock.add_response(method="POST", url="http://localhost:8080/v1alpha1/mem9s",
                            json={"id": "mnm_extra2"}, status_code=201)
    httpx_mock.add_response(method="DELETE",
                            url="http://localhost:8080/v1alpha1/mem9s/mnm_extra2",
                            status_code=404)

    report = run_seed(env_path=env)

    assert len(report.fleet_timings) == 2
    fleet_json = tmp_path / "booth_dashboard/static/fleet_measurements.json"
    assert fleet_json.exists()
    import json
    data = json.loads(fleet_json.read_text())
    # 2 extras + 1 primary
    assert len(data["measurements_ms"]) == 3
