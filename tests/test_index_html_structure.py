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
