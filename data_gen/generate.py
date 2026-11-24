"""Synthetic RFID + POS event generator with deliberately planted findings.

Every number here is fabricated for demo purposes. The planted findings
below are the ones CLAUDE_CODE_PROMPT.md asks the dashboard to surface:

- Footwear: ~11 min average dwell, only ~45% of picked-up items sell.
- Product P115 (Suede Boots): ~80% trial-room rejection rate.
- Store S03: weak footwear-zone antenna, RSSI degrades from ~day 5.
- Store S09: high billing abandonment.
- A "hidden bestseller" pattern: Green Tee (P103) has low pickups but a
  high conversion rate, tucked away in the low-traffic Shelf C zone.

Regenerating (different random seed) will keep the planted patterns but
vary everything else, so the dashboard should not hardcode these numbers
anywhere outside this module.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from core.constants import PRODUCTS, STORE_IDS, ZONES

DAYS = 7
EVENTS_PER_STORE_PER_DAY = 180


def _rssi(distance_cm: float, rng: np.random.Generator, degraded: bool = False) -> float:
    base = -45 - 22 * np.log10(max(distance_cm, 1))
    noise = rng.normal(0, 1.5)
    penalty = 9 if degraded else 0
    return base + noise - penalty


def generate_events(seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    product_by_id = {p["product_id"]: p for p in PRODUCTS}
    footwear_ids = [p["product_id"] for p in PRODUCTS if p["category"] == "Footwear"]

    for store in STORE_IDS:
        for day in range(DAYS):
            degraded_today = store == "S03" and day >= 4  # Shelf B antenna weakens from day 5
            n_events = EVENTS_PER_STORE_PER_DAY
            for _ in range(n_events):
                product = PRODUCTS[rng.integers(0, len(PRODUCTS))]
                pid = product["product_id"]
                zone = product["zone"]
                is_footwear_zone = pid in footwear_ids

                degraded = degraded_today and zone == "Shelf B"

                # base pickup/conversion rates, then bend them for planted findings
                pickup_prob = 0.35
                convert_prob = 0.30

                if pid == "P103":  # hidden bestseller: low pickup, high conversion
                    pickup_prob = 0.12
                    convert_prob = 0.75
                if pid == "P101":  # Navy Blazer: many pickups, few sales
                    pickup_prob = 0.55
                    convert_prob = 0.10
                if pid == "P104":  # Wool Scarf: dead stock, nobody picks it up
                    pickup_prob = 0.02
                    convert_prob = 0.05
                if is_footwear_zone:
                    pickup_prob = 0.45  # footwear draws attention...
                if pid == "P115":  # ...but Suede Boots gets tried and rejected
                    convert_prob = 0.20  # trial accept rate low -> computed as rejection ~80%

                picked_up = rng.random() < pickup_prob
                converted = picked_up and (rng.random() < convert_prob)
                returned_wrong_zone = picked_up and pid == "P105" and rng.random() < 0.3

                dwell_seconds = rng.normal(90, 30)
                if is_footwear_zone:
                    dwell_seconds = rng.normal(11 * 60, 90)

                distance_cm = rng.uniform(15, 60)
                rssi = _rssi(distance_cm, rng, degraded=degraded)
                is_ghost = rssi < -66 and rng.random() < 0.5

                rows.append(
                    {
                        "store_id": store,
                        "day": day,
                        "zone": zone,
                        "event_type": "shelf",
                        "product_id": pid,
                        "product_name": product["name"],
                        "category": product["category"],
                        "price": product["price"],
                        "picked_up": picked_up,
                        "converted": converted,
                        "billing_abandoned": False,
                        "returned_wrong_zone": returned_wrong_zone,
                        "dwell_seconds": max(dwell_seconds, 5),
                        "rssi": rssi,
                        "is_ghost_read": is_ghost,
                        "trial_rejected": False,
                    }
                )

            # --- Fitting Room visits (so Trial Room Manager has data) ---
            for _ in range(30):
                product = PRODUCTS[rng.integers(0, len(PRODUCTS))]
                pid = product["product_id"]
                is_suede_boots = pid == "P115"
                reject_prob = 0.8 if is_suede_boots else 0.25
                rejected = rng.random() < reject_prob
                dwell_seconds = rng.normal(150, 40)
                distance_cm = rng.uniform(15, 60)
                rssi = _rssi(distance_cm, rng)
                is_ghost = rssi < -66 and rng.random() < 0.3

                rows.append(
                    {
                        "store_id": store,
                        "day": day,
                        "zone": "Fitting Room",
                        "event_type": "trial",
                        "product_id": pid,
                        "product_name": product["name"],
                        "category": product["category"],
                        "price": product["price"],
                        "picked_up": True,
                        "converted": not rejected,
                        "billing_abandoned": False,
                        "returned_wrong_zone": False,
                        "dwell_seconds": max(dwell_seconds, 5),
                        "rssi": rssi,
                        "is_ghost_read": is_ghost,
                        "trial_rejected": rejected,
                    }
                )

            # --- Billing visits (so Billing Manager has data) ---
            for _ in range(40):
                product = PRODUCTS[rng.integers(0, len(PRODUCTS))]
                pid = product["product_id"]
                billing_abandon = store == "S09" and rng.random() < 0.35
                dwell_seconds = rng.normal(120, 40)
                distance_cm = rng.uniform(15, 60)
                rssi = _rssi(distance_cm, rng)
                is_ghost = rssi < -66 and rng.random() < 0.3

                rows.append(
                    {
                        "store_id": store,
                        "day": day,
                        "zone": "Billing",
                        "event_type": "billing",
                        "product_id": pid,
                        "product_name": product["name"],
                        "category": product["category"],
                        "price": product["price"],
                        "picked_up": True,
                        "converted": not billing_abandon,
                        "billing_abandoned": billing_abandon,
                        "returned_wrong_zone": False,
                        "dwell_seconds": max(dwell_seconds, 5),
                        "rssi": rssi,
                        "is_ghost_read": is_ghost,
                        "trial_rejected": False,
                    }
                )

    return pd.DataFrame(rows)


def load_events(seed: int = 42) -> pd.DataFrame:
    """Cached-friendly entry point for the app to call."""
    return generate_events(seed=seed)
