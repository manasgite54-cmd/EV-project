"""Flask web interface for EV Market Insights.

This application is the web integration layer. Tableau remains the required
source for the final Tableau dashboard and story. The local charts below are
supporting previews, not a replacement for the Tableau workbook.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env")

app = Flask(__name__, template_folder="templates", static_folder="static")
CLEAN_PATH = ROOT / os.getenv("EV_CLEAN_CSV", "data/processed/ev_market_clean.csv")
TRAIN_PATH = ROOT / os.getenv("EV_TRAIN_CSV", "data/raw/ev_market_train.csv")
TABLEAU_DASHBOARD_URL = os.getenv("TABLEAU_DASHBOARD_URL", "").strip()
TABLEAU_STORY_URL = os.getenv("TABLEAU_STORY_URL", "").strip()


def load_frame() -> tuple[pd.DataFrame, bool]:
    """Prefer cleaned combined data; fall back to train data with a clear status flag."""
    if CLEAN_PATH.exists():
        return pd.read_csv(CLEAN_PATH, low_memory=False), True
    if TRAIN_PATH.exists():
        return pd.read_csv(TRAIN_PATH, low_memory=False), False
    return pd.DataFrame(), False


def summarize() -> dict:
    df, cleaned_ready = load_frame()
    if df.empty:
        return {"data_ready": False, "row_count": 0, "manufacturer_count": 0,
                "avg_range": None, "avg_rating": None, "top_manufacturers": [],
                "battery_counts": [], "category_counts": [], "available_columns": []}

    def safe_mean(column: str):
        return round(float(df[column].dropna().mean()), 1) if column in df and df[column].notna().any() else None

    top = []
    if "manufacturer" in df:
        metric = "annual_sales_units" if "annual_sales_units" in df else "vehicle_id"
        grouped = df.groupby("manufacturer", dropna=True)[metric].sum(min_count=1) if metric == "annual_sales_units" else df.groupby("manufacturer").size()
        top = [{"label": str(name), "value": round(float(value), 0)} for name, value in grouped.sort_values(ascending=False).head(8).items()]

    battery_counts = []
    if "battery_type" in df:
        battery_counts = [{"label": str(k), "value": int(v)} for k, v in df["battery_type"].fillna("Unknown").value_counts().head(8).items()]

    category_counts = []
    if "category" in df:
        category_counts = [{"label": str(k), "value": int(v)} for k, v in df["category"].fillna("Unknown").value_counts().head(10).items()]

    return {
        "data_ready": bool(cleaned_ready),
        "row_count": int(len(df)),
        "manufacturer_count": int(df["manufacturer"].nunique(dropna=True)) if "manufacturer" in df else 0,
        "avg_range": safe_mean("range_km"),
        "avg_rating": safe_mean("customer_rating"),
        "top_manufacturers": top,
        "battery_counts": battery_counts,
        "category_counts": category_counts,
        "available_columns": list(df.columns),
    }


@app.route("/")
def home():
    stats = summarize()
    return render_template("index.html", stats=stats, active="overview")


@app.route("/dashboard")
def dashboard():
    stats = summarize()
    return render_template("dashboard.html", stats=stats, tableau_url=TABLEAU_DASHBOARD_URL, active="dashboard")


@app.route("/story")
def story():
    return render_template("story.html", tableau_url=TABLEAU_STORY_URL, active="story")


@app.route("/methodology")
def methodology():
    stats = summarize()
    return render_template("methodology.html", stats=stats, active="methodology")


@app.route("/api/summary")
def api_summary():
    return jsonify(summarize())


@app.route("/health")
def health():
    return jsonify({"status": "ok", "app": "EV Market Insights"})


if __name__ == "__main__":
    # Debug is intentionally off by default. Do not expose the dev server to untrusted networks.
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=False)
