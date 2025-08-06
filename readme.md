# GinioCrawler — dokumentacja

## O co chodzi?

Mała apka do wyszukiwania firm po frazie (np. *“producenci granulatu Polska”*), pobierania stron i wyciągania kontaktów (emaile, telefony). Zapisuje wyniki do **CSV** i **XLSX**.

## Wymagania

* Python 3.10+ (dev) / Windows 10+ (EXE)
* Klucz do wyszukiwarki: **SERPAPI\_KEY** (SerpAPI)
* Internet 😅

## Instalacja (dev)

```bash
python -m venv .venv
# Win PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
# jeśli używasz GUI i zapisu klucza:
pip install python-dotenv pandas openpyxl
```

## Konfiguracja klucza SERPAPI

Masz dwie drogi:

1. **Zmienna środowiskowa**
   Windows (PowerShell):

   ```powershell
   setx SERPAPI_KEY "TWÓJ_KLUCZ"
   ```

   Potem zrestartuj terminal/aplikację.
2. **GUI zapisze klucz samo** (jeśli masz `ensure_api_key()`):
   Przy pierwszym uruchomieniu **app\_gui.py** / EXE wyskoczy okno → wklejasz klucz → zapisze się do
   `%APPDATA%\GinioCrawler\.env`.

## Uruchomienie — konsola (CLI)

```bash
python main.py
# wpisz frazę, np. "SoftwareHouse Warszawa"
```

Wyniki lecą do:

* `wyniki/csv/wyniki_YYYYMMDD_HHMMSS.csv`
* `wyniki/excel/wyniki_YYYYMMDD_HHMMSS.xlsx`

Kolumny: `url, title, emails, phones, contact_url`.
W `emails` i `phones` wartości są rozdzielone **spacją**.

## Uruchomienie — GUI

```bash
python app_gui.py
```

* Wpisz frazę.
* (Opcjonalnie) kliknij **Wybierz…** i wskaż folder wyjściowy (w środku stworzy `csv/` i `excel/`).
* Kliknij **Start**. Po zakończeniu otworzy folder z Excellem.

## Budowanie EXE (Windows)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "GinioCrawler" app_gui.py
# opcjonalnie: --icon icon.ico
```

Plik znajdziesz w `dist/GinioCrawler.exe`. Zrób skrót na pulpit.

## Jak to działa (skrót techniczny)

* **SerpAPI** zwraca listę URL-i dla frazy.
* **httpx + BeautifulSoup** pobiera stronę, szuka maili/telefonów i linku **Kontakt** (głębia 1).
* Szanuje `robots.txt`.
* Zapis: **CSV (UTF-8-SIG)** + **XLSX** (auto-szerokości, nagłówki, hiperlinki).
* Separator wielu maili/telefonów: **spacja**.

## Częste problemy

* **„Brak SERPAPI\_KEY”** – ustaw zmienną środowiskową albo użyj GUI z zapisem do `.env`.
* **„ModuleNotFoundError: pandas/openpyxl”** – `pip install pandas openpyxl`.
* **Puste wyniki** – fraza zbyt ogólna / strony blokują boty / brak kontaktu na [www](http://www/).
* **Excel zlepia numery** – w XLSX kolumna „phones” jest tekstem; jeśli nie, włącz format „Tekst”.

## Dobre praktyki / etyka

* Szanuj **`robots.txt`** i limity serwisów.
* Nie bombarduj równoległymi żądaniami (możesz dodać `httpx.Limits` i `asyncio.Semaphore`).
* Sprawdzaj regulaminy serwisów; używaj oficjalnych API wyszukiwarek.
