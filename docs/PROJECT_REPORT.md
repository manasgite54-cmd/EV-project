# Project Report: Electric Vehicle Market Performance & Insights

> Report template. Replace all bracketed prompts and placeholder statements after completing the work. Do not submit unverified findings as final results.

## 1. Abstract

This project analyzes the supplied electric-vehicle dataset using data preparation, SQL queries, Tableau visualizations, and a Flask web interface. The workflow combines the provided training and test CSV files after profiling their schemas and vehicle identifiers, applies documented cleaning rules, loads a cleaned table into a SQL database, and develops a Tableau dashboard and Story to communicate descriptive patterns in manufacturer, category, battery, range, price, geography, and customer-rating fields. The published Tableau views are embedded in the Flask site. Final quantitative findings will be added after verification in Tableau and SQL.

## 2. Problem statement

The supplied dataset contains multiple specifications and market-related fields for electric vehicles. Raw tabular data is not an efficient way for a decision-maker to compare categories, manufacturers, battery technologies, driving range, price, and customer ratings. The project aims to turn the dataset into a cleaned and queryable source, build clear visual summaries, and present the findings through an interactive dashboard and a guided data story.

## 3. Objectives

1. Inspect the dataset schema, quality, and provenance.
2. Preserve raw source files and create a repeatable data-cleaning pipeline.
3. Store prepared records in a relational database and perform SQL analysis.
4. Build multiple distinct Tableau worksheets, a dashboard, and a multi-scene Story.
5. Embed the published Tableau views into a responsive Flask website.
6. Test data correctness, filtering, responsiveness, and performance, then document results.

## 4. Research questions

- Which manufacturers and vehicle categories have the most records in this dataset?
- How do recorded sales values differ by manufacturer, region, or model year, assuming definitions support those aggregations?
- How do battery technologies compare on capacity, driving range, cycle life, and degradation?
- What patterns are visible between price, range, efficiency, and customer rating?
- How do records vary by manufacturing country and market region?
- What data-quality limitations should influence a user's interpretation?

## 5. Tools and technologies

- Python and pandas: loading, data profiling, cleaning, and repeatable transformation.
- SQLAlchemy + SQLite by default / MySQL optionally: database loading and database access.
- SQL: summary queries and comparisons.
- Tableau: required worksheets, calculated fields, dashboard, filters, and Story.
- Flask: web interface and Tableau embedding.
- Git/GitHub: source control and sharing the source code.

## 6. Dataset description and provenance

- Training CSV: `data/raw/ev_market_train.csv`.
- Test CSV: `data/raw/ev_market_test.csv`.
- Columns cover identifiers, manufacturer/model, year/country/region/category, battery, range, efficiency, performance, charging, price/cost, safety, environmental estimate, annual-sales value, customer rating, and use case.
- Source/title/author/download date/license: see `DATA_SOURCE.md`; these must be completed from the original Kaggle page.
- Note: the current file names and columns alone do not prove whether the rows are real-world, synthetic, or simulated. State provenance exactly as the dataset publisher describes it.

## 7. Methodology

### 7.1 Profiling

The included profiler reports row and column counts, data types, missing values, exact duplicate rows, duplicate vehicle identifiers, and cross-file ID overlap. Run `python src/profile_dataset.py` to regenerate the profile after a dataset change.

### 7.2 Cleaning

The pipeline keeps raw files unchanged; adds `source_split`; normalizes whitespace and empty text; parses numeric columns; removes exact duplicate rows; keeps the first record for duplicate `vehicle_id`; excludes missing vehicle keys; preserves other missing values; and derives `efficiency_kwh_per_100km = efficiency_wh_per_km / 10`. A JSON cleaning report records the input/output row counts, duplicates, missing cells, and split counts.

### 7.3 Database and SQL

The pipeline writes table `ev_vehicles`. `sql/schema.sql` documents the intended MySQL schema and indexes. `sql/analysis_queries.sql` provides reproducible summary, manufacturer, year, category, battery, geography, scatter-source, data-quality, and outlier-review queries.

### 7.4 Tableau visual analytics

Build the worksheets, filters, dashboard, and Story according to `../tableau/TABLEAU_BUILD_GUIDE.md` and `STORYBOARD.md`. Record the workbook path, screenshots, number of worksheets, calculated fields, and successful filter tests in the final report.

### 7.5 Flask integration

The Flask site provides Overview, Dashboard, Story, and Methodology pages. Published Tableau views are configured with environment variables. Local HTML bar previews are a development aid, not replacements for Tableau deliverables.

## 8. Results (complete only after testing)

- Total valid vehicle records after cleaning: [read cleaning report]
- Distinct manufacturers: [run SQL / verify in Tableau]
- Leading category by record count: [verified result and count]
- Manufacturer comparison finding: [verified metric, filter scope, and count]
- Battery/range finding: [verified pattern and sample size]
- Price/rating finding: [verified pattern and sample size]
- Data quality issue and handling: [verified from cleaning report]

Avoid adding numbers until they have been checked against the database and workbook.

## 9. Performance testing

Complete the results in `PERFORMANCE_TEST_PLAN.md`. Include the machine setup, database engine, row count, workbook version, filters tested, observed load times, and any performance improvements. Do not claim specific performance until measured.

## 10. Limitations

- Data provenance, generation method, and licensing must be verified on Kaggle.
- Model year is not automatically the sales year.
- `annual_sales_units` might not be additive across all records; inspect publisher definitions before summing as market-wide sales.
- Missing numeric fields reduce the effective sample size for averages.
- Relationships between numerical fields are descriptive and do not establish causal effects.
- Tableau publishing may expose the workbook/data publicly; choose the approved publishing location based on license and college policy.

## 11. Conclusion (write after the final Story)

Summarize the strongest three supported findings, the main data limitation, and one next analysis that would improve reliability. Tie each recommendation to evidence from a SQL query or Tableau view.

## 12. References

- Kaggle dataset page: [paste verified source URL]
- Tableau documentation used: [URLs/resources actually consulted]
- Other sources: [list any sources used]
