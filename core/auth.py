"""Access-key based role scoping."""
from __future__ import annotations

from core.constants import ROLES


def resolve_key(key: str) -> dict | None:
    """Return the role/scope dict for an access key, or None if invalid."""
    return ROLES.get(key.strip().upper())


def scope_label(scope: dict) -> str:
    bits = [scope["role"]]
    if scope.get("store"):
        bits.append(f"Store {scope['store']}")
    if scope.get("zone"):
        bits.append(f"{scope['zone']} zone")
    return " · ".join(bits)
