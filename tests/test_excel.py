from pathlib import Path

import pandas as pd

from main import save_results


def test_save_results_creates_files(tmp_path, monkeypatch):
    root_out = tmp_path / "wyniki"
    data = [
        {
            "url": "https://x",
            "title": "X",
            "emails": ["a@x"],
            "phones": ["123"],
            "contact_url": None,
        }
    ]
    from main import write_excel as real_write_excel

    xlsx_called = {}

    def fake_write(csv, xlsx):
        xlsx_called["csv"] = csv
        xlsx_called["xlsx"] = xlsx
        return real_write_excel(csv, xlsx)

    monkeypatch.setattr("ginio.write_excel", fake_write)
    csv_p, xlsx_p = save_results(data, "20250101_000000", root_out)
    assert Path(csv_p).exists() and Path(xlsx_p).exists()
    df = pd.read_excel(xlsx_p)
    assert set(df.columns) >= {"url", "title", "emails", "phones", "contact_url"}
