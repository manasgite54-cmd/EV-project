# Baseline pipeline verification

The packaged code was run against the two CSVs supplied in this conversation in the build environment.

- Training CSV: 200,000 rows, 37 source columns.
- Test CSV: 100,000 rows, 37 source columns.
- Overlap in `vehicle_id` between the two files: 0.
- Exact duplicate rows across the combined input: 1.
- Clean output rows: 299,999.
- Unique `vehicle_id` values in database: 299,999.
- Distinct manufacturer labels in the cleaned data: 200.
- Missing measurement cells retained by the cleaning pipeline: 28,507, including 5,908 missing customer ratings, 3,017 missing annual-sales values, 5,814 missing battery cycle-life values, 9,160 missing 3-year resale values, and 4,608 missing infotainment screen sizes.
- Database used in this verification: local SQLite.

Detailed actual profile: `data_profile.json`. Cleaning report snapshot: `verified_pipeline_run.json`.

This verifies the data pipeline and database row count only. It does **not** mean Tableau workbook authoring, publication, embed configuration, or manual dashboard-performance measurements have been completed. Re-run the pipeline in your environment and compare your results before using this baseline in the report.
