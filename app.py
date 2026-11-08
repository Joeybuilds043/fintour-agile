from __future__ import annotations

from typing import Any
import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st

st.set_page_config(page_title="Horizon Tourism | Destination Growth Studio", page_icon="H", layout="wide", initial_sidebar_state="expanded")
APP_NAME = "Horizon Tourism"
XAI_URL = "https://api.x.ai/v1/chat/completions"
XAI_MODEL = "latest"

DESTINATIONS: dict[str, dict[str, Any]] = {
    "Hunza Valley": {"region":"Gilgit-Baltistan","type":"Mountain / culture","lat":36.3167,"lon":74.6500,"season":"April–October; shoulder-season potential","baseline_visitors":180000,"avg_spend":26000,"local_capture":48,"opportunity":7.0,"risk":"Road disruption, water stress, waste pressure and seasonal concentration.","strategy":"Increase visitor value and extend the season rather than maximizing peak-season arrivals.","initiatives":["Village-owned homestay and experience network with common quality standards","Spring and autumn culture, food and orchard itineraries to spread demand","Digital booking inventory for guides, transport, stays and community experiences","Waste-return incentives, refill stations and local-produce procurement agreements"],"innovation":"A destination marketplace bundling verified local experiences, transport and stays with transparent community revenue sharing.","kpis":"Average spend per visitor, shoulder-season occupancy, local procurement share, waste collected per visitor."},
    "Skardu": {"region":"Gilgit-Baltistan","type":"Adventure / mountain","lat":35.2971,"lon":75.6333,"season":"May–October; winter products need careful readiness","baseline_visitors":220000,"avg_spend":34000,"local_capture":42,"opportunity":8.0,"risk":"Access disruption, emergency-response gaps, fragile landscapes and high peak-season loads.","strategy":"Build a higher-yield, safer adventure destination with longer itineraries and stronger local supplier capacity.","initiatives":["Integrated trekking, lake and heritage passes with licensed guide allocation","Porter welfare, guide certification, rescue coordination and safety protocols","Pre-booked transport and visitor-flow management for high-pressure sites","Local food, equipment rental and repair partnerships that retain visitor spend"],"innovation":"A digital adventure operations platform linking permits, weather alerts, verified guides, emergency contacts and responsible operator capacity.","kpis":"Average trip length, spend per visitor, licensed-guide participation, incident response time, local supplier share."},
    "Naran–Kaghan": {"region":"Khyber Pakhtunkhwa","type":"Alpine valley / road trip","lat":34.9090,"lon":73.6500,"season":"May–September","baseline_visitors":450000,"avg_spend":14500,"local_capture":38,"opportunity":6.5,"risk":"Traffic congestion, waste accumulation, road closures and unplanned construction.","strategy":"Manage peak demand through mobility, site capacity and a more organized visitor economy.","initiatives":["Park-and-ride hubs with scheduled electric or low-emission shuttles","Timed parking and digital occupancy information for high-demand access points","Trail, lake and village circuits that distribute spending beyond the main bazaar","Operator standards for waste handling, water use and visitor safety"],"innovation":"A live mobility and crowd-management layer using parking reservations, shuttle dispatch and visitor information.","kpis":"Average road delay, shuttle share, visitor spend outside the main hub, waste collection coverage."},
    "Swat Valley": {"region":"Khyber Pakhtunkhwa","type":"Nature / heritage / family","lat":35.2220,"lon":72.4258,"season":"March–November","baseline_visitors":520000,"avg_spend":12500,"local_capture":44,"opportunity":7.0,"risk":"River safety, flood exposure, uneven service quality and concentration around a few resorts.","strategy":"Position Swat as a year-round valley destination connecting nature, heritage, food and community experiences.","initiatives":["Curated heritage, archaeology, craft and food routes with local guides","Quality accreditation for family stays, restaurants and adventure operators","River-safety information, marked access zones and emergency response partnerships","Community-led farm, craft and cultural experiences outside peak resort clusters"],"innovation":"A verified valley pass and itinerary planner linking attractions, transport, stays and local experiences.","kpis":"Non-peak occupancy, visitor satisfaction, certified business share, average length of stay."},
    "Murree": {"region":"Punjab","type":"Hill station / short break","lat":33.9070,"lon":73.3943,"season":"Year-round; strongest holiday and summer peaks","baseline_visitors":1600000,"avg_spend":10500,"local_capture":52,"opportunity":5.5,"risk":"Severe peak congestion, parking constraints, waste, service inflation and weather disruption.","strategy":"Shift from volume-led day trips toward managed access, longer stays and higher-quality visitor services.","initiatives":["Pre-booked parking and park-and-ride with clear peak-day access information","Dispersal itineraries connecting Patriata, nearby villages and nature trails","Transparent hotel and restaurant standards with digital complaint resolution","Off-peak events and packaged two-night stays to improve weekday utilization"],"innovation":"A demand-management system combining parking reservations, shuttle capacity and visitor alerts.","kpis":"Peak travel time, average length of stay, weekday occupancy, visitor complaints per 1,000 trips."},
    "Neelum Valley": {"region":"Azad Jammu & Kashmir","type":"River / mountain / eco-tourism","lat":34.5850,"lon":73.9070,"season":"April–October","baseline_visitors":260000,"avg_spend":16000,"local_capture":50,"opportunity":7.5,"risk":"Road access vulnerability, landslides, river hazards and limited waste services.","strategy":"Develop low-impact community tourism with reliable safety information and distributed local enterprise.","initiatives":["Community-owned accommodation clusters with minimum environmental standards","River and trail safety protocols, trained local responders and clear hazard notices","Local guide, transport and food directories with bookable itineraries","Visitor contributions ring-fenced for waste, trail maintenance and conservation"],"innovation":"A community destination cooperative coordinating bookings, standards and shared infrastructure investment.","kpis":"Community revenue share, certified stays, safety incidents, waste recovery rate."},
    "Chitral & Kalash Valleys": {"region":"Khyber Pakhtunkhwa","type":"Culture / mountain / heritage","lat":35.8510,"lon":71.7864,"season":"May–October; festival periods require advance planning","baseline_visitors":135000,"avg_spend":22000,"local_capture":58,"opportunity":8.0,"risk":"Cultural commodification, access constraints, fragile heritage and uneven local benefit.","strategy":"Protect cultural integrity while increasing locally retained value through small-group, experience-led tourism.","initiatives":["Community-approved visitor protocols and consent-led cultural interpretation","Small-group guided heritage, craft, food and landscape experiences","Festival capacity plans and advance accommodation coordination","Local artisan marketplace with fair pricing and transparent commissions"],"innovation":"A community-governed cultural tourism charter and booking network with local control over experiences and capacity.","kpis":"Local revenue retention, community satisfaction, small-group participation, heritage compliance."},
    "Lahore": {"region":"Punjab","type":"Urban / food / heritage","lat":31.5204,"lon":74.3587,"season":"October–March; indoor and evening products year-round","baseline_visitors":1200000,"avg_spend":18000,"local_capture":62,"opportunity":8.0,"risk":"Fragmented visitor information, congestion at heritage cores and inconsistent interpretation.","strategy":"Convert Lahore's heritage and food assets into bookable, higher-value multi-day visitor journeys.","initiatives":["Integrated heritage, food and craft passes across the Walled City and major museums","Evening walking tours and curated food trails with licensed local guides","Multilingual interpretation, digital ticketing and accessible visitor information","Hotel, restaurant and attraction bundles that encourage longer stays"],"innovation":"A city tourism pass with timed entry, audio interpretation, route discovery and partner revenue settlement.","kpis":"Attraction conversion, spend per visitor, average stay, digital pass usage, local guide earnings."},
    "Taxila": {"region":"Punjab","type":"Archaeology / education / heritage","lat":33.7460,"lon":72.8390,"season":"October–April; school and university calendar opportunities","baseline_visitors":90000,"avg_spend":9500,"local_capture":45,"opportunity":7.0,"risk":"Low dwell time, limited interpretation, conservation funding and fragmented site experiences.","strategy":"Build a connected heritage-learning destination that increases dwell time without compromising conservation.","initiatives":["Combined museum and archaeological-site passes with trained interpretation","University, school and specialist research itineraries","Digital storytelling and site interpretation in multiple languages","Local craft, food and guide partnerships with a conservation contribution"],"innovation":"A digital heritage layer with audio guides, learning trails, timed visits and conservation-linked ticketing.","kpis":"Average dwell time, guided-tour uptake, education-group visits, conservation contribution."},
    "Gwadar & Hingol Coast": {"region":"Balochistan","type":"Coastal / desert / nature","lat":25.1260,"lon":62.3220,"season":"October–March","baseline_visitors":80000,"avg_spend":24000,"local_capture":46,"opportunity":8.5,"risk":"Remote access, water scarcity, environmental sensitivity, safety and limited visitor services.","strategy":"Create a carefully managed coastal circuit with local operators, safety standards and environmental safeguards.","initiatives":["Small-group coastal and desert circuits with licensed local operators","Water-aware accommodation and waste-backhaul requirements","Boat, road and weather safety protocols with verified operator information","Local seafood, crafts and community experiences integrated into itineraries"],"innovation":"A low-impact coastal circuit marketplace linking verified operators, safety updates and conservation fees.","kpis":"Local operator earnings, water use per guest, safety compliance, waste removed, visitor spend."},
}

GB_MONTHS = ["Jan","Feb","Mar","Apr","May","Jun"]
GB_2026 = {
    "Skardu":[1890,4072,7412,20312,25460,38542],"Gilgit":[1762,3054,4581,16521,19520,31290],
    "Astore":[860,912,1027,13266,15690,32310],"Hunza":[1840,3821,5780,18241,20313,36980],
    "Diamer":[10275,12560,13675,18932,19870,51732],"Nagar":[618,924,1036,1027,1183,1178],
    "Ghanche":[109,245,374,1269,1494,2002],"Ghizer":[822,923,1287,752,1263,2364],
    "Shigar":[203,378,402,2001,2965,3652],"Kharmang":[21,46,51,328,570,630],
}

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');
:root{--bg:#0b1220;--panel:#111d30;--line:#263750;--ink:#edf3fb;--muted:#98a9bf;--blue:#62b5e5}
html,body,[data-testid="stAppViewContainer"]{background:var(--bg);color:var(--ink);font-family:'DM Sans',sans-serif}
[data-testid="stHeader"]{background:transparent}[data-testid="stSidebar"]{background:#0d1728;border-right:1px solid var(--line)}
.block-container{max-width:1500px;padding-top:2rem;padding-bottom:3rem}
h1,h2,h3,h4{color:var(--ink)!important;letter-spacing:-.5px}p,label{color:var(--muted)}
.hero{font-size:34px;font-weight:800;letter-spacing:-1.5px;color:var(--ink);margin:2px 0 4px}
.subhero{font-size:13px;color:var(--muted);line-height:1.7}.eyebrow{font-size:10px;letter-spacing:1.8px;text-transform:uppercase;font-weight:800;color:var(--blue);margin-bottom:7px}
.panel{background:linear-gradient(145deg,#16243a,#111d30);border:1px solid var(--line);border-radius:14px;padding:18px 20px;margin-bottom:12px}
.kpi-label{font-size:10px;color:var(--muted);text-transform:uppercase;letter-spacing:1px;font-weight:700}.kpi-value{font-size:25px;font-weight:800;color:var(--ink);margin-top:7px}.kpi-note{font-size:11px;color:var(--muted);margin-top:3px}
.tag{display:inline-block;border:1px solid #38506d;border-radius:20px;padding:4px 9px;color:#b9d9ef;font-size:10px;margin:3px 4px 3px 0}
div[data-testid="stButton"]>button{background:#172a42;color:#e9f2fb;border:1px solid #344b68;border-radius:9px;min-height:40px;font-weight:600}
div[data-testid="stButton"]>button:hover{background:#203b59;border-color:var(--blue);color:white}
[data-testid="stMetric"]{background:#111d30;border:1px solid var(--line);border-radius:12px;padding:13px}
[data-testid="stMetricLabel"]{color:var(--muted)!important}[data-testid="stMetricValue"]{color:var(--ink)!important}
hr{border-color:var(--line)}footer{visibility:hidden}
@media(max-width:768px){.hero{font-size:27px}.block-container{padding-top:1rem}}
</style>
""", unsafe_allow_html=True)


def money_pkr(value: float) -> str:
    if value >= 1_000_000_000:
        return f"PKR {value / 1_000_000_000:,.2f}bn"
    if value >= 1_000_000:
        return f"PKR {value / 1_000_000:,.1f}m"
    return f"PKR {value:,.0f}"


def scenario_projection(visitors: int, spend: int, base_growth: float, strategy_uplift: float, execution: int, local_capture: int, years: int = 5) -> pd.DataFrame:
    """Illustrative scenario model, not an observed forecast."""
    rows = []
    for year in range(years + 1):
        baseline = visitors * ((1 + base_growth / 100) ** year)
        strategy = visitors * ((1 + (base_growth + strategy_uplift * execution / 100) / 100) ** year)
        rows.append({
            "Year": year, "Baseline visitors": round(baseline), "Strategy visitors": round(strategy),
            "Baseline spend (PKR bn)": baseline * spend / 1_000_000_000,
            "Strategy spend (PKR bn)": strategy * spend / 1_000_000_000,
            "Local value retained (PKR bn)": strategy * spend * local_capture / 100 / 1_000_000_000,
        })
    return pd.DataFrame(rows)


def make_projection_chart(df: pd.DataFrame, metric: str, title: str) -> go.Figure:
    is_visitors = metric == "visitors"
    columns = [("Baseline visitors","Baseline / no new programme"),("Strategy visitors","With strategy programme")] if is_visitors else [("Baseline spend (PKR bn)","Baseline / no new programme"),("Strategy spend (PKR bn)","With strategy programme")]
    fig = go.Figure()
    for column,label in columns:
        fig.add_trace(go.Scatter(x=df["Year"],y=df[column],mode="lines+markers",name=label,line=dict(width=3),marker=dict(size=7)))
    fig.update_layout(title=dict(text=title,font=dict(size=15)),height=340,margin=dict(l=12,r=12,t=48,b=12),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font=dict(color="#dce7f4",family="DM Sans"),xaxis=dict(title="Year from programme start",gridcolor="#263750",dtick=1),yaxis=dict(gridcolor="#263750",zeroline=False),legend=dict(orientation="h",y=-0.23),hovermode="x unified")
    return fig


def get_api_key() -> str:
    try:
        key = st.secrets.get("GROK_API_KEY", "")
        if key:
            return str(key).strip()
    except Exception:
        pass
    return st.session_state.get("temporary_api_key", "")


def ask_grok(api_key: str, destination: str, question: str, context: str) -> str:
    system = (
        "You are Horizon Tourism's senior tourism investment and destination-management advisor. "
        "Advise destination management organizations, operators, investors and local government. "
        "Be commercially rigorous and specific. Prioritize local value capture, carrying capacity, service quality, "
        "seasonality, climate resilience, community consent, conservation and measurable unit economics. "
        "Never invent visitor statistics, market sizes, government approvals or research citations. "
        "Clearly label assumptions and distinguish recommendations from verified facts. State what data is missing. "
        "Use headings: Diagnosis, Strategic moves, Business model, 12-month execution, KPIs, Risks and investment logic."
    )
    messages = [
        {"role":"system","content":system},
        {"role":"user","content":f"Destination: {destination}\nContext: {context}\nRequest: {question}\nQuantify only where assumptions are explicit."},
    ]
    response = requests.post(XAI_URL,headers={"Authorization":f"Bearer {api_key}","Content-Type":"application/json"},json={"model":XAI_MODEL,"messages":messages,"temperature":0.2,"max_tokens":1600},timeout=(10,90))
    if response.status_code != 200:
        raise RuntimeError(f"xAI API error {response.status_code}: {response.text[:350].replace(chr(10),' ')}")
    choices = response.json().get("choices") or []
    answer = choices[0].get("message",{}).get("content") if choices else None
    if not isinstance(answer,str) or not answer.strip():
        raise RuntimeError("The AI provider returned an empty answer.")
    return answer.strip()


def style_chart(fig: go.Figure, height: int = 340) -> go.Figure:
    fig.update_layout(height=height,margin=dict(l=10,r=10,t=45,b=10),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font=dict(color="#dce7f4",family="DM Sans"),xaxis=dict(gridcolor="#263750"),yaxis=dict(gridcolor="#263750"),legend=dict(orientation="h",y=-0.25))
    return fig


if "temporary_api_key" not in st.session_state:
    st.session_state.temporary_api_key = ""
if "last_advisor_result" not in st.session_state:
    st.session_state.last_advisor_result = ""

with st.sidebar:
    st.markdown('<div style="font-size:22px;font-weight:800;color:#eaf3fb">HORIZON</div><div style="font-size:10px;letter-spacing:1.7px;color:#8da6bf">TOURISM GROWTH STUDIO</div>',unsafe_allow_html=True)
    st.divider()
    workspace = st.radio("WORKSPACE",["Destination portfolio","Growth scenario planner","AI strategy advisor","Market evidence"])
    st.divider()
    st.caption("COVERAGE")
    st.markdown("**10 destinations**")
    st.caption("Pakistan · Destination strategy · Investment scenarios")
    st.divider()
    st.success("AI connection configured") if get_api_key() else st.warning("AI key not configured")
    with st.expander("Configure AI connection"):
        st.caption("Use Streamlit Secrets for deployment. A temporary key stays only in this session.")
        key_input = st.text_input("xAI API key",type="password",key="key_entry")
        if st.button("Save session key",use_container_width=True):
            if key_input.strip():
                st.session_state.temporary_api_key = key_input.strip()
                st.rerun()
            else:
                st.warning("Enter an API key first.")
    st.caption("Scenario outputs are illustrative, not forecasts.")

selected = st.session_state.get("selected_destination","Hunza Valley")
if selected not in DESTINATIONS:
    selected = "Hunza Valley"

st.markdown('<div class="eyebrow">PAKISTAN DESTINATION DEVELOPMENT</div>',unsafe_allow_html=True)
st.markdown('<div class="hero">Horizon Tourism</div>',unsafe_allow_html=True)
st.markdown('<div class="subhero">Destination Growth & Investment Studio · Turn tourism assets into resilient, locally valuable businesses.</div>',unsafe_allow_html=True)
st.write("")

if workspace == "Destination portfolio":
    st.markdown("### Destination portfolio")
    st.caption("Strategy-led view of ten priority destinations. Opportunity ratings are qualitative assessments, not official rankings.")
    chosen = st.selectbox("Select destination",list(DESTINATIONS),index=list(DESTINATIONS).index(selected))
    st.session_state.selected_destination = chosen
    d = DESTINATIONS[chosen]
    cols = st.columns(4)
    cards = [("Region",d["region"],d["type"]),("Illustrative annual visitors",f'{d["baseline_visitors"]:,}',"Editable planning assumption"),("Average visitor spend",money_pkr(d["avg_spend"]),"Illustrative PKR per trip"),("Opportunity score",f'{d["opportunity"]:.1f}/10',"Qualitative prioritization")]
    for col,(label,value,note) in zip(cols,cards):
        with col:
            st.markdown(f'<div class="panel"><div class="kpi-label">{label}</div><div class="kpi-value" style="font-size:19px">{value}</div><div class="kpi-note">{note}</div></div>',unsafe_allow_html=True)
    left,right = st.columns([1.05,1.2],gap="large")
    with left:
        st.markdown("#### Strategic diagnosis")
        st.write(d["risk"])
        st.markdown("#### Recommended strategic direction")
        st.write(d["strategy"])
        st.markdown("#### Best-fit innovation")
        st.info(d["innovation"])
    with right:
        st.markdown("#### Business strategy & initiatives")
        for i,item in enumerate(d["initiatives"],1):
            st.markdown(f"**{i}.** {item}")
        st.markdown("#### Performance scorecard")
        st.write(d["kpis"])
        st.markdown(f'<span class="tag">{d["season"]}</span><span class="tag">{d["region"]}</span>',unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("#### Pakistan destination map")
    mdf = pd.DataFrame([{"Destination":name,"Region":v["region"],"lat":v["lat"],"lon":v["lon"]} for name,v in DESTINATIONS.items()])
    map_fig = go.Figure(go.Scattermap(lat=mdf["lat"],lon=mdf["lon"],mode="markers+text",text=mdf["Destination"],textposition="top right",marker=dict(size=12,color="#62b5e5"),customdata=mdf[["Region"]],hovertemplate="<b>%{text}</b><br>%{customdata[0]}<extra></extra>"))
    map_fig.update_layout(map=dict(style="carto-darkmatter",center=dict(lat=31.8,lon=72.8),zoom=4.4),height=490,margin=dict(l=0,r=0,t=0,b=0),paper_bgcolor="rgba(0,0,0,0)",font=dict(color="#dce7f4"))
    st.plotly_chart(map_fig,use_container_width=True,config={"displayModeBar":False})

elif workspace == "Growth scenario planner":
    st.markdown("### Growth scenario planner")
    st.caption("Compare a baseline trajectory with a strategy-led scenario. Starting values and growth rates are editable assumptions.")
    chosen = st.selectbox("Destination",list(DESTINATIONS),index=list(DESTINATIONS).index(selected),key="planner_destination")
    st.session_state.selected_destination = chosen
    d = DESTINATIONS[chosen]
    a,b,c = st.columns(3)
    with a:
        visitors = st.number_input("Current annual visitors (assumption)",min_value=1000,max_value=20000000,value=int(d["baseline_visitors"]),step=5000)
    with b:
        spend = st.number_input("Average spend per visitor (PKR)",min_value=500,max_value=1000000,value=int(d["avg_spend"]),step=500)
    with c:
        local_capture = st.slider("Local value retained (%)",10,90,int(d["local_capture"]))
    x,y,z = st.columns(3)
    with x:
        base_growth = st.slider("Baseline annual growth (%)",0.0,12.0,2.0,0.5)
    with y:
        uplift = st.slider("Strategy growth uplift at full execution (%)",0.0,15.0,float(d["opportunity"]),0.5)
    with z:
        execution = st.slider("Strategy execution level (%)",0,100,70,5)
    years = st.select_slider("Projection horizon",options=[3,4,5,6,7,8,9,10],value=5)
    df = scenario_projection(int(visitors),int(spend),base_growth,uplift,execution,local_capture,years)
    end = df.iloc[-1]
    base_rev = float(end["Baseline spend (PKR bn)"])
    strategy_rev = float(end["Strategy spend (PKR bn)"])
    delta = (strategy_rev/base_rev-1)*100 if base_rev else 0
    k1,k2,k3,k4 = st.columns(4)
    k1.metric(f"Year {years} visitors",f'{int(end["Strategy visitors"]):,}')
    k2.metric(f"Year {years} visitor spend",money_pkr(strategy_rev*1_000_000_000),f"{delta:+.1f}% vs baseline")
    k3.metric("Local value retained",money_pkr(float(end["Local value retained (PKR bn)"])*1_000_000_000))
    k4.metric("Execution level",f"{execution}%")
    p1,p2 = st.columns(2)
    with p1:
        st.plotly_chart(make_projection_chart(df,"visitors","Visitor volume: baseline vs strategy"),use_container_width=True)
    with p2:
        st.plotly_chart(make_projection_chart(df,"spend","Estimated direct visitor spend (PKR bn)"),use_container_width=True)
    st.markdown("#### Scenario detail")
    st.dataframe(df.style.format({"Baseline visitors":"{:,.0f}","Strategy visitors":"{:,.0f}","Baseline spend (PKR bn)":"{:,.2f}","Strategy spend (PKR bn)":"{:,.2f}","Local value retained (PKR bn)":"{:,.2f}"}),use_container_width=True,hide_index=True)
    st.warning("These are scenario outputs from your inputs, not observed growth, official forecasts or guaranteed outcomes. Validate baseline visitors, spend, leakage and capacity before investment decisions.")

elif workspace == "AI strategy advisor":
    st.markdown("### AI strategy advisor")
    st.caption("Destination-specific business models, investment sequencing, innovation and implementation.")
    chosen = st.selectbox("Destination",list(DESTINATIONS),index=list(DESTINATIONS).index(selected),key="advisor_destination")
    st.session_state.selected_destination = chosen
    d = DESTINATIONS[chosen]
    context = f"Region: {d['region']}; type: {d['type']}; season: {d['season']}; visitor planning assumption: {d['baseline_visitors']:,}; spend assumption: PKR {d['avg_spend']:,}; local value capture assumption: {d['local_capture']}%. Risk: {d['risk']} Strategy: {d['strategy']} Initiatives: {'; '.join(d['initiatives'])} Innovation: {d['innovation']} KPIs: {d['kpis']}"
    with st.expander("Destination context sent to AI"):
        st.write(context)
    analysis_type = st.selectbox("Analysis type",["Build a 12-month destination business strategy","Design a commercially viable tourism business model","Prioritize investment opportunities and partnership structure","Create a digital innovation roadmap","Develop a sustainable visitor and carrying-capacity plan","Assess risks and implementation barriers"])
    question = st.text_area("Specific requirements",placeholder="Example: Design a three-year business model for community-owned stays, including revenue streams, costs, partners and KPIs.",height=105)
    api_key = get_api_key()
    if not api_key:
        st.info("Configure your xAI API key in the sidebar. The other workspaces work without an API key.")
    if st.button("Generate destination strategy",type="primary",disabled=not bool(api_key),use_container_width=True):
        prompt = analysis_type if not question.strip() else f"{analysis_type}\nAdditional requirements: {question.strip()}"
        with st.spinner("Preparing destination-specific strategy..."):
            try:
                result = ask_grok(api_key,chosen,prompt,context)
                st.session_state.last_advisor_result = result
            except requests.exceptions.Timeout:
                st.error("The AI request timed out. Retry with a shorter question.")
            except requests.exceptions.RequestException as exc:
                st.error(f"Network error: {exc}")
            except (ValueError,RuntimeError) as exc:
                st.error(str(exc))
    if st.session_state.last_advisor_result:
        st.markdown("---")
        st.markdown("#### Strategy output")
        st.markdown(st.session_state.last_advisor_result)
        st.download_button("Download strategy brief",st.session_state.last_advisor_result,file_name=f"{chosen.lower().replace(' ','-')}-strategy-brief.md",mime="text/markdown")
        if st.button("Clear strategy output"):
            st.session_state.last_advisor_result = ""
            st.rerun()

elif workspace == "Market evidence":
    st.markdown("### Tourism market evidence")
    st.caption("Official Gilgit-Baltistan monthly domestic visitor inflows for January–June 2026. Partial-year data only.")
    district = st.selectbox("District",list(GB_2026),index=list(GB_2026).index("Skardu"))
    series = pd.DataFrame({"Month":GB_MONTHS,"Domestic visitors":GB_2026[district]})
    fig = go.Figure(go.Bar(x=series["Month"],y=series["Domestic visitors"],marker=dict(color="#62b5e5"),hovertemplate="%{x}: %{y:,} visitors<extra></extra>"))
    style_chart(fig,330)
    fig.update_layout(title=f"{district} · monthly domestic inflows (Jan–Jun 2026)",yaxis_title="Reported visitors")
    st.plotly_chart(fig,use_container_width=True)
    st.dataframe(series,use_container_width=True,hide_index=True)
    st.caption("Source: Government of Gilgit-Baltistan Tourism Department, Tourist Inflows dashboard. The published table lists monthly domestic flow through June 2026. No foreign-inflow records appeared in the retrieved table. Do not annualize this partial-year series.")
    st.markdown("[Open official GB tourist inflow dashboard](https://e-tourism.visitgilgitbaltistan.gov.pk/plan-trip/tourist-inflows)")
    st.markdown("[Open Pakistan Tourism Development Corporation publications](https://tourism.gov.pk/publications.html)")
    st.warning("Visitor, occupancy, spend and seasonality data are not consistently published for every province. The remaining destination baselines are editable assumptions, not official statistics.")

st.divider()
st.markdown('<div style="text-align:center;color:#71849c;font-size:10px;letter-spacing:1.2px">HORIZON TOURISM · DESTINATION GROWTH & INVESTMENT STUDIO</div>',unsafe_allow_html=True)
st.markdown('<div style="text-align:center;color:#53677f;font-size:10px;margin-top:4px">Decision-support tool · Validate scenario assumptions before capital allocation</div>',unsafe_allow_html=True)
