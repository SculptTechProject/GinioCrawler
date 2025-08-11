import httpx, pytest, respx
from main import fetch

@pytest.mark.asyncio
@respx.mock
async def test_fetch_ok(monkeypatch):
    monkeypatch.setattr("ginio.in_robots", lambda url: True)
    respx.get("https://x.test/ok").mock(return_value=httpx.Response(200, text="<h1>ok</h1>"))
    async with httpx.AsyncClient() as client:
        html = await fetch("https://x.test/ok", client)
    assert "ok" in html

@pytest.mark.asyncio
@respx.mock
async def test_fetch_respects_robots(monkeypatch):
    monkeypatch.setattr("ginio.in_robots", lambda url: False)
    async with httpx.AsyncClient() as client:
        assert await fetch("https://x.test/nope", client) is None
