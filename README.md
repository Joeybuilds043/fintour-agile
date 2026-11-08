# Horizon Tourism

**Pakistan Digital Destination Discovery & Tourism Intelligence Prototype**

Horizon connects an editorial, experience-led visitor discovery journey with an emerging tourism intelligence and investment workspace.

## Run locally
Install requirements, then run: streamlit run app.py

## Workspaces
Home; 30+ destination discovery collection; destination field guides; trip planner; interactive Pakistan travel atlas; destination intelligence; investment studio; data observatory; AI travel concierge; AI strategy advisor; growth scenario planner.

## Optional AI configuration
The visitor interface uses an editorial travel-magazine design system; tourism intelligence and investment pages use a separate restrained analytical design system. The travel atlas uses a custom PyDeck map with CARTO basemap styling and thematic destination markers.\n\nThe AI workspaces use Google's Gemini Developer API through a shared server-side service. Add `GEMINI_API_KEY` to Streamlit Community Cloud Secrets or a local `.streamlit/secrets.toml` file. The default model is `gemini-3.6-flash`; it can be changed with the `HORIZON_GEMINI_MODEL` environment variable. Never commit a real API key. The visitor and industry workspaces remain usable without AI credentials.

Example Streamlit Secrets entry:

```toml
GEMINI_API_KEY = "replace_with_your_gemini_api_key"
```

The free tier has model-specific rate limits and Google may use free-tier submitted content to improve its products. Do not submit confidential visitor or business information. Check current quotas and terms in Google AI Studio before production use.

## Data integrity
Weather forecasts are retrieved from Open-Meteo and cached temporarily. Destination photographs are retrieved from Wikimedia Commons, relevance-ranked using file titles and landscape resolution, gently colour/contrast corrected for display, and shown with file-level creator, licence and source attribution where metadata is available. Automated matching is not a substitute for manual visual and licence review. The 30+ destination clusters are an expanding editorial collection, not an exhaustive official gazetteer or ranking. Destination editorial content and approximate cluster coordinates require local review. No hotel availability, live road safety, nationwide verified occupancy or visitor spending is claimed. Financial inputs are illustrative and user-editable. The Gilgit-Baltistan dataset is a static partial-year snapshot from the earlier project and must not be annualised.

## Sources
- Gemini API: https://ai.google.dev/gemini-api/docs
- Open-Meteo: https://open-meteo.com/en/docs
- Wikimedia Commons API: https://commons.wikimedia.org/wiki/Commons:API
- Gilgit-Baltistan tourist inflows: https://e-tourism.visitgilgitbaltistan.gov.pk/plan-trip/tourist-inflows
- Pakistan Tourism Development Corporation: https://tourism.gov.pk/publications.html

See docs for the product blueprint, strategy and innovation framework, data dictionary, architecture, source register, evaluation plan, impact framework, governance and roadmap.

## Deployment
Streamlit Community Cloud can deploy this repository with `app.py` as the entry point. Review external provider terms and attribution requirements before commercial use.
