from unittest.mock import patch

def test_ensure_api_key_env(monkeypatch):
    monkeypatch.setenv("SERPAPI_KEY","secret")
    from src.app_gui import ensure_api_key
    assert ensure_api_key() == "secret"

def test_ensure_api_key_prompt(tmp_path, monkeypatch):
    monkeypatch.delenv("SERPAPI_KEY", raising=False)
    monkeypatch.setenv("APPDATA", str(tmp_path))
    from src.app_gui import ensure_api_key
    with patch("src.app_gui.simpledialog.askstring", return_value="abc"):
        assert ensure_api_key() == "abc"

def test_start_calls_run_without_threading(monkeypatch):
    import src.app_gui as g
    g.build_ui()
    g.entry_query.delete(0,'end'); g.entry_query.insert(0,"kawa")
    monkeypatch.setenv("SERPAPI_KEY","x")

    class DummyThread:
        def __init__(self, target, daemon): self.target = target
        def start(self): self.target()

    monkeypatch.setattr("src.app_gui.threading.Thread", DummyThread)
    monkeypatch.setattr(g.root, "after", lambda ms, fn: fn(), raising=False)

    async def fake_run(q):
        return [{"url":"u","title":"t","emails":[],"phones":[],"contact_url":None}]
    monkeypatch.setattr("src.app_gui.run", fake_run)

    with patch.object(g, "messagebox"):
        g.start()
        assert g.btn_start["state"] == "normal"
        assert "OK — zapisano" in g.status.get()
        try:
            g.root.destroy()
        except Exception:
            pass

