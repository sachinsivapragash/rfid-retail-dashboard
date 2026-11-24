"""Shared constants: stores, zones, products, roles and access keys.

All data in this project is synthetic. See CLAUDE_CODE_PROMPT.md for the
full spec this scaffold was generated from.
"""
from __future__ import annotations

STORE_IDS = [f"S{str(i).zfill(2)}" for i in range(1, 11)]

STORE_CITIES = {
    "S01": "Coimbatore",
    "S02": "Chennai",
    "S03": "Madurai",
    "S04": "Salem",
    "S05": "Tiruppur",
    "S06": "Trichy",
    "S07": "Erode",
    "S08": "Vellore",
    "S09": "Tirunelveli",
    "S10": "Thanjavur",
}

ZONES = ["Shelf A", "Shelf B", "Shelf C", "Fitting Room", "Billing"]

ZONE_TRAFFIC = {
    "Shelf A": "high",
    "Shelf B": "medium",
    "Shelf C": "low",
    "Fitting Room": "n/a",
    "Billing": "n/a",
}

PRODUCTS = [
    {"product_id": "P101", "name": "Navy Blazer", "category": "Formal", "zone": "Shelf A", "price": 2999},
    {"product_id": "P102", "name": "Red Polo", "category": "Casual", "zone": "Shelf A", "price": 899},
    {"product_id": "P103", "name": "Green Tee", "category": "Casual", "zone": "Shelf C", "price": 499},
    {"product_id": "P104", "name": "Wool Scarf", "category": "Accessory", "zone": "Shelf B", "price": 699},
    {"product_id": "P105", "name": "Denim Jacket", "category": "Casual", "zone": "Shelf B", "price": 2499},
    {"product_id": "P106", "name": "White Shirt", "category": "Formal", "zone": "Shelf A", "price": 1299},
    {"product_id": "P107", "name": "Black Trousers", "category": "Formal", "zone": "Shelf A", "price": 1599},
    {"product_id": "P108", "name": "Floral Dress", "category": "Casual", "zone": "Shelf B", "price": 1899},
    {"product_id": "P109", "name": "Grey Hoodie", "category": "Casual", "zone": "Shelf A", "price": 1399},
    {"product_id": "P110", "name": "Leather Belt", "category": "Accessory", "zone": "Shelf C", "price": 799},
    {"product_id": "P111", "name": "Linen Kurta", "category": "Ethnic", "zone": "Shelf B", "price": 1199},
    {"product_id": "P112", "name": "Running Shoes", "category": "Footwear", "zone": "Shelf A", "price": 2199},
    {"product_id": "P113", "name": "Canvas Sneakers", "category": "Footwear", "zone": "Shelf C", "price": 1499},
    {"product_id": "P114", "name": "Formal Loafers", "category": "Footwear", "zone": "Shelf A", "price": 2699},
    {"product_id": "P115", "name": "Suede Boots", "category": "Footwear", "zone": "Shelf B", "price": 3199},
    {"product_id": "P116", "name": "Sports Cap", "category": "Accessory", "zone": "Shelf C", "price": 399},
]

ROLES = {
    "HQ-9000": {"role": "Higher Management", "store": None, "zone": None},
    "SM-1001": {"role": "Store Manager", "store": "S01", "zone": None},
    "ZM-2001": {"role": "Zone Manager", "store": "S01", "zone": "Footwear"},
    "TM-3001": {"role": "Trial Room Manager", "store": None, "zone": "Fitting Room"},
    "BM-4001": {"role": "Billing Manager", "store": None, "zone": "Billing"},
}

RESTOCK_LEAD_TIME_DAYS = 5
GHOST_READ_RSSI_THRESHOLD = -66
RSSI_DEGRADE_DB = 5
