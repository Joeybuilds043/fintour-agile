from __future__ import annotations
import pandas as pd
import plotly.express as px
import streamlit as st
from src.ui import apply_visitor_theme

try:
    from src.ui import style_plotly_figure
except ImportError:  # Keep these pages usable if an older cached module is loaded.
    def style_plotly_figure(fig, *, height: int = 390):
        fig.update_layout(height=height, template="plotly_white")
        return fig

st.set_page_config(page_title="Destination Intelligence | VoyagePK",page_icon=None,layout="wide")
apply_visitor_theme()
st.title("Destination intelligence")
st.write("The industry workspace will turn fragmented tourism evidence into comparable destination insights. This release prioritises data transparency over unsupported national statistics.")
st.info("Verified, comparable occupancy, visitor-spending, transport-capacity and operating-cost data are not yet available consistently across the 39 curated destination clusters. Missing data is shown as a gap, not replaced with invented values.")
rows=[
("Visitor demand","Monthly domestic and international arrivals","Official statistics / validated counts","Not yet comparable nationally"),
("Accommodation","Room supply, occupancy, ADR and RevPAR","Tourism departments / verified properties","Partner data required"),
("Visitor economy","Average spend and length of stay","Visitor surveys / transaction research","Survey design required"),
("Transport access","Routes, journey times, seasonal disruption","Road authorities / transport operators","Live feeds vary by region"),
("Local value","Local procurement, employment and revenue retention","Business surveys / supply-chain analysis","Baseline study required"),
("Sustainability","Waste, water, ecological pressure and community views","Local authorities / field research","Destination-specific indicators required")]
st.dataframe(pd.DataFrame(rows,columns=["Theme","Measures","Preferred evidence","Current status"]),use_container_width=True,hide_index=True)
st.subheader("Pilot evidence: Gilgit-Baltistan domestic inflows")
st.write("The following is a static January–June 2026 snapshot retained from the earlier prototype. It is not a live feed, covers only part of the year and must not be annualised.")
data=pd.read_csv("data/gb_domestic_inflows_2026_h1.csv")
district=st.selectbox("District",sorted(data["District"].unique()),index=sorted(data["District"].unique()).index("Skardu"))
series=data[data["District"]==district]
fig=px.bar(series,x="Month",y="Domestic visitors",color="Domestic visitors",color_continuous_scale=["#0B3825","#278B63","#D7B96D"],text_auto=".2s",title=f"{district} — reported domestic visitor inflows, Jan–Jun 2026")
fig.update_traces(marker_line_color="rgba(255,255,255,.42)",marker_line_width=1.2,textposition="outside",textfont=dict(family="Manrope",size=11))
fig.update_layout(coloraxis_showscale=False)
st.plotly_chart(style_plotly_figure(fig,height=390),use_container_width=True)
st.dataframe(series,use_container_width=True,hide_index=True)
st.markdown("[Open the official Gilgit-Baltistan tourist inflows dashboard](https://e-tourism.visitgilgitbaltistan.gov.pk/plan-trip/tourist-inflows)")
st.markdown("[Pakistan Tourism Development Corporation publications](https://tourism.gov.pk/publications.html)")
st.caption("Source: Government of Gilgit-Baltistan Tourist Inflows dashboard as recorded in the earlier project snapshot. Recheck the source before reuse or publication.")
