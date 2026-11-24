"""KPI calculations over the (already scoped) cleaned event table."""
from __future__ import annotations

import pandas as pd


def summary_kpis(df: pd.DataFrame) -> dict:
    if df.empty:
        return {
            "avg_dwell_min": 0.0,
            "pickup_rate": 0.0,
            "conversion_rate": 0.0,
            "billing_abandonment_rate": 0.0,
            "avg_bill_value": 0.0,
            "return_rate": 0.0,
        }

    picked = df[df["picked_up"]]
    billing = df[df["zone"] == "Billing"]

    return {
        "avg_dwell_min": round(df["dwell_seconds"].mean() / 60, 1),
        "pickup_rate": round(df["picked_up"].mean() * 100, 1),
        "conversion_rate": round((picked["converted"].mean() * 100) if len(picked) else 0.0, 1),
        "billing_abandonment_rate": round((billing["billing_abandoned"].mean() * 100) if len(billing) else 0.0, 1),
        "avg_bill_value": round(df.loc[df["converted"], "price"].mean(), 0) if df["converted"].any() else 0.0,
        "return_rate": round(df["returned_wrong_zone"].mean() * 100, 1),
    }


def zone_engagement(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("zone")
        .agg(
            avg_dwell_min=("dwell_seconds", lambda s: round(s.mean() / 60, 1)),
            pickup_rate=("picked_up", lambda s: round(s.mean() * 100, 1)),
            events=("zone", "count"),
        )
        .reset_index()
    )


def product_performance(df: pd.DataFrame) -> pd.DataFrame:
    picked = df[df["picked_up"]]
    return (
        picked.groupby(["product_id", "product_name", "category", "zone"])
        .agg(
            pickups=("picked_up", "count"),
            conversion_rate=("converted", lambda s: round(s.mean() * 100, 1)),
        )
        .reset_index()
        .sort_values("pickups", ascending=False)
    )


def store_leaderboard(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    sales = (
        df[df["converted"]]
        .groupby("store_id")["price"]
        .sum()
        .reset_index(name="revenue")
        .sort_values("revenue", ascending=False)
        .head(top_n)
    )
    return sales


def peak_hours_placeholder(df: pd.DataFrame) -> pd.DataFrame:
    """Day-level activity as a stand-in until true timestamps are generated."""
    return df.groupby("day").size().reset_index(name="events")
