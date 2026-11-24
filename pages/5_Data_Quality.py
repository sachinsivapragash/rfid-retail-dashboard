from __future__ import annotations

import streamlit as st

from processing.pipeline import apply_scope
from ui.theme import inject

st.set_page_config(page_title="Data quality & privacy", page_icon="🔒", layout="wide")
inject()

if not st.session_state.get("scope"):
    st.warning("Please sign in from the home page first.")
    st.stop()

scope = st.session_state["scope"]
raw = apply_scope(st.session_state["events_raw"], scope)
clean = apply_scope(st.session_state["events_clean"], scope)

st.title("🔒 Data quality & privacy")

c1, c2, c3 = st.columns(3)
c1.metric("Raw reads", len(raw))
c2.metric("Clean reads (ghosts removed)", len(clean))
ghost_rate = (1 - len(clean) / len(raw)) * 100 if len(raw) else 0
c3.metric("Ghost read rate", f"{ghost_rate:.1f}%")

st.subheader("Reader performance (median RSSI by zone)")
st.dataframe(
    clean.groupby("zone")["rssi"].median().round(1).reset_index(name="median_rssi_dbm"),
    use_container_width=True,
    hide_index=True,
)

st.subheader("Privacy")
st.markdown(
    """
    - Customer identifiers are anonymous session IDs — no PII is stored.
    - Consent status and a data-retention date should be tracked per session
      (not yet modeled in this scaffold — see `CLAUDE_CODE_PROMPT.md`).
    - All data on this page is synthetic.
    """
)
