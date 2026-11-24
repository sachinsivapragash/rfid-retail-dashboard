from __future__ import annotations

import streamlit as st

from analytics.rules import all_suggestions
from processing.pipeline import apply_scope
from ui.components import alert_card
from ui.theme import inject

st.set_page_config(page_title="Alerts", page_icon="🚨", layout="wide")
inject()

if not st.session_state.get("scope"):
    st.warning("Please sign in from the home page first.")
    st.stop()

scope = st.session_state["scope"]
df = apply_scope(st.session_state["events_clean"], scope)

st.title("🚨 Alerts & suggestions")
st.caption(
    "Every ₹ figure here is an estimate from synthetic data (50% realisation factor), "
    "scored against planted problems in our own simulator — not real-store accuracy."
)

min_confidence = st.sidebar.slider("Minimum confidence", 0.0, 1.0, 0.5, 0.05)

cards = [c for c in all_suggestions(df) if c["confidence"] >= min_confidence]

if not cards:
    st.success("No alerts above this confidence threshold.")
else:
    for i, card in enumerate(cards):
        alert_card(card, key=f"{card['title']}::{i}")

st.caption(
    "⚠️ Alert acknowledgement state currently lives only in this browser session. "
    "A real build should persist it (SQLite/Postgres) — see CLAUDE_CODE_PROMPT.md."
)
