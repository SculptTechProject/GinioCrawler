from unittest.mock import patch


def test_ensure_api_key_env(monkeypatch):
<<<<<<< HEAD
    monkeypatch.setenv("SERPAPI_KEY","secret")
    from src.main import ensure_api_key
    assert ensure_api_key()=="secret"

def test_ensure_api_key_prompt(tmp_path, monkeypatch):
    monkeypatch.setenv("APPDATA", str(tmp_path))
    from src.main import ensure_api_key
=======
    monkeypatch.setenv("SERPAPI_KEY", "secret")
    from main import ensure_api_key

    assert ensure_api_key() == "secret"


def test_ensure_api_key_prompt(tmp_path, monkeypatch):
    monkeypatch.setenv("APPDATA", str(tmp_path))
    from main import ensure_api_key

>>>>>>> e772c4167010570baed9b34907b8a8834fe77e81
    with patch("ginio.simpledialog.askstring", return_value="abc"):
        key = ensure_api_key()
    assert key == "abc"


def test_start_calls_run_without_threading(monkeypatch):
<<<<<<< HEAD
    import src.app_gui as g
=======
    import app_gui as g

>>>>>>> e772c4167010570baed9b34907b8a8834fe77e81
    g.build_ui()
    g.entry_query.delete(0, "end")
    g.entry_query.insert(0, "kawa")
    monkeypatch.setenv("SERPAPI_KEY", "x")

    class DummyThread:
        def __init__(self, target, daemon):
            self.target = target

        def start(self):
            self.target()

    monkeypatch.setattr("ginio_gui.threading.Thread", DummyThread)
    monkeypatch.setattr(
        "ginio_gui.run",
        lambda q: [
            {"url": "u", "title": "t", "emails": [], "phones": [], "contact_url": None}
        ],
    )
    with patch.object(g, "messagebox"):
        g.start()
        assert g.btn_start["state"] == "normal"
        assert "OK — zapisano" in g.status.get()
