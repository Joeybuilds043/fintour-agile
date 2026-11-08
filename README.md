# Horizon Tourism

**Pakistan Digital Destination Discovery & Tourism Intelligence Prototype**

Horizon connects an editorial, experience-led visitor discovery journey with an emerging tourism intelligence and investment workspace.

## Run locally
Install requirements, then run: streamlit run app.py

## Workspaces
Home; Discover Pakistan; destination guides; trip planner; explore map; destination intelligence; investment studio; data observatory; AI travel concierge; AI strategy advisor; growth scenario planner.

## Optional AI configuration
The AI workspaces use the xAI Chat Completions API. Add GROK_API_KEY to Streamlit Community Cloud Secrets or a local .streamlit/secrets.toml file. Never commit a real key. The visitor and industry workspaces remain usable without AI credentials.

## Data integrity
Weather forecasts are retrieved from Open-Meteo and cached temporarily. Destination photographs are retrieved from Wikimedia Commons and displayed with file-level creator, licence and source attribution where metadata is available. Destination editorial content and cluster coordinates require review. No hotel availability, live road safety, nationwide verified occupancy or visitor spending is claimed. Financial inputs are illustrative and user-editable. The Gilgit-Baltistan dataset is a static partial-year snapshot from the earlier project and must not be annualised.

## Sources
- Open-Meteo: https://open-meteo.com/en/docs
- Wikimedia Commons API: https://commons.wikimedia.org/wiki/Commons:API
- Gilgit-Baltistan tourist inflows: https://e-tourism.visitgilgitbaltistan.gov.pk/plan-trip/tourist-inflows
- Pakistan Tourism Development Corporation: https://tourism.gov.pk/publications.html

See docs for the product blueprint, strategy and innovation framework, data dictionary, architecture, source register, evaluation plan, impact framework, governance and roadmap.

## Deployment
Streamlit Community Cloud can deploy this repository with app.py as the entry point. Review external provider terms and attribution requirements before commercial use.
