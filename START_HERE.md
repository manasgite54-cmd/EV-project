# Start here — EV Market Insights

This ZIP already contains the two CSV files you uploaded, plus the code and documentation scaffolding. Follow these steps in order; don't jump straight to building the website.

## What is already prepared

- Both original source CSVs are in `data/raw/`.
- A Python cleaning/loading pipeline is in `src/pipeline.py`.
- SQL schema and example analysis queries are in `sql/`.
- Flask website source is in `web/`.
- Tableau worksheet/dashboard/story instructions are in `tableau/TABLEAU_BUILD_GUIDE.md` and `docs/STORYBOARD.md`.
- The full requirement checklist is `docs/COLLEGE_CHECKLIST.md`.

## Step 1 — Unzip and open in VS Code

Extract the ZIP. Open the extracted `EV-Market-Insights` folder in VS Code. In Terminal → New Terminal, check that the terminal's current folder is this project root (the folder containing `README.md`).

## Step 2 — Create Python environment

Run these commands in PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If activation is blocked by PowerShell policy, use Command Prompt and run `.venv\Scripts\activate.bat` instead. Installing dependencies requires access to the package index; if college Wi-Fi blocks it, use an approved connection or ask your lab admin.

## Step 3 — Process the uploaded dataset

```powershell
python -m src.pipeline
```

Expected baseline after successful run: 300,000 source rows total, one exact duplicate row removed, 299,999 rows in the processed output and SQL table, and 299,999 unique vehicle IDs. If the output differs, inspect the report before proceeding.

## Step 4 — Choose the database for Tableau

For the simplest first run, leave `DATABASE_URL` empty. The pipeline uses local SQLite and creates `db/ev_market.db`. For the final required live DB-to-Tableau connection, confirm your installed Tableau edition and supported database connector. If your Tableau setup does not connect to SQLite, install/configure MySQL 8+, set `DATABASE_URL` in `.env`, and rerun the pipeline. Do not commit `.env` or credentials.

## Step 5 — Build Tableau (manual task)

Open Tableau, connect it to `ev_vehicles` through the connector available in your edition, then follow the build guide. If faculty only allows CSV connections or the edition has no SQLite connector, use the processed CSV as the visualization source while retaining the SQL database and queries, and disclose the fallback to your mentor. Create the workbook, worksheets, dashboard, and Story in Tableau itself.

## Step 6 — Run Flask and connect Tableau views

```powershell
python web/app.py
```

Open `http://127.0.0.1:5000`. After publishing the Tableau views in an approved location, copy each real embed URL into `.env` using `TABLEAU_DASHBOARD_URL` and `TABLEAU_STORY_URL`, restart Flask, and test `/dashboard` and `/story`.

## Step 7 — Validate before portal submission

```powershell
python -m pytest -q
```

Complete `docs/COLLEGE_CHECKLIST.md`, `docs/DATA_SOURCE.md`, and the measured result columns in `docs/PERFORMANCE_TEST_PLAN.md`. The portal's Demo link and GitHub link should point to actual accessible resources.

## Prompt for Codex

Open `docs/CODEX_PROMPTS.md`, copy the initial prompt into Codex, and let it inspect the folder before asking it to change code. Ask it to work phase by phase, run tests, explain commands, and report anything that requires manual work in Tableau.
