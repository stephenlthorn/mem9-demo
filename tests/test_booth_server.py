from fastapi.testclient import TestClient

from booth_dashboard.server import build_app


def test_healthz_returns_ok():
    app = build_app(mem9_url="http://mnemo-server:8080", tenant_id="mnm_test")
    client = TestClient(app)
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_meta_returns_tenant_fields():
    app = build_app(mem9_url="http://mnemo-server:8080", tenant_id="mnm_test")
    client = TestClient(app)
    r = client.get("/meta")
    assert r.status_code == 200
    body = r.json()
    assert body["tenant_id"] == "mnm_test"
    assert "provision_ms" in body
