from __future__ import annotations
import pandas as pd
import plotly.express as px
import streamlit as st
from src.finance import simulate_project
from src.ui import apply_intelligence_theme

st.set_page_config(page_title="Investment Studio | VoyagePK", layout="wide")
apply_intelligence_theme()
st.title("Tourism investment & risk studio")
st.write("Model a small accommodation project in a Northern Areas or cultural destination. Inputs are assumptions; outputs are scenario distributions, not forecasts or investment advice.")
st.warning("No authenticated real-time PTDC or Statista feed is connected. Do not treat any input below as sourced macroeconomic data. Add licensed datasets and citations before using this for a live investment decision.")
dest = st.selectbox("Illustrative location", ["Hunza Valley", "Skardu", "Naran–Kaghan", "Lahore", "Multan", "Islamabad"])
a, b, c = st.columns(3)
rooms = a.number_input("Rooms", 1, 500, 20)
adr = b.number_input("Average daily room rate (PKR)", 500, 1000000, 12000, 500)
occupancy = c.slider("Stabilised occupancy (%)", 5, 95, 40)
d, e, f = st.columns(3)
fixed_cost = d.number_input("Annual operating costs (PKR)", 0, 1000000000, 35000000, 500000)
capex = e.number_input("Initial capital expenditure (PKR)", 100000, 5000000000, 80000000, 1000000)
discount = f.slider("Discount rate (%)", 0, 40, 15)
years = st.slider("Projection horizon (years)", 1, 20, 10)
if st.button("Run Monte Carlo simulation", type="primary"):
    try:
        result = simulate_project(int(rooms), float(adr), float(occupancy), float(fixed_cost),
                                  float(capex), years=years, discount_rate_pct=float(discount))
        x, y, z = st.columns(3)
        x.metric("P50 project NPV", f"PKR {result['npv_p50']:,.0f}")
        y.metric("P10–P90 NPV range", f"{result['npv_p10']:,.0f} to {result['npv_p90']:,.0f}")
        z.metric("Probability of positive NPV", f"{result['positive_npv_probability']:.1f}%")
        st.metric("Median cumulative ROI proxy", f"{result['roi_p50_pct']:.1f}%")
        frame = pd.DataFrame({"Year": list(range(1, years + 1)),
                              "Median annual project cash flow (PKR)": result["annual_median_cashflow"]})
        st.plotly_chart(px.line(frame, x="Year", y="Median annual project cash flow (PKR)",
                                markers=True, title=f"{dest}: median annual cash-flow path"),
                        use_container_width=True)
        with st.expander("Simulation assumptions and methodology"):
            st.json(result["assumptions"])
            st.write(f"{result['simulations']:,} simulations · deterministic seed 42 · "
                     "P10/P50/P90 are simulated percentiles, not confidence intervals.")
            st.write("NPV discounts annual operating cash flow and deducts simulated initial capex. Cash flow deducts a 3% room-revenue replacement-reserve proxy. Excludes debt service, tax, depreciation, working capital, non-room revenue, terminal value, construction phasing and seasonality.")
    except ValueError as exc:
        st.error(str(exc))
st.markdown("### Data provenance required before investment use")
st.write("- PTDC: source and publication date must be recorded for any tourism statistics imported.")
st.write("- Statista: use only data available under an appropriate licence; record metric definition, geography, vintage and extraction date.")
st.write("- Local market: validate ADR, occupancy, seasonality, payroll, utilities, construction costs, tax and transport access with primary evidence.")
st.write("- Scenario outputs are sensitive to assumptions. A Monte Carlo simulation does not make weak inputs reliable.")
