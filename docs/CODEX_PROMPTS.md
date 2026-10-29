# Copy-ready Codex prompts

Use these prompts inside Codex with the project folder open. Ask it to inspect before changing files and to stop after the requested phase. Do not ask it to fabricate Tableau workbook results or report tests it did not run.

## Prompt 0 — inspect and plan

```text
Inspect this EV-Market-Insights repository before modifying anything. Read START_HERE.md, README.md, the pipeline, SQL scripts, Tableau guide, and college checklist. Verify the current files and existing tests. Map every college requirement to a concrete artifact. Identify any mismatch, missing information, environment limitations, or risks. Do not overwrite raw CSVs, do not put secrets in source control, and do not claim a Tableau workbook was created unless it exists and has been checked in Tableau. Give me a beginner-friendly next-step plan and wait for approval.
```

## Prompt 1 — verify dataset and pipeline

```text
Implement/verify only the dataset pipeline phase. Check both data/raw CSVs, preserve them unchanged, run the profiler and pipeline, inspect data/processed/cleaning_report.json, and query the actual database row count plus distinct vehicle_id count. Confirm handling of missing values and duplicates. Run the automated tests. Fix only evidence-backed bugs, rerun the tests, and explain each changed file and command. Don't invent dataset provenance; leave source/license fields marked for me to fill from Kaggle.
```

## Prompt 2 — SQL and database

```text
Review sql/schema.sql, sql/analysis_queries.sql, and src/pipeline.py against the college requirements. Confirm the table/indexes exist in the configured database, run appropriate queries, and compare their results to the cleaned data. Explain SQL GROUP BY, COUNT, AVG, SUM, and NULL handling. Check whether annual_sales_units is additive before using it as a market-wide total. Do not create fake results. Make a small, testable change only if required and rerun checks.
```

## Prompt 3 — Tableau workbook planning

```text
Help me author the actual required Tableau workbook, step by step, using the connected ev_vehicles data. Follow tableau/TABLEAU_BUILD_GUIDE.md. Explain every worksheet's Rows, Columns, Marks, filters, aggregation, and title. Build at least eight distinct visualizations, a dashboard with useful filters and at least one filter action, and the multi-scene Story. Do not substitute Flask/Python charts for Tableau. If you cannot operate Tableau directly in this environment, give me exact click-by-click instructions and a list of screenshots/evidence to capture.
```

## Prompt 4 — Flask integration

```text
Inspect the existing Flask app before making changes. Verify that Overview, Dashboard, Story, and Methodology routes render; /health responds; /api/summary returns expected values from the cleaned data; and published Tableau dashboard/story URLs are read from .env. Improve only specific issues, keep design responsive and accessible, never hard-code secrets, and rerun tests. The Tableau views must remain embedded Tableau content, not be replaced by charts generated in Flask.
```

## Prompt 5 — performance testing

```text
Complete the test plan in docs/PERFORMANCE_TEST_PLAN.md with tests you can actually run. Verify record counts, unique IDs, null values, calculation examples, filters where testable, Flask endpoints, and responsive layout. For Tableau interactions that require the Tableau desktop/browser, mark them as manual and give me exact steps instead of claiming success. Record the machine/software context and measured times; never fabricate timings. Update the checklist only for items supported by evidence.
```

## Prompt 6 — final submission review

```text
Perform a final audit against docs/COLLEGE_CHECKLIST.md and the original requirements. Verify README instructions from a clean environment if possible, test the app and pipeline, search for secrets and generated files that should not be committed, confirm dataset license/source attribution, check the published Tableau embed URLs, and list incomplete deliverables. Update documentation to distinguish completed and pending items. Do not mark the whole project complete if workbook publishing or manual performance tests are still pending.
```
