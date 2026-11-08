# Horizon Tourism — Destination Growth & Investment Studio

A Streamlit decision-support application for destination strategy, business-model design, innovation planning and transparent growth scenarios across ten destinations in Pakistan.

## Workspaces
- Destination portfolio: destination-specific diagnosis, initiatives, innovation concepts and KPIs.
- Growth scenario planner: editable visitor, spend, execution and growth assumptions; compares baseline and strategy scenarios over 3–10 years.
- AI strategy advisor: destination-specific business and implementation plans through xAI.
- Market evidence: official Gilgit-Baltistan monthly domestic inflows for January–June 2026.

## Data limitations
The growth planner is a scenario model, not a forecast. Default visitor counts, average spend and growth rates are illustrative assumptions and must be replaced with verified local data before investment decisions. The GB panel is partial-year data and must not be annualized. The app does not claim projected growth has already occurred.

## Run locally
Install requirements, then run: streamlit run app.py

## Configure xAI
Create .streamlit/secrets.toml locally or configure the same secret in Streamlit Community Cloud:
GROK_API_KEY = "your_xai_api_key"

Never commit a real API key. AI is optional; the other workspaces work without it.

## Sources
- https://e-tourism.visitgilgitbaltistan.gov.pk/plan-trip/tourist-inflows
- https://tourism.gov.pk/publications.html

## Deployment
Deploy this repository on Streamlit Community Cloud with app.py as the main file. Add GROK_API_KEY under the app's Secrets settings if AI functionality is required.
