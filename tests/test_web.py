import pandas as pd
import pytest
pytest.importorskip("flask", reason="Install requirements.txt to run Flask tests")
from web.app import app


def sample_frame():
    return pd.DataFrame({
        "vehicle_id": ["EV1", "EV2", "EV3"],
        "manufacturer": ["Maker A", "Maker B", "Maker A"],
        "model_year": [2022, 2023, 2024],
        "range_km": [300.0, 400.0, 350.0],
        "customer_rating": [4.2, None, 4.6],
        "battery_type": ["LFP", "NMC", "LFP"],
        "category": ["Sedan", "SUV", "Sedan"],
        "annual_sales_units": [100, 200, 150],
    })


def test_health_endpoint():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_pages_render(monkeypatch):
    from web import app as module
    monkeypatch.setattr(module, "load_frame", lambda: (sample_frame(), True))
    client = module.app.test_client()
    for path in ["/", "/dashboard", "/story", "/methodology"]:
        response = client.get(path)
        assert response.status_code == 200, path
    summary = client.get("/api/summary").get_json()
    assert summary["row_count"] == 3
    assert summary["manufacturer_count"] == 2
