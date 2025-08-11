<<<<<<< HEAD
import httpx, pytest, respx
from src.main import crawl_one, run
=======
import httpx
import pytest
import respx

from main import crawl_one, run
>>>>>>> e772c4167010570baed9b34907b8a8834fe77e81


@pytest.mark.asyncio
@respx.mock
async def test_crawl_one_merges_contact(monkeypatch):
    monkeypatch.setattr("ginio.in_robots", lambda url: True)
    respx.get("https://site.test/").mock(
        return_value=httpx.Response(
            200,
            text="""
        <a href="/contact">Contact</a>
        <p>a@site.test</p>
    """,
        )
    )
    respx.get("https://site.test/contact").mock(
        return_value=httpx.Response(
            200,
            text="""
        <p>support@site.test 123 456 789</p>
    """,
        )
    )
    async with httpx.AsyncClient() as client:
        out = await crawl_one("https://site.test/", client)
    assert "a@site.test" in out["emails"] and "support@site.test" in out["emails"]
    assert any("123" in p for p in out["phones"])


@pytest.mark.asyncio
@respx.mock
async def test_run_full(monkeypatch):
    respx.get("https://serpapi.com/search").mock(
        return_value=httpx.Response(
            200,
            json={
                "organic_results": [{"link": "https://a.pl"}, {"link": "https://b.pl"}]
            },
        )
    )
    # stub robots + strony
    monkeypatch.setattr("ginio.in_robots", lambda url: True)
    respx.get("https://a.pl").mock(
        return_value=httpx.Response(200, text="<title>A</title>")
    )
    respx.get("https://b.pl").mock(
        return_value=httpx.Response(200, text="<title>B</title>")
    )
    monkeypatch.setenv("SERPAPI_KEY", "x")
    results = await run("foo")
    assert {r["title"] for r in results} == {"A", "B"}
