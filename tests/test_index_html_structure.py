"""Structural tests for booth_dashboard/static/index.html.

Each task in the UI redesign plan appends a test function here.
Run from the repo root: pytest tests/test_index_html_structure.py -v
"""
from pathlib import Path

HTML = Path("booth_dashboard/static/index.html").read_text()


def test_hero_has_positioning_tagline():
    """Task 1: Hero should contain the TiDB AI-era positioning tagline."""
    assert "Unified Data Foundation" in HTML


def test_hero_has_memory_wall_hook():
    """Task 1: Hero should contain the memory wall narrative hook."""
    assert "memory wall" in HTML.lower()


def test_customer_proof_strip_exists():
    """Task 1: Customer proof strip class should be present."""
    assert "customer-proof-strip" in HTML


def test_all_customers_present():
    """Task 1: All customer names must appear in the HTML."""
    for name in ["Manus", "Pinterest", "DeepSeek", "Plaud", "Kimi", "Dify", "Flipkart"]:
        assert name in HTML, f"Missing customer: {name}"


def test_lifecycle_tab_has_failure_modes():
    """Task 2: Lifecycle tab should have the three failure modes panel."""
    assert "failure-modes-section" in HTML
    assert "Token Debt" in HTML
    assert "Context Amnesia" in HTML
    assert "Memory Decay" in HTML


def test_lifecycle_tab_has_why_tidb_strip():
    """Task 3: Lifecycle tab should have the Why TiDB 4-card strip."""
    assert "why-tidb-strip" in HTML
    assert "Unified HTAP" in HTML
    assert "VEC_COSINE_DISTANCE" in HTML
    assert "MCP integration" in HTML
    assert "Zero-ETL" in HTML


def test_why_tidb_tab_exists():
    """Task 4: New Why TiDB tab should contain pain points and AI scenarios."""
    assert 'data-tab="whytidb"' in HTML
    assert 'data-tab-panel="whytidb"' in HTML
    assert "Memory fragmentation" in HTML
    assert "Vector + SQL" in HTML
    assert "Multi-tenant isolation" in HTML
    assert "Schema migrations" in HTML
    assert "Agent Long-Term Memory" in HTML
    assert "RAG Unified Storage" in HTML
    assert "AI SaaS Multi-Tenancy" in HTML
    assert "Real-time Feature Library" in HTML


def test_fleet_tab_has_scale_ladder():
    """Task 5: Fleet tab should have scale ladder and proof tiles, not tile grid."""
    assert "scale-ladder" in HTML
    assert "scale-proof-tiles" in HTML
    assert "10M+" in HTML
    # Old tile grid elements should be gone
    assert "spawn-100" not in HTML
    assert "spawn-10000" not in HTML
    assert "fleet-grid" not in HTML


def test_tabs_have_outcome_strips():
    """Task 6: Each tab panel should have at least one tab-outcome-strip."""
    import re
    strips = re.findall(r'tab-outcome-strip', HTML)
    # Expect at least 5 (one per tab: queryflow, chat, lifecycle, unified, proof, whytidb)
    assert len(strips) >= 5, f"Expected at least 5 outcome strips, found {len(strips)}"
