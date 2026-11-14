# VoyagePK

VoyagePK is a tourism discovery prototype for Pakistan. It brings destination information, regional attractions, festivals, trip planning and early tourism strategy tools into one Streamlit app.

## Run the app

1. Install Python 3.11 or a compatible version.
2. Clone this repository.
3. Install the packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Start Streamlit:

   ```bash
   streamlit run app.py
   ```

## Main sections

- Regional Atlas: destination clusters, attraction records, festivals and image collections.
- Discover Pakistan: browse destinations and experiences.
- Trip Planner: prepare a draft itinerary.
- Destination Intelligence: review selected tourism data and research gaps.
- Investment Studio and Growth Scenario Planner: test example assumptions.
- AI Travel Concierge and AI Strategy Advisor: request AI-assisted suggestions when Groq is configured.
- About: app purpose, author and limits.

## Data and services

- Destination, festival and image records are stored in this repository.
- Open-Meteo provides weather data where enabled: https://open-meteo.com/en/docs
- Wikimedia Commons provides image metadata and media where available: https://commons.wikimedia.org/wiki/Commons:API
- Groq provides optional AI text generation: https://console.groq.com/docs
- Gilgit-Baltistan inflow snapshot source: https://e-tourism.visitgilgitbaltistan.gov.pk/plan-trip/tourist-inflows

Some image records use user-supplied image URLs. Image URLs and existing records are preserved. Missing creator, licence or source details need manual review.

## Optional Groq setup

Add the key as a Streamlit Community Cloud secret or server environment variable. Do not put keys in source code or commit them.

```toml
GROQ_API_KEY = "your_key_here"
```

The AI pages have a catalogue-based fallback when Groq is not configured or a request fails. Groq usage may be limited by the account plan and available credits.

## Important limits

- VoyagePK is a prototype, not an official tourism service.
- It does not make bookings or confirm prices or availability.
- It is not a road, weather or safety service.
- Destination and festival information may be incomplete or out of date.
- Image creator and reuse details are not available for every image. Review the source before reuse.
- AI output can be wrong. Check important facts with official sources and local providers.
- Investment and growth outputs use example assumptions. They are not forecasts or investment advice.
- Gilgit-Baltistan inflow data is a partial January–June 2026 snapshot. It must not be treated as a full-year figure or annualised.

## Deployment

Deploy on Streamlit Community Cloud with `app.py` as the app entry point. Configure optional secrets in the Streamlit app settings, not in Git.
