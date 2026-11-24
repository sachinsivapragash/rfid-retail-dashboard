# Prompt for Claude Code — continue this dashboard

Paste this into Claude Code, pointed at this repo, to pick up where the
scaffold leaves off.

---

Complete and polish this Streamlit RFID retail analytics dashboard
(`app.py` + `pages/`, runs via `python -m streamlit run app.py`). Extend
and polish what exists here — don't throw it away — and don't mix in real
ESP32 hardware scans; all data stays synthetic (`data_gen/generate.py`).

## Project context
This is a student project (Forge KCT, PRICE track) building RFID-based
retail customer interaction analytics, benchmarked against i-TEK's
GarudaVigil platform. The goal is to beat GarudaVigil on: customer
interaction analytics, store layout/placement insight, explainable
suggestions with ₹ impact, and trust in the data (RFID signal quality,
detected vs. true events). Audience: SME retail and Tier-2/3 market
economics — the dashboard should read as affordable and explain money
impact in rupees. Readers are store managers, zone managers, trial-room
managers, billing managers, and higher management.

## The five architectural layers (from the original requirements doc)
1. **Data Collection**: EPC, Product ID, Reader ID, Antenna ID,
   timestamp, RSSI, Zone ID, Store ID, POS Transaction ID.
2. **Data Processing**: event/session IDs, event type, entry/exit time,
   previous/current zone, dwell time, read count, movement status,
   event confidence score. (`processing/pipeline.py` is a minimal start.)
3. **Operational dashboard**: customer, zone, product, trial room,
   billing activity. (`pages/2_Operations.py`)
4. **Analytical dashboard**: KPIs, patterns, conversion/rejection rates.
   (`pages/3_Analytics.py`)
5. **Management dashboard**: insights for store and higher management.
   (`pages/1_Management.py`)

Common keys: `Store_ID`, `Session_ID`, `EPC_ID`, `Product_ID`, `Zone_ID`,
`Transaction_ID`.

## Roles and access keys (already wired up in `core/auth.py`)
| Role | Key | Scope |
|---|---|---|
| Higher Management | `HQ-9000` | All stores, all tabs |
| Store Manager | `SM-1001` | Store S01 (Coimbatore) |
| Zone Manager | `ZM-2001` | S01, Footwear zone |
| Trial Room Manager | `TM-3001` | Trial-room data |
| Billing Manager | `BM-4001` | Billing data |

## KPIs to surface
Average customer dwell, average zone dwell, zone engagement rate,
product interaction rate, pick-up rate, return rate, trial
acceptance/rejection rate, billing abandonment, purchase conversion,
average bill value, category performance. Derived: movement path,
products per customer, zones per visit, product interest score, journey
completion rate, peak shopping hours. Every KPI needs a tooltip
explaining its definition (not yet added — `st.help`/custom tooltip).

## Synthetic data (already generated in `data_gen/generate.py`)
10 Tamil Nadu stores, 16 apparel products, zones: Shelf A (front, high
traffic), Shelf B, Shelf C (back corner, low traffic), Fitting Room,
Billing, over 7 days. Includes a noise model (RSSI, ghost reads) and the
following **planted findings**, which the dashboard's rules should
surface correctly:

- Footwear: ~11 min average dwell, only ~45% of picked-up items sell.
- Product P115 (Suede Boots): ~80% trial-room rejection rate.
- Store S03: weak footwear-zone antenna, RSSI degrades from ~day 5.
- Store S09: high billing abandonment.
- A "hidden bestseller" (Green Tee / P103): low pickups but high
  conversion, in the low-traffic Shelf C zone — this is deliberately the
  hardest pattern to catch; don't over-tune it to 100%.

Extend this generator to cover 90 days and 300+ SKUs across all 10
stores with festival surges and ~4% POS mismatches if you want it closer
to a full production-shaped demo (see "Stretch goals" below).

## Suggestion engine (`analytics/rules.py` — ported, extend as needed)
- *High interest, low conversion*: ≥25 pickups, conversion + 1.64×SE
  below 0.6× store median conversion.
- *Relocate a hidden bestseller*: pickups < 0.5× store median, but
  conversion above store median.
- *Stock-out risk*: stock ÷ daily sales below the 5-day restock lead
  time. **(Not yet implemented — needs a stock-level field added to the
  data generator.)**
- *Dead stock*: ≤2 pickups in the period.
- *Misplaced items*: ≥25% of detected returns land in a different zone.
- *Reader health*: zone median RSSI >4 dB below its day-1–3 baseline for
  2+ days; suggestions from that zone get 40% less confidence.
- *Billing abandonment*: store billing-abandonment rate > 20%.
- Impact in ₹ uses a 50% realisation factor and must be labeled as an
  **estimate**. Priority = impact × confidence. Every card should show a
  "Why this card?" explanation (already in `alert_card`).
- Always label accuracy/precision/recall numbers as "tested against
  planted problems in our own simulator," never as real-store accuracy.

## Screens/tabs (scaffolded in `pages/`, extend each)
- **Management**: KPIs vs. previous period, trends, best/worst zone,
  highest-rejection products, peak hours, recommendations, top 5/10
  store leaderboard (HQ only).
- **Operations**: customer, zone, product, trial room, billing views.
- **Analytics**: all KPIs, derived attributes, movement paths. Add a
  **Sankey zone-flow diagram** and a **floor heatmap** (stretch goal).
- **Alerts**: sidebar-configurable thresholds, persistent Done/Ignore
  (currently session-only — see Known gaps below).
- **Data quality & privacy**: raw vs. unique reads, ghost-read rate,
  reader performance, POS match rate (not modeled yet), consent status
  and retention date (not modeled yet).
- **Live tab**: simulated events streaming in periodically — consider
  `st.fragment` with a short `time.sleep`/rerun loop. **(Not yet built.)**

## Known gaps in this scaffold — fix these first
1. **No persistence.** Alert Done/Ignore state lives only in
   `st.session_state`. Add SQLite (SQLAlchemy, Postgres-compatible
   schema) so it survives a restart.
2. **Alerts have no time-window control** on the lookback period —
   add a sidebar date/day-range filter feeding into `apply_scope`.
3. **No POS validation or stock levels** — the data generator doesn't
   yet produce stock quantities or POS mismatches, so `stockout_risk`
   isn't implemented. Add a `stock_qty` and `daily_sales` field.
4. **No true timestamps** — `day` is used as a stand-in for peak-hours
   analysis; add actual hour-of-day distributions if you want a real
   peak-hours KPI.
5. **Tooltips are missing** on KPI cards.
6. **Charts are functional but minimal** — add drill-down (click a KPI
   to filter the page below it), and more polished Plotly styling.

## UI/UX requirements
- Clean, simple layout (already in `ui/theme.py` / `ui/components.py`)
  with a bold, vibrant, high-contrast palette per zone/role/status —
  keep extending this system rather than introducing ad hoc colors.
- Genuinely interactive: filters, drill-downs, hover tooltips on every
  KPI, clickable/actionable alert cards with persisted state.
- Plotly for all charts (not matplotlib).
- Indian currency formatting (₹) throughout — already used, keep it
  consistent in any new numbers.
- Light/dark theme support if feasible.
- Keep the access-key role-scoping intact and enforced everywhere.

## Testing and delivery
- `tests/test_smoke.py` has a starting smoke test for all five roles —
  extend it as you add features, and add an `AppTest`-based UI smoke
  test per role if time allows.
- Confirm `python -m streamlit run app.py` starts cleanly after changes.
- Update `README.md` with: what changed vs. this scaffold, run
  instructions, the five demo access keys, test results, and honest
  limitations.

## Honest limitations to keep stating
- All data is synthetic; precision/recall numbers reflect performance
  against planted problems in the simulator, not real-store accuracy.
- Real production RFID systems should key product data to the EPC in a
  database rather than writing name/price onto the tag itself.

## Stretch goals (if time allows, from the original "full build" vision)
- Scale synthetic data to 90 days / 300+ SKUs / all 10 stores with
  festival surges and ~4% POS mismatches.
- Sankey zone-flow diagram and floor heatmap.
- What-if layout simulator (move a product between zones, estimate
  impact).
- SME ROI/payback calculator.
- WhatsApp/Telegram alert webhook stub.
- Unique hashed access keys instead of the plaintext demo keys above.
