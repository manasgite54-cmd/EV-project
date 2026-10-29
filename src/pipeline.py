"""Repeatable EV data preparation and database loading pipeline.

Default: reads the two supplied CSVs, cleans them, writes a processed CSV,
then loads the records into local SQLite. Set DATABASE_URL in .env to use MySQL.
Raw CSV files are never overwritten.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

TRAIN_PATH = ROOT / os.getenv("EV_TRAIN_CSV", "data/raw/ev_market_train.csv")
TEST_PATH = ROOT / os.getenv("EV_TEST_CSV", "data/raw/ev_market_test.csv")
CLEAN_PATH = ROOT / os.getenv("EV_CLEAN_CSV", "data/processed/ev_market_clean.csv")
SQLITE_PATH = ROOT / os.getenv("SQLITE_PATH", "db/ev_market.db")
EXPECTED_COLUMNS = [
    "vehicle_id", "model_name", "manufacturer", "model_year", "manufacturing_country",
    "market_region", "category", "battery_capacity_kwh", "battery_type", "battery_cycle_life",
    "battery_degradation_pct_5yr", "range_km", "efficiency_wh_per_km", "motor_power_kw",
    "torque_nm", "num_motors", "drivetrain", "top_speed_kmph", "acceleration_0_100_sec",
    "max_dc_charging_kw", "charging_dc_fast_time_min", "charging_ac_time_hr",
    "num_charging_ports", "num_seats", "weight_kg", "cargo_capacity_liters", "price_usd",
    "insurance_cost_usd_yearly", "warranty_years", "resale_value_pct_3yr",
    "safety_rating_stars", "autonomous_level", "infotainment_screen_inch",
    "co2_saved_tons_per_year", "annual_sales_units", "customer_rating", "recommended_use_case",
]
NUMERIC_COLUMNS = [
    "model_year", "battery_capacity_kwh", "battery_cycle_life", "battery_degradation_pct_5yr",
    "range_km", "efficiency_wh_per_km", "motor_power_kw", "torque_nm", "num_motors",
    "top_speed_kmph", "acceleration_0_100_sec", "max_dc_charging_kw",
    "charging_dc_fast_time_min", "charging_ac_time_hr", "num_charging_ports", "num_seats",
    "weight_kg", "cargo_capacity_liters", "price_usd", "insurance_cost_usd_yearly",
    "warranty_years", "resale_value_pct_3yr", "safety_rating_stars", "autonomous_level",
    "infotainment_screen_inch", "co2_saved_tons_per_year", "annual_sales_units", "customer_rating",
]
TEXT_COLUMNS = [c for c in EXPECTED_COLUMNS if c not in NUMERIC_COLUMNS]


def load_raw_data(train_path: Path = TRAIN_PATH, test_path: Path = TEST_PATH) -> pd.DataFrame:
    """Read train/test CSVs and tag source split before combining them."""
    frames = []
    for split, path in (("train", train_path), ("test", test_path)):
        if not path.exists():
            raise FileNotFoundError(f"Required dataset not found: {path}\nPut the supplied CSV in data/raw/ or update .env.")
        frame = pd.read_csv(path, low_memory=False)
        missing_cols = sorted(set(EXPECTED_COLUMNS) - set(frame.columns))
        extra_cols = sorted(set(frame.columns) - set(EXPECTED_COLUMNS))
        if missing_cols:
            raise ValueError(f"{path.name} is missing expected columns: {missing_cols}")
        if extra_cols:
            print(f"WARNING: {path.name} has extra columns that will be omitted: {extra_cols}")
        frame = frame[EXPECTED_COLUMNS].copy()
        frame["source_split"] = split
        frames.append(frame)
    return pd.concat(frames, ignore_index=True)


def clean_data(raw: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Apply transparent, conservative cleaning; do not impute real measurements."""
    before_rows = len(raw)
    input_missing = int(raw.isna().sum().sum())
    data = raw.copy()

    # Normalize text without inventing values. Empty strings become missing values.
    for col in TEXT_COLUMNS + ["source_split"]:
        data[col] = data[col].astype("string").str.strip().str.replace(r"\s+", " ", regex=True)
        data[col] = data[col].replace("", pd.NA)

    for col in NUMERIC_COLUMNS:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    # Drop exact duplicates and then duplicate business keys, keeping the first row.
    exact_duplicates = int(data.duplicated().sum())
    data = data.drop_duplicates(keep="first")
    duplicate_vehicle_ids = int(data["vehicle_id"].duplicated(keep="first").sum())
    data = data.drop_duplicates(subset=["vehicle_id"], keep="first")

    # A row without a vehicle key cannot be reliably identified; exclude it from the fact table.
    missing_vehicle_ids = int(data["vehicle_id"].isna().sum())
    data = data[data["vehicle_id"].notna()].copy()

    # Derived field for analysis: Wh/km converted into kWh/100 km.
    data["efficiency_kwh_per_100km"] = data["efficiency_wh_per_km"] / 10.0

    # Stable ordering helps reproducibility. Missing numeric values remain missing.
    data = data.sort_values("vehicle_id", kind="stable").reset_index(drop=True)
    report = {
        "input_rows": before_rows,
        "output_rows": int(len(data)),
        "removed_exact_duplicate_rows": exact_duplicates,
        "removed_duplicate_vehicle_id_rows_after_exact_dedup": duplicate_vehicle_ids,
        "removed_rows_missing_vehicle_id": missing_vehicle_ids,
        "missing_cells_before_cleaning": input_missing,
        "missing_cells_after_cleaning": int(data.isna().sum().sum()),
        "unique_vehicle_ids": int(data["vehicle_id"].nunique(dropna=True)),
        "columns_before_cleaning": int(len(raw.columns)),
        "columns_after_cleaning": int(len(data.columns)),
        "missing_by_column": {k: int(v) for k, v in data.isna().sum().items() if int(v) > 0},
        "source_split_counts": {str(k): int(v) for k, v in data["source_split"].value_counts(dropna=False).items()},
    }
    return data, report


def make_engine() -> Engine:
    """Use DATABASE_URL if configured; otherwise use local SQLite."""
    database_url = os.getenv("DATABASE_URL", "").strip()
    if database_url:
        return create_engine(database_url, pool_pre_ping=True)
    SQLITE_PATH.parent.mkdir(parents=True, exist_ok=True)
    return create_engine(f"sqlite:///{SQLITE_PATH.as_posix()}")


def run_pipeline() -> dict:
    raw = load_raw_data()
    cleaned, report = clean_data(raw)
    CLEAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(CLEAN_PATH, index=False)

    engine = make_engine()
    try:
        # Replace makes the script repeatable. Never run against a table containing unrelated data.
        cleaned.to_sql("ev_vehicles", engine, if_exists="replace", index=False, chunksize=10000, method=None)
        # Enforce the vehicle key and add indexes for typical dashboard/grouping fields.
        # The table is replaced immediately above, so these indexes can be recreated safely.
        index_specs = [
            ("uq_ev_vehicle_id", "vehicle_id", True),
            ("idx_ev_manufacturer", "manufacturer", False),
            ("idx_ev_year", "model_year", False),
            ("idx_ev_category", "category", False),
            ("idx_ev_battery_type", "battery_type", False),
            ("idx_ev_region", "market_region", False),
        ]
        with engine.begin() as conn:
            for index_name, column_name, is_unique in index_specs:
                unique_sql = "UNIQUE " if is_unique else ""
                if engine.dialect.name == "sqlite":
                    conn.execute(text(f"CREATE {unique_sql}INDEX IF NOT EXISTS {index_name} ON ev_vehicles ({column_name})"))
                else:
                    conn.execute(text(f"CREATE {unique_sql}INDEX {index_name} ON ev_vehicles ({column_name})"))
        with engine.connect() as conn:
            db_count = conn.execute(text("SELECT COUNT(*) FROM ev_vehicles")).scalar_one()
            unique_count = conn.execute(text("SELECT COUNT(DISTINCT vehicle_id) FROM ev_vehicles")).scalar_one()
        if int(db_count) != int(unique_count):
            raise RuntimeError(f"Database key validation failed: {db_count} rows but {unique_count} unique vehicle IDs.")
        report["database_rows_loaded"] = int(db_count)
        report["database_type"] = engine.dialect.name
    finally:
        engine.dispose()

    report_path = CLEAN_PATH.with_name("cleaning_report.json")
    report_path.write_text(__import__("json").dumps(report, indent=2), encoding="utf-8")
    print("\nPIPELINE COMPLETE")
    print(f"Clean CSV: {CLEAN_PATH.relative_to(ROOT)}")
    print(f"Rows loaded to ev_vehicles: {report['database_rows_loaded']:,}")
    print(f"Database: {report['database_type']}")
    print(f"Cleaning report: {report_path.relative_to(ROOT)}")
    print("Note: null measurements were retained as NULL/blank; they were not replaced with zero.")
    return report


if __name__ == "__main__":
    run_pipeline()
