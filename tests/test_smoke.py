"""Smoke tests: data generates, every access key resolves, rules don't crash."""
from core.auth import resolve_key
from core.constants import ROLES
from data_gen.generate import load_events
from processing.pipeline import apply_scope, clean_events
from analytics.kpis import summary_kpis
from analytics.rules import all_suggestions


def test_data_generates():
    df = load_events()
    assert len(df) > 0
    assert {"store_id", "zone", "product_id", "rssi"}.issubset(df.columns)


def test_all_access_keys_resolve():
    for key in ROLES:
        scope = resolve_key(key)
        assert scope is not None
        assert "role" in scope


def test_scoping_and_kpis_per_role():
    df = clean_events(load_events())
    for key, scope in ROLES.items():
        scoped = apply_scope(df, scope)
        kpis = summary_kpis(scoped)
        assert "conversion_rate" in kpis


def test_suggestions_do_not_crash():
    df = clean_events(load_events())
    cards = all_suggestions(df)
    assert isinstance(cards, list)
    for c in cards:
        assert "impact_rupees" in c and "confidence" in c
