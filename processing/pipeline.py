"""Event processing: filter ghost reads, score confidence, apply scope."""
from __future__ import annotations

import pandas as pd


def clean_events(df: pd.DataFrame) -> pd.DataFrame:
    """Drop ghost reads and attach a simple confidence score."""
    clean = df[~df["is_ghost_read"]].copy()
    clean["confidence"] = (clean["rssi"].clip(lower=-90, upper=-30) + 90) / 60
    return clean


def apply_scope(df: pd.DataFrame, scope: dict) -> pd.DataFrame:
    """Filter events to what this role/access-key is allowed to see."""
    out = df
    if scope.get("store"):
        out = out[out["store_id"] == scope["store"]]
    if scope.get("zone") == "Footwear":
        out = out[out["category"] == "Footwear"]
    elif scope.get("zone") == "Fitting Room":
        out = out[out["zone"] == "Fitting Room"]
    elif scope.get("zone") == "Billing":
        out = out[out["zone"] == "Billing"]
    return out
