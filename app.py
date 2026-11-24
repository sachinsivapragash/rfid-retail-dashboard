"""RFID Retail Analytics — entry point.

Role-based login by access key, then routes to the pages/ multipage app.
All data is synthetic (see data_gen/generate.py). See CLAUDE_CODE_PROMPT.md
for the full feature spec this scaffold is meant to grow into.
"""
from __future__ import annotations

import streamlit as st

from core.auth import resolve_key, scope_label
from data_gen.generate import load_events
from processing.pipeline import clean_events
from ui.theme import inject

st.set_page_config(page_title="RFID Retail Analytics", page_icon="📡", layout="wide")
inject()

if "scope" not in st.session_state:
    st.session_state["scope"] = None

st.title("📡 RFID Retail Analytics")
st.caption("Synthetic demo data · Tamil Nadu apparel chain · built to beat GarudaVigil on interaction analytics, layout insight and data trust")

if st.session_state["scope"] is None:
    st.subheader("Sign in with your access key")
    key = st.text_input("Access key", placeholder="e.g. HQ-9000", type="password")
    if st.button("Enter dashboard", type="primary"):
        scope = resolve_key(key)
        if scope:
            st.session_state["scope"] = scope
            st.rerun()
        else:
            st.error("Access key not recognised. Try HQ-9000, SM-1001, ZM-2001, TM-3001 or BM-4001.")

    with st.expander("Demo access keys"):
        st.markdown(
            """
            | Role | Key | Scope |
            |---|---|---|
            | Higher Management | `HQ-9000` | All stores, all tabs |
            | Store Manager | `SM-1001` | Store S01 (Coimbatore) |
            | Zone Manager | `ZM-2001` | S01, Footwear zone |
            | Trial Room Manager | `TM-3001` | Trial-room data |
            | Billing Manager | `BM-4001` | Billing data |
            """
        )
else:
    scope = st.session_state["scope"]
    with st.sidebar:
        st.success(f"Signed in as **{scope_label(scope)}**")
        if st.button("Sign out"):
            st.session_state["scope"] = None
            st.rerun()
        st.divider()
        st.page_link("pages/1_Management.py", label="Management", icon="📊")
        st.page_link("pages/2_Operations.py", label="Operations", icon="🧭")
        st.page_link("pages/3_Analytics.py", label="Analytics", icon="📈")
        st.page_link("pages/4_Alerts.py", label="Alerts", icon="🚨")
        st.page_link("pages/5_Data_Quality.py", label="Data quality & privacy", icon="🔒")

    st.info("Use the pages in the sidebar. Everything you see is scoped to your access key.")

    events = load_events()
    cleaned = clean_events(events)
    st.session_state["events_raw"] = events
    st.session_state["events_clean"] = cleaned
