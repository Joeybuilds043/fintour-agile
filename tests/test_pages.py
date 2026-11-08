import os
from pathlib import Path
from streamlit.testing.v1 import AppTest

def test_every_workspace_page_executes_without_exceptions(monkeypatch):
    monkeypatch.setenv("HORIZON_DISABLE_REMOTE_MEDIA", "1")
    monkeypatch.setenv("HORIZON_DISABLE_EXTERNAL_DATA", "1")
    root = Path.cwd()
    app = AppTest.from_file(root / "app.py").run(timeout=45)
    assert not app.exception, app.exception
    for page in sorted((root / "pages").glob("*.py")):
        relative_page = page.relative_to(root).as_posix()
        app.switch_page(relative_page).run(timeout=45)
        assert not app.exception, f"{relative_page}: {app.exception}"
