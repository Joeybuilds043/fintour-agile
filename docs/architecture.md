# System Architecture

## Current prototype
Streamlit multipage application; Python service modules; structured destination catalogue; Wikimedia Commons image lookup with caching; Open-Meteo weather integration with caching; isolated accommodation scenario calculations; CSV seed data; documentation and tests.

## Logical flow
Visitor and industry pages -> Python services -> destination catalogue / external providers / analytics -> source and evidence labels.

## Future data platform
PostgreSQL can replace or supplement CSV seed data as the catalogue grows. Proposed entities: destinations, experience categories, attractions, destination-experiences, accommodation, transport access, cultural information, weather snapshots, tourism indicators, business opportunities, data sources and verification records.

## Future production option
A React or Next.js visitor frontend with a FastAPI backend is a possible later evolution. It is not required for the initial prototype. Keep data contracts and business logic separate from Streamlit UI to make migration feasible.
