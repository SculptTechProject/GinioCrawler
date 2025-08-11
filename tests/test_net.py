import httpx, respx, pytest
from src.main import fetch

@respx.mock
@pytest.mark.anyio
async def test_fetch_ok(monkeypatch):
    monkeypatch.setattr("src.main.in_robots", lambda u: True)
    respx.get("https://x.test/ok").mock(return_value=httpx.Response(200, text="<h1>ok</h1>"))
    async with httpx.AsyncClient() as c:
        html = await fetch("https://x.test/ok", c)
    assert "ok" in html

@respx.mock
@pytest.mark.anyio
async def test_fetch_respects_robots(monkeypatch):
    monkeypatch.setattr("src.main.in_robots", lambda u: False)
    async with httpx.AsyncClient() as c:
        assert await fetch("https://x.test/nope", c) is None
