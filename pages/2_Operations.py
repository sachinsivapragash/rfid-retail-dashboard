from __future__ import annotations

import plotly.express as px
import streamlit as st

from analytics.kpis import product_performance, zone_engagement
from processing.pipeline import apply_scope
from ui.theme import PALETTE, inject

st.set_page_config(page_title="Operations", page_icon="🧭", layout="wide")
inject()

if not st.session_state.get("scope"):
    st.warning("Please sign in from the home page first.")
    st.stop()

scope = st.session_state["scope"]
df = apply_scope(st.session_state["events_clean"], scope)

st.title("🧭 Operations")

st.subheader("Zone engagement")
zdf = zone_engagement(df)
fig = px.bar(
    zdf,
    x="zone",
    y="pickup_rate",
    color="zone",
    color_discrete_map=PALETTE,
    labels={"pickup_rate": "Pick-up rate (%)"},
)
fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Product performance (by pickups)")
pdf = product_performance(df)
st.dataframe(pdf, use_container_width=True, hide_index=True)
