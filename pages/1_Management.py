from __future__ import annotations

import streamlit as st

from analytics.kpis import store_leaderboard, summary_kpis
from processing.pipeline import apply_scope
from ui.components import kpi_row
from ui.theme import inject

st.set_page_config(page_title="Management", page_icon="📊", layout="wide")
inject()

if not st.session_state.get("scope"):
    st.warning("Please sign in from the home page first.")
    st.stop()

scope = st.session_state["scope"]
df = apply_scope(st.session_state["events_clean"], scope)

st.title("📊 Management overview")

k = summary_kpis(df)
kpi_row(
    [
        ("Avg. dwell", f"{k['avg_dwell_min']} min", "Shelf A"),
        ("Pick-up rate", f"{k['pickup_rate']}%", "Shelf B"),
        ("Conversion", f"{k['conversion_rate']}%", "good"),
        ("Avg. bill value", f"₹{k['avg_bill_value']:,.0f}", "Billing"),
        ("Billing abandonment", f"{k['billing_abandonment_rate']}%", "bad"),
    ]
)

st.subheader("Top stores by revenue")
if scope["role"] == "Higher Management":
    lb = store_leaderboard(df, top_n=10)
    st.bar_chart(lb.set_index("store_id")["revenue"])
else:
    st.caption("Store leaderboard is only available to Higher Management.")

st.subheader("Recommendations")
st.caption("See the Alerts page for the full, explainable suggestion list with ₹ impact and confidence.")
