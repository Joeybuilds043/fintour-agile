import os
from pathlib import Path
from streamlit.testing.v1 import AppTest

def test_every_workspace_page_executes_without_exceptions(monkeypatch):
    monkeypatch.setenv("HORIZON_DISABLE_REMOTE_MEDIA", "1")
    monkeypatch.setenv("HORIZON_DISABLE_EXTERNAL_DATA", "1")
    for page in sorted(Path("pages").glob("*.py")):
        app = AppTest.from_file(str(page)).run(timeout=45)
        assert not app.exception, f"{page}: {app.exception}"
