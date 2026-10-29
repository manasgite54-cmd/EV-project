# Electric Vehicle Market Performance & Insights

A college data-analytics project starter that combines **CSV data preparation, SQL analysis, Tableau visualizations/dashboard/story, and Flask web integration**. It is designed around the supplied `ev_market_train.csv` and `ev_market_test.csv` files.

> **Important distinction:** the Flask pages and data pipeline are included as source code. The final Tableau workbook, published Tableau views, and their embed URLs must still be created/verified in Tableau. The local Flask charts are supporting previews only and do not replace the required Tableau worksheets.

## College requirement map

| College requirement | Included deliverable / status |
|---|---|
| Define problem / understand problem | `docs/PROJECT_REPORT.md` — problem statement, objectives, research questions |
| Collect dataset | `data/raw/` contains both uploaded CSV files; add exact Kaggle source/license in `docs/DATA_SOURCE.md` |
| Store data in DB | `src/pipeline.py` loads a combined cleaned table named `ev_vehicles`; SQLite is default; MySQL is configurable |
| Perform SQL operations | `sql/schema.sql`, `sql/analysis_queries.sql` |
| Connect DB with Tableau | `tableau/TABLEAU_BUILD_GUIDE.md` |
| Data preparation | `src/pipeline.py`; creates processed CSV and cleaning report |
| Visualizations | `tableau/TABLEAU_BUILD_GUIDE.md` describes the worksheet plan |
| Dashboard and responsive design | Tableau dashboard plan plus responsive Flask shell in `web/` |
| Story / scenes | `docs/STORYBOARD.md` and `web/templates/story.html` |
| Performance testing | `docs/PERFORMANCE_TEST_PLAN.md`, `tests/` |
| Web integration with Flask | `web/app.py` and templates; configure published Tableau embed URLs in `.env` |
| Demonstration and documentation | `docs/PROJECT_REPORT.md`, `docs/DEMO_SCRIPT.md`, this README |

## Quick start (Windows / VS Code)

### 1. Open the folder

Unzip this project, open `EV-Market-Insights` in VS Code, and open Terminal → New Terminal.

### 2. Create a virtual environment

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks environment activation, use Command Prompt and run:

```bat
.venv\Scripts\activate.bat
```

### 3. Configure settings

Copy `.env.example` to `.env`. Leave `DATABASE_URL` blank for the default local SQLite database. Do not commit `.env` or put passwords in source code.

### 4. Run the data pipeline

From the project root:

```powershell
python -m src.pipeline
```

This reads both raw files, tags each row as train/test, cleans whitespace and data types, removes exact duplicates and repeated `vehicle_id` keys, preserves missing measurements as missing, writes `data/processed/ev_market_clean.csv`, writes `data/processed/cleaning_report.json`, and loads `ev_vehicles` into `db/ev_market.db` by default.

The script is repeatable: re-running it rebuilds the cleaned CSV and `ev_vehicles` table. Do not point it at a database/table containing unrelated data; `if_exists="replace"` replaces that table.

### 5. Start the Flask website

```powershell
python web/app.py
```

Open `http://127.0.0.1:5000`. The `/health` endpoint should return `{"status":"ok", ...}`. The local website shows a preview and explains where Tableau embeds need to be configured.

### 6. Build Tableau content

Follow `tableau/TABLEAU_BUILD_GUIDE.md`. Create and save a Tableau workbook with separate worksheets, filters, a dashboard, and a Tableau Story. Publish it only if allowed by your dataset license/privacy requirements. Add the published dashboard/story embed URLs to `.env` as `TABLEAU_DASHBOARD_URL` and `TABLEAU_STORY_URL`, then restart Flask.

### 7. Run tests

```powershell
python -m pytest -q
```

### 8. Optional: use MySQL

Create a database and restricted user in MySQL, then set a SQLAlchemy URL in `.env`, for example:

```text
DATABASE_URL=mysql+pymysql://ev_user:YOUR_PASSWORD@localhost:3306/ev_market
```

Run the pipeline again. Ensure the MySQL server is running and the account can create/replace the project table. Test the connection before running the full pipeline. The default SQLite setup is simpler for local development; the final database choice should follow your faculty's instructions.

## Data interpretation cautions

- `model_year` is a vehicle model year, not necessarily the year in which a sale occurred.
- `annual_sales_units` is included in source data, but check the Kaggle description before adding these values across records. It may represent model-level values repeated across many records.
- Do not describe generated-looking records as verified industry facts unless the source confirms their origin and methodology.
- Missing values should not be silently converted to zero. Show non-null sample counts where they affect interpretation.
- Correlation between battery size, range, price, or rating does not prove causation.
- `ev_market_test.csv` has the same visible columns as the training file, including analytical fields. In a typical machine-learning task, a test file may have a different role; for this descriptive analytics project, the pipeline includes both files after confirming there is no overlap in vehicle IDs.

## Project structure

```text
EV-Market-Insights/
├── data/raw/                 # Original supplied CSVs (do not edit)
├── data/processed/           # Generated clean CSV and quality report
├── db/                       # Local SQLite database generated at run time
├── docs/                     # Report, source notes, storyboard, tests and demo guide
├── sql/                      # Schema and query library
├── src/                      # Data profiling and cleaning/loading pipeline
├── tableau/                  # Workbook authoring and publishing guide
├── tests/                    # Automated checks
├── web/                      # Flask app, HTML templates and CSS
├── .env.example              # Safe configuration template
└── requirements.txt
```

## Dataset source record

The CSV files are included as provided by the student. The exact Kaggle URL, dataset title, author, license, and any source-specific usage conditions have not been inferred. Complete `docs/DATA_SOURCE.md` with the actual Kaggle information before final submission.
