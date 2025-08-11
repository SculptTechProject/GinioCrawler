# GinioCrawler

![Release](https://img.shields.io/github/v/release/SculptTechProject/GinioCrawler?include_prereleases&label=release)

## DESCRIPTION

Small, pragmatic lead-gen helper: type a query → get company contacts → export to Excel/CSV. Built to help small businesses assemble contact lists without manual copy-paste.

– Uses SerpAPI (Google results)

– Extracts emails and phone numbers from target pages

– Exports to .xlsx and .csv

– If SERPAPI\_KEY is missing, the app will prompt for it on first run

## DEMO

<img width="1177" height="520" alt="image" src="https://github.com/user-attachments/assets/ef1bad28-6b57-4fe2-a276-afb1ba4ebfa1" />


## FEATURES

– Targeted search via SerpAPI (country/language aware)

– Email and phone extraction from result pages

– Clean Excel/CSV export with consistent columns

– Simple GUI flow (and basic CLI)

– Safety knobs: polite delays and rate limits

## ARCHITECTURE (HIGH LEVEL)

**Query → SerpAPI (Google) → result URLs → fetch and parse → extract contacts → dedupe → export (xlsx/csv)**

REQUIREMENTS

– Python 3.9+

– SerpAPI account (free tier works): [CLICK](https://serpapi.com)

*Note: no manual env setup required; the app will ask for the key if it’s missing.*

## **QUICKSTART — GUI**

```bash
#1. 
git clone https://github.com/SculptTechProject/GinioCrawler.git
# 2. 
cd GinioCrawler
# 3. 
pip install -r requirements.txt
# 4. Run your entry script, for example:
python app_gui.py
 # If SERPAPI_KEY is not set, the app will prompt for it and continue.
```

## QUICKSTART — CLI

```bash
#1. 
git clone https://github.com/SculptTechProject/GinioCrawler.git
# 2. 
cd GinioCrawler
# 3. 
pip install -r requirements.txt
# 4. Please make sure you provided SERPAPI_KEY, then:
python main.py
```

## OUTPUT SCHEMA (TYPICAL COLUMNS)

<img width="2035" height="373" alt="image" src="https://github.com/user-attachments/assets/c40467fb-cbc4-4770-9e83-1f998023fa60" />


## GOOD CITIZEN (ETHICS AND LIMITS)

– Respect websites’ robots.txt and Terms of Service

– Keep reasonable rate limits; do not hammer the same domain

– SerpAPI has quotas; heavy usage may require a paid plan

– Use responsibly; this tool is for legitimate contact discovery (no spam)

## TROUBLESHOOTING

– Empty results: make the query more specific; check SerpAPI quota; set proper country/lang

– Slow or blocked: increase delays, lower concurrency, fetch fewer pages

– Excel won’t open: try CSV, or ensure .xlsx is written with a supported library

– Key prompt loops: verify your SerpAPI key and remaining credits

## PACKAGING (DISTRIBUTABLES)

**Windows (.exe):**

```bash
pip install pyinstaller

pyinstaller –onefile –name GinioCrawler app.py

Output: dist/GinioCrawler.exe
```

**macOS (.app / .dmg):**

```bash
pip install pyinstaller

pyinstaller –windowed –name GinioCrawler app.py

hdiutil create -volname GinioCrawler -srcfolder dist/GinioCrawler.app -ov -format UDZO dist/GinioCrawler.dmg
```

*Note: unsigned app; users can open via Right-click → Open. (Signing/notarization can be added later in CI.)*

## TESTS (WHAT TO COVER + QUICK START)

Install and run:

pip install pytest

pytest -q

Recommended coverage:

– search/SerpAPI: correct request, pagination, error handling and rate/limit behavior

– fetch: retries with backoff, timeouts, robots.txt respected

– extract: email/phone patterns (various formats), duplicates handling, URL normalization

– export: column order and names, files openable in Excel and CSV

– CLI/UX: missing SERPAPI\_KEY triggers prompt; flag parsing; happy path without real network calls (mocked)

## ROADMAP (SUGGESTED)

– Saved queries and recent exports

– De-duplication across sessions

– Fallback engines and smarter retry strategy

– Better parsing and validation for contacts

– Dockerfile for one-command runs

## LICENSE

MIT 👀️


