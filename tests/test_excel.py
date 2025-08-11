from pathlib import Path
import pandas as pd
from src.app_gui import save_results
from src.main import write_excel as real_write_excel

def test_save_results_creates_files(tmp_path, monkeypatch):
    root_out = tmp_path / "wyniki"
    data = [{"url":"https://x","title":"X","emails":["a@x"],"phones":["123"],"contact_url":None}]

    called = {}
    def fake_write(csv_path, xlsx_path):
        called["csv"] = csv_path; called["xlsx"] = xlsx_path
        return real_write_excel(csv_path, xlsx_path)

    monkeypatch.setattr("src.app_gui.write_excel", fake_write)

    csv_p, xlsx_p = save_results(data, "20250101_000000", root_out)
    assert Path(csv_p).exists() and Path(xlsx_p).exists()
    df = pd.read_excel(xlsx_p)
    assert {"url","title","emails","phones","contact_url"}.issubset(df.columns)
    assert called["csv"] == str(csv_p) and called["xlsx"] == str(xlsx_p)
