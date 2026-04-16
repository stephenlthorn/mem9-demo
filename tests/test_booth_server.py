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


def test_proxy_get_injects_api_key_and_forwards(httpx_mock):
    httpx_mock.add_response(
        method="GET",
        url="http://mnemo-server:8080/v1alpha2/mem9s/memories?q=pipeline&limit=3",
        match_headers={"X-API-Key": "mnm_test"},
        json={"hits": []},
    )

    app = build_app(mem9_url="http://mnemo-server:8080", tenant_id="mnm_test")
    client = TestClient(app)
    r = client.get("/api/v1alpha2/mem9s/memories", params={"q": "pipeline", "limit": 3})

    assert r.status_code == 200
    assert r.json() == {"hits": []}


def test_proxy_refuses_when_tenant_unset():
    app = build_app(mem9_url="http://mnemo-server:8080", tenant_id=None)
    client = TestClient(app)
    r = client.get("/api/v1alpha2/mem9s/memories", params={"q": "x"})
    assert r.status_code == 503
    assert r.json()["error"].startswith("tenant not provisioned")


def test_canned_returns_three_queries():
    app = build_app(mem9_url="http://mnemo-server:8080", tenant_id="mnm_test")
    client = TestClient(app)
    r = client.get("/canned")
    assert r.status_code == 200
    data = r.json()
    assert set(data.keys()) == {"q1", "q2", "q3"}
    for key in ("q1", "q2", "q3"):
        assert len(data[key]["hits"]) == 3
        assert "label" in data[key]
