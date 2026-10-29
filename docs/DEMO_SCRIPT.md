# Project demonstration script (5–7 minutes)

## 1. Problem and objective (30–45 seconds)

"Our project, Electric Vehicle Market Performance & Insights, turns the supplied EV dataset into a reproducible analytics workflow using Python, SQL, Tableau, and Flask. We explore vehicle segments, manufacturer data, battery specifications, driving range, price, and customer ratings, while documenting source limitations."

## 2. Dataset and preparation (60 seconds)

Show the two source files and explain the original files are preserved. Run through the data dictionary and cleaning report. Explain duplicate handling, missing-value policy, source-split tagging, and the efficiency unit conversion. Mention the verified dataset source and license only after completing `DATA_SOURCE.md`.

## 3. SQL (60 seconds)

Show `sql/analysis_queries.sql` and execute a table count plus one grouped query. Explain `COUNT`, `AVG`, `SUM`, and `GROUP BY`. If you show summed annual sales, explain how the data source supports the aggregation.

## 4. Tableau (2 minutes)

Show the worksheets, one KPI, manufacturer/category comparisons, battery-range scatter plot, filters, and dashboard. Demonstrate at least one filter and verify how it changes multiple views. Navigate to the Tableau Story and explain each scene using actual results.

## 5. Flask integration (45–60 seconds)

Open the local Flask site. Show the Overview, Tableau Dashboard, Story, and Methodology pages. Explain that published Tableau URLs are configured via environment variables rather than hard-coded credentials.

## 6. Performance and conclusion (45 seconds)

Show the performance test log, report one observed load/filter measurement, and state one limitation and one data-backed finding. Be transparent about any tests that remain incomplete.

## Likely viva questions

- Why use SQL if Python can read CSVs? SQL provides a queryable relational data layer and reproducible aggregation; the requirement explicitly asks for database operations.
- Why Tableau? It is the required visualization tool and supports interactive dashboards and Stories.
- Why Flask? It provides a web UI and embeds published Tableau content.
- Why preserve nulls? A missing measurement is not zero; replacing it can bias averages and charts.
- Why check the annual-sales field? Repeated model-level sales values may double-count when summed; the source data dictionary must support the metric.
- How was performance tested? Show the actual test log and environment instead of guessing.
