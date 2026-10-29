"""Generate a basic data quality profile from the supplied raw CSV files."""
from pathlib import Path
import json
import pandas as pd
from pipeline import ROOT, TRAIN_PATH, TEST_PATH, EXPECTED_COLUMNS


def profile_one(path: Path) -> dict:
    df = pd.read_csv(path, low_memory=False)
    return {
        "file": path.name,
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "column_names": list(df.columns),
        "duplicate_full_rows": int(df.duplicated().sum()),
        "duplicate_vehicle_ids": int(df["vehicle_id"].duplicated().sum()) if "vehicle_id" in df else None,
        "unique_vehicle_ids": int(df["vehicle_id"].nunique(dropna=True)) if "vehicle_id" in df else None,
        "missing_by_column": {str(k): int(v) for k, v in df.isna().sum().items() if int(v) > 0},
        "dtypes": {str(k): str(v) for k, v in df.dtypes.items()},
    }

if __name__ == "__main__":
    report = {"train": profile_one(TRAIN_PATH), "test": profile_one(TEST_PATH)}
    train_ids = set(pd.read_csv(TRAIN_PATH, usecols=["vehicle_id"]).vehicle_id.dropna())
    test_ids = set(pd.read_csv(TEST_PATH, usecols=["vehicle_id"]).vehicle_id.dropna())
    report["cross_file_vehicle_id_overlap"] = int(len(train_ids & test_ids))
    out = ROOT / "docs" / "data_profile.json"
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"train_rows": report['train']['rows'], "test_rows": report['test']['rows'],
                      "cross_file_vehicle_id_overlap": report['cross_file_vehicle_id_overlap'],
                      "output": str(out.relative_to(ROOT))}, indent=2))
