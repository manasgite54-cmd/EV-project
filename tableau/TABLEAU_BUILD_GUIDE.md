# Tableau workbook build guide

This guide maps the project requirements to a workbook you create in Tableau Desktop or Tableau Public. The ZIP does not contain a completed `.twb`/`.twbx` workbook because that workbook must be authored and verified in Tableau itself.

## A. Connect Tableau to the database

Recommended academic path: use MySQL 8+ if faculty specifically expects a relational database; the pipeline also supports local SQLite. Tableau connector availability and drivers vary by Tableau edition/version. If SQLite is not available as a native connector, use MySQL or export the cleaned CSV as a Tableau input extract.

1. Run `python -m src.pipeline` and verify `database_rows_loaded` in `data/processed/cleaning_report.json`.
2. In Tableau, choose the database connector supported by your installed edition (MySQL is a common choice). Enter the server, port, database, username, and password locally; never place credentials into screenshots, this repository, or the published workbook.
3. Select the `ev_vehicles` table and inspect the data preview. Check that `model_year` is a dimension/date-like numeric field as appropriate, IDs and names are dimensions, and measures use correct numeric aggregation.
4. If the chosen database has no supported Tableau connector, use the generated `data/processed/ev_market_clean.csv` as a documented fallback for visualization, but retain the SQL database and SQL query deliverables to satisfy the database requirement.
5. Save the workbook as `tableau/EV_Market_Insights.twbx` (packaged workbook preferred for portability if source licensing allows it). Do not add a password to any project file.

## B. Define calculated fields

Create these in Tableau or reproduce them in SQL/Python. Confirm that the name does not already exist before creating.

| Calculated field | Tableau formula | Purpose / note |
|---|---|---|
| `Vehicle Record Count` | `COUNT([vehicle_id])` | Number of records with a vehicle ID; unique IDs are expected after pipeline cleaning. |
| `Average Range (km)` | `AVG([range_km])` | Average non-null range. |
| `Average Battery Capacity (kWh)` | `AVG([battery_capacity_kwh])` | Average non-null capacity. |
| `Average Customer Rating` | `AVG([customer_rating])` | Interpret with visible sample size. |
| `Efficiency (kWh/100 km)` | `[efficiency_wh_per_km] / 10` | Unit conversion from Wh/km. |
| `Price per km of range` | `IF [range_km] > 0 THEN [price_usd] / [range_km] END` | Descriptive ratio, not a complete affordability measure. |
| `Non-null Rating Count` | `COUNT([customer_rating])` | Use alongside average rating to expose sample coverage. |

Avoid sales market-share calculations until data semantics are confirmed. If faculty expects a market share metric, document the denominator and ensure values are comparable and additive.

## C. Required worksheets / distinct visualizations

Create at least these eight worksheets. The assignment does not state a precise minimum number; eight provides a reasonable varied set. Use a clear title, unit labels, useful tooltips, sensible sort order, and appropriate formats.

1. **KPI — Market Summary:** number of vehicle records, distinct manufacturers, average range, average battery capacity, average rating. Use actual aggregate values.
2. **Recorded Sales by Manufacturer:** horizontal bars by `manufacturer`, using `SUM(annual_sales_units)` only after validating source semantics. Otherwise use vehicle-record count and label it clearly.
3. **Records by Model Year:** bars by `model_year`; title must say model year, not sales year.
4. **Vehicle Category Comparison:** bars by `category` with record count; optionally show average range in tooltip.
5. **Battery Technology Mix:** bars or treemap by `battery_type` and record count. A donut/pie is optional, but label counts/percentages clearly.
6. **Battery Capacity vs Range:** scatter plot with `battery_capacity_kwh` on X and `range_km` on Y; color by battery type; detail by model or ID. Do not infer causality.
7. **Price vs Range:** scatter plot with `price_usd` on X and `range_km` on Y; color or shape by category; use tooltip for manufacturer, model, rating. Consider logarithmic axes only if justified.
8. **Customer Rating by Category or Manufacturer:** bars of average rating with count of non-null ratings in tooltip; do not rank groups with extremely small samples without a warning.
9. **Manufacturing Country / Market Region:** a bar chart or map if geographic fields map reliably to Tableau's geographic roles. Use a bar chart if a map is ambiguous.
10. **Efficiency / Battery Degradation:** compare efficiency and degradation by battery type if appropriate fields are populated. Show missingness/sample counts.

## D. Dashboard layout and interactions

Create a dashboard named `EV Market Overview` (use a consistent desktop layout and test a narrower viewport if your Tableau edition supports it).

Suggested layout:
- Header: dashboard title, data source note, and selected date/year range.
- Top: 4–5 KPI tiles.
- Middle: sales/manufacturer comparison and category distribution.
- Bottom: battery capacity vs range, price vs range, rating comparison.
- Filter rail or top filter row: `model_year`, `manufacturer`, `category`, `battery_type`, `market_region`.
- Add a clear **Reset Filters** instruction or dashboard navigation if available.
- Use “Apply to Worksheets → All Using This Data Source” only where shared filters are desired.
- Configure at least one “Use as Filter” chart or dashboard filter action and test that it does not leave unrelated charts blank unexpectedly.
- Use consistent colors, no 3D charts, limited gridlines, readable fonts, and labels on important values.

### Responsive design

Test the dashboard at a wide laptop size and a narrower window; inspect clipping, scrollbars, overlapping legends, axis labels, filter placement, and tooltip readability. Use automatic or device-specific layouts supported by your Tableau edition. Record screenshot evidence in `docs/evidence/` (create the folder when needed).

## E. Create the Tableau Story

Create a Tableau Story called `EV Market Findings` and use the six scenes in `docs/STORYBOARD.md`. Each scene should have:
- a descriptive title written as a question or takeaway;
- one or more relevant sheets/dashboard views;
- 1–3 sentences describing the evidence, with the metric/sample size;
- an interpretation that does not overclaim;
- a transition to the next question.

Use actual results from the workbook. Do not copy placeholder recommendations into the final story without validating them against the data.

## F. Publish and embed in Flask

1. Publish to Tableau Public only if the dataset license allows public redistribution and the data has no confidential information; otherwise use your institution's approved Tableau Server/Cloud workspace.
2. Open the published dashboard/story and locate the Share/Embed option. Copy the URL accepted by Tableau's embed interface (do not invent a URL or paste an edit URL).
3. In `.env`, set:

```text
TABLEAU_DASHBOARD_URL=PASTE_DASHBOARD_EMBED_URL_HERE
TABLEAU_STORY_URL=PASTE_STORY_EMBED_URL_HERE
```

4. Restart Flask with `python web/app.py`, open `/dashboard` and `/story`, and confirm the views load without login errors. Published views may be blocked by organization policy or browser restrictions; follow faculty policy if so.
5. Keep the actual URLs in `.env` if they are private; if public, add them to the README only if your instructor requests it.

## G. Performance and validation checks

- Compare Tableau total record count with SQL `COUNT(*)`.
- Check each filter against a known SQL query.
- Check nulls and denominators behind all averages and percentages.
- Record initial load time and interaction response for representative filter changes.
- Test dashboard after changing one filter and multiple filters together.
- Record row count, columns, calculated-field count, worksheet count, and any optimizations tried.
- Prefer source filters, extracts, aggregation, or fewer marks when the workbook renders slowly; record actual measured values rather than guessing.
