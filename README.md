# VoyagePK — Pakistan Unbound

**Pakistan Digital Destination Discovery & Tourism Intelligence Prototype**

VoyagePK connects an editorial, experience-led visitor discovery journey with an emerging tourism intelligence and investment workspace.

## Run locally
Install requirements, then run: streamlit run app.py

## Workspaces
Home; 60+ destination discovery collection; destination field guides; regional atlas with detailed attraction records and festival calendar; trip planner; interactive Pakistan travel atlas; destination intelligence; investment studio; data observatory; AI travel concierge; AI strategy advisor; growth scenario planner.

## Optional AI configuration
The visitor interface uses an editorial travel-magazine design system; tourism intelligence and investment pages use a separate restrained analytical design system. The travel atlas uses a custom PyDeck map with CARTO basemap styling and thematic destination markers.

The AI workspaces use Groq's OpenAI-compatible Responses API through the OpenAI Python SDK. Add `GROQ_API_KEY` to Streamlit Community Cloud → App settings → Secrets. Visitors never enter API keys. The default model is `llama-3.1-8b-instant`; it can be changed with `VOYAGEPK_GROQ_MODEL`. Never commit a real key. The selected Llama model does not provide built-in live web research in this app, so current road, weather, permit, safety and pricing details must be verified through official sources.

Example Streamlit Secrets entry:

```toml
GROQ_API_KEY = "replace_with_your_groq_api_key"
```

Groq API access is subject to Groq's current model-specific limits and pricing and requires available API credits. Usage limits and pricing depend on the model and your Groq account tier. Set a budget and usage limits in the Groq Console before sharing the app. Do not submit confidential visitor or business information.

## Data integrity
Weather forecasts are retrieved from Open-Meteo and cached temporarily. Destination photographs are retrieved from Wikimedia Commons, relevance-ranked using file titles and landscape resolution, gently colour/contrast corrected for display, and shown with file-level creator, licence and source attribution where metadata is available. Automated matching is not a substitute for manual visual and licence review. The 30+ destination clusters are an expanding editorial collection, not an exhaustive official gazetteer or ranking. Destination editorial content and approximate cluster coordinates require local review. No hotel availability, live road safety, nationwide verified occupancy or visitor spending is claimed. Financial inputs are illustrative and user-editable. The Gilgit-Baltistan dataset is a static partial-year snapshot from the earlier project and must not be annualised.

## Sources
- Groq Responses API: https://console.groq.com/docs/responses-api
- Open-Meteo: https://open-meteo.com/en/docs
- Wikimedia Commons API: https://commons.wikimedia.org/wiki/Commons:API
- Gilgit-Baltistan tourist inflows: https://e-tourism.visitgilgitbaltistan.gov.pk/plan-trip/tourist-inflows
- Pakistan Tourism Development Corporation: https://tourism.gov.pk/publications.html

See docs for the product blueprint, strategy and innovation framework, data dictionary, architecture, source register, evaluation plan, impact framework, governance and roadmap.

## Deployment
Streamlit Community Cloud can deploy this repository with `app.py` as the entry point. Review external provider terms and attribution requirements before commercial use.
