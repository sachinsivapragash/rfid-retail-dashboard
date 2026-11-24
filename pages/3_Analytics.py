from __future__ import annotations

import plotly.express as px
import streamlit as st

from analytics.kpis import peak_hours_placeholder, zone_engagement
from processing.pipeline import apply_scope
from ui.theme import inject

st.set_page_config(page_title="Analytics", page_icon="📈", layout="wide")
inject()

if not st.session_state.get("scope"):
    st.warning("Please sign in from the home page first.")
    st.stop()

scope = st.session_state["scope"]
df = apply_scope(st.session_state["events_clean"], scope)

st.title("📈 Analytics")

st.subheader("Activity over time")
peak = peak_hours_placeholder(df)
fig = px.line(peak, x="day", y="events", markers=True)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Dwell time by zone (heatmap-style)")
zdf = zone_engagement(df)
fig2 = px.bar(zdf, x="zone", y="avg_dwell_min", color="avg_dwell_min", color_continuous_scale="Sunset")
st.plotly_chart(fig2, use_container_width=True)

st.caption(
    "TODO for a fuller build: Sankey zone-flow diagram, floor heatmap, "
    "what-if layout simulator — see CLAUDE_CODE_PROMPT.md."
)
