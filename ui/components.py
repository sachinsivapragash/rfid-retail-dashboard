"""Reusable Streamlit components: KPI rows and alert/action cards."""
from __future__ import annotations

import streamlit as st

from ui.theme import PALETTE, kpi_card


def kpi_row(items: list[tuple[str, str, str]]) -> None:
    """items: list of (label, value, color-key-or-hex)."""
    cols = st.columns(len(items))
    for col, (label, value, color) in zip(cols, items):
        hex_color = PALETTE.get(color, color)
        with col:
            st.markdown(kpi_card(label, value, hex_color), unsafe_allow_html=True)


def alert_card(card: dict, key: str) -> None:
    status_key = f"alert_status::{key}"
    status = st.session_state.get(status_key, "open")

    border = {"open": "#FF4B91", "done": "#1DB954", "ignored": "#999999"}[status]
    st.markdown(
        f"""
        <div class="alert-card" style="border-left-color:{border};">
            <strong>{card['title']}</strong><br/>
            {card['detail']}<br/>
            <span>Estimated impact: ₹{card['impact_rupees']:,} · Confidence: {card['confidence']*100:.0f}%</span>
            <div class="why">Why this card? {card['why']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns([1, 1, 4])
    with c1:
        if st.button("Done", key=f"done::{key}"):
            st.session_state[status_key] = "done"
            st.rerun()
    with c2:
        if st.button("Ignore", key=f"ignore::{key}"):
            st.session_state[status_key] = "ignored"
            st.rerun()
