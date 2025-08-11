from src.main import parse_info, absolutize

def test_absolutize():
    assert absolutize("https://ex.com/dir/", "../a") == "https://ex.com/a"

def test_parse_info_extracts_contact():
    html = """
    <html><head><title> ACME </title></head>
    <body>
      <a href="/kontakt">Kontakt</a>
      <p>mail: biuro@acme.pl tel: 123-456-789</p>
    </body></html>
    """
    info = parse_info(html, "https://acme.pl/")
    assert info["title"].strip() == "ACME"
    assert "biuro@acme.pl" in info["emails"]
    assert info["contact_url"].endswith("/kontakt")
