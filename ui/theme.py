"""Vibrant-but-clean color palette and shared CSS injection."""
from __future__ import annotations

import streamlit as st

PALETTE = {
    "Shelf A": "#FF4B91",
    "Shelf B": "#2EC4B6",
    "Shelf C": "#FFB400",
    "Fitting Room": "#7B61FF",
    "Billing": "#FF6B35",
    "good": "#1DB954",
    "warn": "#FFB400",
    "bad": "#FF4B4B",
    "ink": "#1A1A2E",
    "bg_soft": "#F4F1FF",
}

CSS = """
<style>
.block-container {padding-top: 2rem; padding-bottom: 3rem;}
.kpi-card {
    border-radius: 16px;
    padding: 1.1rem 1.3rem;
    color: white;
    box-shadow: 0 6px 18px rgba(0,0,0,0.12);
}
.kpi-card .label {font-size: 0.8rem; opacity: 0.85; text-transform: uppercase; letter-spacing: 0.04em;}
.kpi-card .value {font-size: 1.8rem; font-weight: 700; margin-top: 0.1rem;}
.alert-card {
    border-radius: 14px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
    background: #FFFFFF;
    border-left: 8px solid #FF4B91;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
}
.alert-card .why {font-size: 0.8rem; color: #666; margin-top: 0.3rem;}
h1, h2, h3 {letter-spacing: -0.01em;}
</style>
"""


def inject() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def kpi_card(label: str, value: str, color: str) -> str:
    return (
        f'<div class="kpi-card" style="background:{color};">'
        f'<div class="label">{label}</div>'
        f'<div class="value">{value}</div>'
        f"</div>"
    )
