# Performance testing plan and results log

Fill the observed-result column after running the test. Do not guess timings or claim unperformed tests.

| ID | Requirement | Procedure | Expected result | Observed result |
|---|---|---|---|---|
| P01 | Data volume rendered to DB | Run pipeline; compare output rows to `SELECT COUNT(*) FROM ev_vehicles` and `cleaning_report.json`. | Counts match exactly. | [fill in] |
| P02 | Unique keys | Run `SELECT COUNT(*), COUNT(DISTINCT vehicle_id) FROM ev_vehicles`. | Both counts match after deduplication. | [fill in] |
| P03 | Missing values | Run data-quality queries; inspect null counts in Tableau. | Nulls are visible/documented, not silently set to zero. | [fill in] |
| P04 | Tableau filters | Change each filter individually and in combination; compare with SQL subset. | Charts update consistently and no unrelated sheet behaves unexpectedly. | [fill in] |
| P05 | Calculated fields | Manually calculate a few example records and compare with Tableau. | Calculations match units/rounding. | [fill in] |
| P06 | Number of visualizations | Count finished worksheets in workbook. | [enter count; target >= 8 distinct worksheets in guide]. | [fill in] |
| P07 | Dashboard render time | Measure at least 3 cold and 3 warm loads on same machine/network. | Record median and environment, no invented target. | [fill in] |
| P08 | Filter response time | Time representative filter actions, repeat each at least 3 times. | Record median and filter combination. | [fill in] |
| P09 | Data volume scaling | If safe, compare a subset/extract and the full dataset workbook. | Report result and trade-off. | [fill in] |
| P10 | Web responsiveness | Inspect Flask pages at wide desktop and mobile/narrow viewport sizes. | No horizontal overflow, text is readable, nav works. | [fill in] |
| P11 | Tableau embed | Open `/dashboard` and `/story` after setting URLs. | Views load or a documented policy/login issue is reported. | [fill in] |
| P12 | Flask health | Visit `/health` and `/api/summary`. | HTTP 200 and valid JSON. | [fill in] |

## Test environment

- Computer/CPU/RAM: [fill in]
- OS: [fill in]
- Python version: [fill in]
- Database engine/version: [fill in]
- Tableau edition/version: [fill in]
- Total rows loaded: [fill in]
- Workbook size / extract mode: [fill in]

## Optimization log

For each optimization, record the problem, change, before measurement, after measurement, and trade-off. Possible options include using an extract, limiting marks, reducing unnecessary detail, using indexes for query workloads, removing redundant quick filters, and simplifying heavy calculated fields.
