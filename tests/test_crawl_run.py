import httpx, respx, pytest
from src.main import crawl_one, run

@respx.mock
@pytest.mark.anyio
async def test_crawl_one_merges_contact(monkeypatch):
    monkeypatch.setattr("src.main.in_robots", lambda u: True)
    respx.get("https://site.test/").mock(return_value=httpx.Response(200, text="""
        <a href="/contact">Contact</a><p>a@site.test</p>"""))
    respx.get("https://site.test/contact").mock(return_value=httpx.Response(200, text="""
        <p>support@site.test 123 456 789</p>"""))
    async with httpx.AsyncClient() as c:
        out = await crawl_one("https://site.test/", c)
    assert {"a@site.test","support@site.test"} <= set(out["emails"])

@respx.mock
@pytest.mark.anyio
async def test_run_full(monkeypatch):
    respx.get("https://serpapi.com/search").mock(return_value=httpx.Response(
        200, json={"organic_results":[{"link":"https://a.pl"},{"link":"https://b.pl"}]}
    ))
    monkeypatch.setattr("src.main.in_robots", lambda u: True)
    respx.get("https://a.pl").mock(return_value=httpx.Response(200, text="<title>A</title>"))
    respx.get("https://b.pl").mock(return_value=httpx.Response(200, text="<title>B</title>"))
    monkeypatch.setenv("SERPAPI_KEY","x")
    out = await run("foo")
    assert {r["title"] for r in out} == {"A","B"}
