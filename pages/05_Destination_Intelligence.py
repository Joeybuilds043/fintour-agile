from __future__ import annotations
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Destination Intelligence | Horizon",page_icon="📊",layout="wide")
st.title("Destination intelligence")
st.write("The industry workspace will turn fragmented tourism evidence into comparable destination insights. This release prioritises data transparency over unsupported national statistics.")
st.info("Verified, comparable occupancy, visitor-spending, transport-capacity and operating-cost data are not yet available for all ten destination clusters. Missing data is shown as a gap, not replaced with invented values.")
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
fig=px.bar(series,x="Month",y="Domestic visitors",title=f"{district} — reported domestic visitor inflows, Jan–Jun 2026")
fig.update_layout(height=350,margin=dict(l=10,r=10,t=45,b=10),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig,use_container_width=True)
st.dataframe(series,use_container_width=True,hide_index=True)
st.markdown("[Open the official Gilgit-Baltistan tourist inflows dashboard](https://e-tourism.visitgilgitbaltistan.gov.pk/plan-trip/tourist-inflows)")
st.markdown("[Pakistan Tourism Development Corporation publications](https://tourism.gov.pk/publications.html)")
st.caption("Source: Government of Gilgit-Baltistan Tourist Inflows dashboard as recorded in the earlier project snapshot. Recheck the source before reuse or publication.")
