import os, csv, asyncio, threading, subprocess, sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv, set_key

from src.main import run, write_excel


def ensure_api_key():
    # 1) jeśli już jest w env, użyj
    if os.environ.get("SERPAPI_KEY"):
        return os.environ["SERPAPI_KEY"]

    # 2) spróbuj wczytać z pliku .env w %APPDATA%\GinioCrawler\.env
    cfg_dir = Path(os.getenv("APPDATA") or (Path.home() / ".config")) / "GinioCrawler"
    cfg_dir.mkdir(parents=True, exist_ok=True)
    env_path = cfg_dir / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=False)
        if os.environ.get("SERPAPI_KEY"):
            return os.environ["SERPAPI_KEY"]

    # 3) poproś użytkownika
    key = simpledialog.askstring("SERPAPI", "Wklej swój SERPAPI_KEY:", show="*")
    if not key:
        raise RuntimeError("Brak SERPAPI_KEY.")
    # zapisz i ustaw w env
    set_key(str(env_path), "SERPAPI_KEY", key)
    os.environ["SERPAPI_KEY"] = key
    return key


def open_folder(path: Path):
    try:
        if sys.platform.startswith("win"):
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.run(["open", str(path)])
        else:
            subprocess.run(["xdg-open", str(path)])
    except Exception:
        pass


def save_results(data, ts, root_out: Path):
    csv_dir = root_out / "csv"
    xlsx_dir = root_out / "excel"
    csv_dir.mkdir(parents=True, exist_ok=True)
    xlsx_dir.mkdir(parents=True, exist_ok=True)

    csv_path = csv_dir / f"wyniki_{ts}.csv"
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(
            f, fieldnames=["url", "title", "emails", "phones", "contact_url"]
        )
        w.writeheader()
        for row in data:
            w.writerow(
                {
                    "url": row.get("url", ""),
                    "title": row.get("title", ""),
                    "emails": " ".join(row.get("emails", [])),  # separator = spacja
                    "phones": " ".join(row.get("phones", [])),
                    "contact_url": row.get("contact_url", ""),
                }
            )

    xlsx_path = xlsx_dir / f"wyniki_{ts}.xlsx"
    write_excel(str(csv_path), str(xlsx_path))
    return csv_path, xlsx_path


def start():
    q = entry_query.get().strip()
    if not q:
        messagebox.showwarning("Uwaga", "Wpisz frazę.")
        return
    try:
        ensure_api_key()
    except Exception as e:
        messagebox.showerror("Błąd", str(e))
        return

    out_root = Path(out_dir_var.get().strip() or "wyniki")
    btn_start.config(state="disabled")
    prog.start(10)
    status.set("Szukam…")

    def worker():
        try:
            data = asyncio.run(run(q))
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            if not data:
                root.after(
                    0,
                    lambda: (
                        prog.stop(),
                        btn_start.config(state="normal"),
                        status.set("Brak wyników."),
                    ),
                )
                return
            csv_path, xlsx_path = save_results(data, ts, out_root)
            root.after(0, lambda: done(csv_path, xlsx_path, len(data), out_root))
        except Exception as e:
            root.after(
                0,
                lambda: (
                    prog.stop(),
                    btn_start.config(state="normal"),
                    messagebox.showerror("Błąd", str(e)),
                ),
            )

    threading.Thread(target=worker, daemon=True).start()


def done(csv_path, xlsx_path, n, out_root):
    prog.stop()
    btn_start.config(state="normal")
    status.set(f"OK — zapisano {n} rekordów.")
    try:
        open_folder(out_root / "excel")
    except:
        pass
    messagebox.showinfo("Gotowe", f"CSV:  {csv_path}\nXLSX: {xlsx_path}")


def choose_dir():
    path = filedialog.askdirectory(title="Wybierz folder wyjściowy")
    if path:
        out_dir_var.set(path)


# --- UI ---
def build_ui():
    global root, entry_query, btn_start, prog, status, out_dir_var
    root = tk.Tk()
    root.title("GinioCrawler")
    root.geometry("560x220")
    tk.Label(root, text="Fraza do wyszukania:").pack(anchor="w", padx=12, pady=(12, 0))
    entry_query = tk.Entry(root); entry_query.pack(fill="x", padx=12, pady=6); entry_query.focus()
    frm = tk.Frame(root); frm.pack(fill="x", padx=12, pady=(0, 6))
    tk.Label(frm, text="Folder wyjściowy:").pack(side="left")
    out_dir_var = tk.StringVar(value=str((Path.cwd() / "wyniki")))
    entry_dir = tk.Entry(frm, textvariable=out_dir_var); entry_dir.pack(side="left", fill="x", expand=True, padx=(8, 6))
    tk.Button(frm, text="Wybierz…", command=choose_dir).pack(side="left")
    btn_start = tk.Button(root, text="Start", command=start); btn_start.pack(padx=12, pady=6)
    prog = ttk.Progressbar(root, mode="indeterminate"); prog.pack(fill="x", padx=12, pady=(4, 8))
    status = tk.StringVar(value="Gotowy"); tk.Label(root, textvariable=status, anchor="w").pack(fill="x", padx=12, pady=(0, 8))
    return root

if __name__ == "__main__":
    build_ui()
    root.mainloop()
