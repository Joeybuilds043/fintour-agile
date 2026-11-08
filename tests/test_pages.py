import os
from pathlib import Path
from streamlit.testing.v1 import AppTest


def test_every_workspace_page_executes_in_light_and_dark_modes(monkeypatch):
    monkeypatch.setenv("HORIZON_DISABLE_REMOTE_MEDIA", "1")
    monkeypatch.setenv("HORIZON_DISABLE_EXTERNAL_DATA", "1")
    root = Path.cwd()
    pages = sorted((root / "pages").glob("*.py"))

    for theme in ("Light", "Dark"):
        app = AppTest.from_file(root / "app.py")
        app.session_state["voyage_theme"] = theme
        app.run(timeout=45)
        assert not app.exception, f"Homepage ({theme}): {app.exception}"

        for page in pages:
            relative_page = page.relative_to(root).as_posix()
            app.switch_page(relative_page).run(timeout=45)
            assert not app.exception, f"{relative_page} ({theme}): {app.exception}"
