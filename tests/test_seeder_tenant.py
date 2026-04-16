import pytest
from pytest_httpx import HTTPXMock

from mem9_client import Mem9Client


def test_provision_tenant_returns_id_and_timing(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="POST",
        url="http://localhost:8080/v1alpha1/mem9s",
        json={"id": "mnm_abc123"},
        status_code=201,
    )

    client = Mem9Client(base_url="http://localhost:8080")
    result = client.provision_tenant(utm_source="gcn-booth")

    assert result.tenant_id == "mnm_abc123"
    assert result.provision_ms >= 0
    assert result.provision_ms < 5000


def test_create_memory_sets_api_key_header(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="POST",
        url="http://localhost:8080/v1alpha2/mem9s/memories",
        match_headers={"X-API-Key": "mnm_abc123"},
        json={"id": "mem_001"},
        status_code=201,
    )

    client = Mem9Client(base_url="http://localhost:8080")
    mem_id = client.create_memory(
        tenant_id="mnm_abc123",
        content="Sam drinks tea, not coffee.",
        tags=["preference", "bonus"],
    )

    assert mem_id == "mem_001"
