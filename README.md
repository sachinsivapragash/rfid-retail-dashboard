# RFID Retail Analytics Dashboard

A synthetic-data Streamlit dashboard for RFID-based retail customer
interaction analytics — a working scaffold meant to be extended by
Claude Code. See **`CLAUDE_CODE_PROMPT.md`** for the full feature spec
and known gaps to build next.

All data in this project is synthetic and generated locally
(`data_gen/generate.py`). Nothing here connects to real hardware or a
real store.

## Run it

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

Open the URL Streamlit prints (defaults to `http://localhost:8501`).

## Demo access keys

| Role | Key | Scope |
|---|---|---|
| Higher Management | `HQ-9000` | All stores, all tabs |
| Store Manager | `SM-1001` | Store S01 (Coimbatore) |
| Zone Manager | `ZM-2001` | S01, Footwear zone |
| Trial Room Manager | `TM-3001` | Trial-room data |
| Billing Manager | `BM-4001` | Billing data |

## Project layout

```
app.py                  # entry point: login + routing
core/                   # constants, access-key -> role/scope resolution
data_gen/               # synthetic event generator (planted findings)
processing/             # cleaning, ghost-read filtering, scoping
analytics/              # KPI calculations + explainable suggestion rules
ui/                     # color palette, CSS, shared components
pages/                  # one file per dashboard screen (Streamlit multipage)
tests/                  # smoke tests (pytest)
CLAUDE_CODE_PROMPT.md   # the spec to hand to Claude Code next
```

## Tests

```bash
pytest
```

## Status

This is an MVP scaffold: login, role-scoping, synthetic data with the
planted findings, KPI cards, basic charts, and an explainable alert
engine all work end to end. Known gaps (no persistence for alert
acknowledgements, no stock-out rule yet, no Sankey/heatmap/what-if
simulator, minimal tooltips) are listed in `CLAUDE_CODE_PROMPT.md` under
"Known gaps" and "Stretch goals."
