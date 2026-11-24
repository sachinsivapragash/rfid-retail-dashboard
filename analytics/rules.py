"""Explainable suggestion engine: ports the rule logic from rfid_sim_engine.py.

Each rule returns a list of action-card dicts: title, detail, impact_rupees
(an estimate), confidence (0-1), and why (the formula/reasoning).
"""
from __future__ import annotations

import pandas as pd

from core.constants import RESTOCK_LEAD_TIME_DAYS, RSSI_DEGRADE_DB

REALISATION_FACTOR = 0.5


def _shelf_only(df: pd.DataFrame) -> pd.DataFrame:
    """Rules about pickup/conversion on the shop floor should ignore the
    always-picked-up Fitting Room / Billing visit rows."""
    return df[df["event_type"] == "shelf"] if "event_type" in df.columns else df


def high_interest_low_conversion(df: pd.DataFrame) -> list[dict]:
    cards = []
    df = _shelf_only(df)
    picked = df[df["picked_up"]]
    if picked.empty:
        return cards
    median_conv = picked.groupby("product_id")["converted"].mean().median()
    grouped = picked.groupby(["product_id", "product_name"])
    for (pid, name), g in grouped:
        pickups = len(g)
        if pickups < 25:
            continue
        conv = g["converted"].mean()
        se = (conv * (1 - conv) / pickups) ** 0.5
        if conv + 1.64 * se < 0.6 * median_conv:
            impact = round(pickups * (median_conv - conv) * g["price"].iloc[0] * REALISATION_FACTOR)
            cards.append(
                {
                    "title": f"{name}: high interest, low conversion",
                    "detail": f"{pickups} pickups but only {conv*100:.0f}% convert.",
                    "impact_rupees": impact,
                    "confidence": round(min(0.95, 0.5 + pickups / 200), 2),
                    "why": "pickups ≥ 25 and conversion + 1.64×SE below 0.6× store median conversion",
                }
            )
    return cards


def relocate_hidden_bestseller(df: pd.DataFrame) -> list[dict]:
    cards = []
    df = _shelf_only(df)
    picked = df[df["picked_up"]]
    if picked.empty:
        return cards
    counts = picked.groupby(["product_id", "product_name", "zone"]).agg(
        pickups=("picked_up", "count"), conversion=("converted", "mean")
    )
    median_pickups = counts["pickups"].median()
    median_conv = counts["conversion"].median()
    for (pid, name, zone), row in counts.iterrows():
        if row["pickups"] < median_pickups / 2 and row["conversion"] > median_conv:
            impact = round(row["pickups"] * row["conversion"] * 500 * REALISATION_FACTOR)
            cards.append(
                {
                    "title": f"{name}: hidden bestseller in {zone}",
                    "detail": f"Only {row['pickups']} pickups but {row['conversion']*100:.0f}% convert — move to a higher-traffic zone.",
                    "impact_rupees": impact,
                    "confidence": 0.7,
                    "why": "pickups < 0.5× store median and conversion above store median",
                }
            )
    return cards


def dead_stock(df: pd.DataFrame) -> list[dict]:
    cards = []
    df = _shelf_only(df)
    counts = df.groupby(["product_id", "product_name"])["picked_up"].sum()
    for (pid, name), pickups in counts.items():
        if pickups <= 2:
            cards.append(
                {
                    "title": f"{name}: dead stock",
                    "detail": f"Only {pickups} pickups across the period.",
                    "impact_rupees": 0,
                    "confidence": 0.9,
                    "why": "stocked product with ≤ 2 pickups in the period",
                }
            )
    return cards


def misplaced_items(df: pd.DataFrame) -> list[dict]:
    cards = []
    returns = df[df["returned_wrong_zone"]]
    if returns.empty:
        return cards
    by_product = df.groupby("product_name")["returned_wrong_zone"].mean()
    for name, rate in by_product.items():
        if rate >= 0.25:
            cards.append(
                {
                    "title": f"{name}: often returned to the wrong shelf",
                    "detail": f"{rate*100:.0f}% of returns land in a different zone than expected.",
                    "impact_rupees": 0,
                    "confidence": 0.75,
                    "why": "≥ 25% of detected returns land in a different zone",
                }
            )
    return cards


def reader_health(df: pd.DataFrame) -> list[dict]:
    cards = []
    for (store, zone), g in df.groupby(["store_id", "zone"]):
        g = g.sort_values("day")
        baseline_rows = g[g["day"] < 3]
        recent_rows = g[g["day"] >= 5]
        if len(baseline_rows) < 60 or len(recent_rows) < 40:
            continue  # not enough samples to trust the comparison
        baseline = baseline_rows["rssi"].median()
        recent = recent_rows["rssi"].median()
        if pd.notna(baseline) and pd.notna(recent) and baseline - recent > RSSI_DEGRADE_DB:
            cards.append(
                {
                    "title": f"{store} — {zone}: reader signal degrading",
                    "detail": f"Median RSSI dropped {baseline - recent:.1f} dB vs. the first 3 days.",
                    "impact_rupees": 0,
                    "confidence": 0.6,  # 40% less confidence, as suggestions from this zone are discounted
                    "why": "zone median RSSI > 4 dB below its day-1-3 baseline for 2+ days",
                }
            )
    return cards


def billing_abandonment(df: pd.DataFrame) -> list[dict]:
    cards = []
    billing = df[df["zone"] == "Billing"]
    for store, g in billing.groupby("store_id"):
        rate = g["billing_abandoned"].mean()
        if rate > 0.2:
            cards.append(
                {
                    "title": f"{store}: high billing abandonment",
                    "detail": f"{rate*100:.0f}% of billing visits are abandoned before purchase.",
                    "impact_rupees": round(rate * len(g) * 1200 * REALISATION_FACTOR),
                    "confidence": 0.8,
                    "why": "billing-zone abandonment rate above 20%",
                }
            )
    return cards


def all_suggestions(df: pd.DataFrame) -> list[dict]:
    cards = []
    for fn in (
        high_interest_low_conversion,
        relocate_hidden_bestseller,
        dead_stock,
        misplaced_items,
        reader_health,
        billing_abandonment,
    ):
        cards.extend(fn(df))
    cards.sort(key=lambda c: c["impact_rupees"] * c["confidence"], reverse=True)
    return cards
