from pathlib import Path


def test_app_js_never_uses_innerhtml():
    app_js = Path("booth_dashboard/static/app.js").read_text()
    assert "innerHTML" not in app_js, "app.js must use safe DOM methods, not innerHTML"


def test_index_html_has_no_inline_scripts_with_innerhtml():
    html = Path("booth_dashboard/static/index.html").read_text()
    assert "innerHTML" not in html
