from __future__ import annotations
import plotly.graph_objects as go
import streamlit as st
from src.ui import apply_visitor_theme

try:
    from src.ui import style_plotly_figure
except ImportError:  # Keep these pages usable if an older cached module is loaded.
    def style_plotly_figure(fig, *, height: int = 390):
        fig.update_layout(height=height, template="plotly_white")
        return fig
from src.catalog import DESTINATIONS
from src.scenarios import project_destination

st.set_page_config(page_title="Growth Scenario Planner | Horizon",page_icon=None,layout="wide")
apply_visitor_theme()
st.title("Destination growth scenario planner")
st.write("Compare an illustrative baseline with a strategy-led scenario. Inputs are assumptions, not official visitor forecasts.")
name=st.selectbox("Destination",list(DESTINATIONS))
a,b,c=st.columns(3)
with a: visitors=st.number_input("Annual visitors (assumption)",1000,20000000,100000,step=5000)
with b: spend=st.number_input("Spend per visitor (PKR assumption)",500,1000000,15000,step=500)
with c: local=st.slider("Local value retention assumption (%)",0,100,45)
x,y,z=st.columns(3)
with x: baseline=st.slider("Baseline annual growth (%)",0.0,12.0,2.0,0.5)
with y: uplift=st.slider("Strategy uplift at full execution (%)",0.0,15.0,4.0,0.5)
with z: execution=st.slider("Execution level (%)",0,100,65,5)
years=st.select_slider("Projection horizon",options=list(range(3,11)),value=5)
df=project_destination(int(visitors),float(spend),float(baseline),float(uplift),int(execution),int(local),int(years))
last=df.iloc[-1]
p,q,r=st.columns(3)
p.metric(f"Year {years} strategy visitors",f'{int(last["Strategy visitors"]):,}')
q.metric(f"Year {years} strategy visitor spend",f'PKR {last["Strategy visitor spend (PKR)"]:,.0f}')
r.metric("Illustrative local value retained",f'PKR {last["Illustrative local value retained (PKR)"]:,.0f}')
fig=go.Figure()
fig.add_trace(go.Scatter(x=df["Year"],y=df["Strategy visitors"],mode="lines",name="Strategy area",line=dict(width=0),fill="tozeroy",fillcolor="rgba(199,163,91,.16)",hoverinfo="skip",showlegend=False))
fig.add_trace(go.Scatter(x=df["Year"],y=df["Baseline visitors"],mode="lines+markers",name="Baseline",line=dict(color="#55B99A",width=3,dash="dot"),marker=dict(size=8,color="#55B99A",line=dict(color="#F7F3E8",width=1.2)),hovertemplate="Year %{x}<br>Baseline %{y:,.0f} visitors<extra></extra>"))
fig.add_trace(go.Scatter(x=df["Year"],y=df["Strategy visitors"],mode="lines+markers",name="Strategy scenario",line=dict(color="#D8B66E",width=4),marker=dict(size=10,color="#D8B66E",line=dict(color="#F7F3E8",width=1.4)),hovertemplate="Year %{x}<br>Strategy %{y:,.0f} visitors<extra></extra>"))
fig.update_layout(xaxis_title="Year",yaxis_title="Visitors",hovermode="x unified")
st.plotly_chart(style_plotly_figure(fig,height=430),use_container_width=True)
st.dataframe(df,use_container_width=True,hide_index=True)
st.warning("The model compounds user-entered growth assumptions. It is not a forecast, observed growth or an investment valuation. Capacity, seasonality, price inflation, leakage, environmental limits and statistical uncertainty are not yet modelled.")
