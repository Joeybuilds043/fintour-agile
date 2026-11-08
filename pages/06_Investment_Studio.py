from __future__ import annotations
import pandas as pd
import plotly.express as px
import streamlit as st
from src.finance import simulate_project
from src.ui import apply_visitor_theme

try:
    from src.ui import style_plotly_figure
except ImportError:  # Keep these pages usable if an older cached module is loaded.
    def style_plotly_figure(fig, *, height: int = 390):
        fig.update_layout(height=height, template="plotly_white")
        return fig

st.set_page_config(page_title="Investment Studio | VoyagePK", layout="wide")
apply_visitor_theme()
st.title("Tourism investment & risk studio")
st.write("Model a small accommodation project in a Northern Areas or cultural destination. Inputs are assumptions; outputs are scenario distributions, not forecasts or investment advice.")
st.info("This is an assumption-led scenario model. Enter locally validated rates, occupancy, costs and capital expenditure; do not interpret model outputs as observed market data.")
with st.expander("Research sources for market validation"):
    st.markdown("- [PTDC publications and tourism context](https://tourism.gov.pk/publications.html)")
    st.markdown("- [Government of Gilgit-Baltistan tourist inflows dashboard](https://e-tourism.visitgilgitbaltistan.gov.pk/plan-trip/tourist-inflows)")
    st.markdown("- [Pakistan Bureau of Statistics](https://www.pbs.gov.pk/)")
    st.markdown("- [Statista — Pakistan tourism market](https://www.statista.com/outlook/mmo/travel-tourism/pakistan)")
    st.caption("Record metric definition, geography, observation period, extraction date and licence for every imported data point. Google Search grounding supports research discovery, not a substitute for licensed primary data.")
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
        cashflow_fig = px.area(frame, x="Year", y="Median annual project cash flow (PKR)",
                               markers=True, title=f"{dest}: median annual cash-flow path")
        cashflow_fig.update_traces(line=dict(color="#D8B66E", width=3.5),
                                   fillcolor="rgba(48,145,103,.28)",
                                   marker=dict(size=9, color="#55B99A", line=dict(color="#F7F3E8", width=1.4)),
                                   hovertemplate="Year %{x}<br>Median cash flow PKR %{y:,.0f}<extra></extra>")
        st.plotly_chart(style_plotly_figure(cashflow_fig,height=410),use_container_width=True)
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
