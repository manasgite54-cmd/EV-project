import pandas as pd
from src.pipeline import EXPECTED_COLUMNS, clean_data


def make_row(vehicle_id="EV1", manufacturer=" Test Motors "):
    row = {column: None for column in EXPECTED_COLUMNS}
    row.update({
        "vehicle_id": vehicle_id,
        "model_name": " Model X ",
        "manufacturer": manufacturer,
        "model_year": 2024,
        "manufacturing_country": " India ",
        "market_region": " South Asia ",
        "category": " Sedan ",
        "battery_capacity_kwh": 60.0,
        "battery_type": " LFP ",
        "range_km": 400.0,
        "efficiency_wh_per_km": 150.0,
        "price_usd": 30000.0,
        "annual_sales_units": 1000.0,
        "customer_rating": None,
    })
    return row


def test_cleaning_deduplicates_and_preserves_missing_values():
    raw = pd.DataFrame([
        {**make_row(), "source_split": "train"},
        {**make_row(), "source_split": "train"},  # exact duplicate
        {**make_row("EV2", "Other Motors"), "source_split": "test"},
    ])
    cleaned, report = clean_data(raw)
    assert len(cleaned) == 2
    assert cleaned["vehicle_id"].is_unique
    assert report["removed_exact_duplicate_rows"] == 1
    assert cleaned["customer_rating"].isna().all()
    assert "efficiency_kwh_per_100km" in cleaned.columns
    assert (cleaned["efficiency_kwh_per_100km"] == 15).all()
    assert cleaned.loc[cleaned.vehicle_id == "EV1", "manufacturer"].iloc[0] == "Test Motors"


def test_deduplicates_vehicle_key_even_if_other_fields_differ():
    row1 = {**make_row("EV1", "Maker A"), "source_split": "train"}
    row2 = {**make_row("EV1", "Maker B"), "source_split": "test"}
    cleaned, report = clean_data(pd.DataFrame([row1, row2]))
    assert len(cleaned) == 1
    assert report["removed_duplicate_vehicle_id_rows_after_exact_dedup"] == 1
    assert cleaned.iloc[0]["manufacturer"] == "Maker A"
