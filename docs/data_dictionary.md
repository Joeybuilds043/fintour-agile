# Data Dictionary

## Destination record
Name; region; latitude and longitude; tagline; overview; culture; experience tags; highlights; season; access; responsible-travel guidance; image query.

Coordinates identify approximate destination-cluster anchors, not precise attraction entrances or turn-by-turn navigation points.

## Evidence record — target schema
Indicator ID; destination ID; indicator name; numeric value; unit; observation period; geographic coverage; source ID; evidence status; publication date; retrieval date; methodology; limitations.

## Image record — target schema
Media URL; source-page URL; creator; individual licence; attribution text; retrieval date; linked destination.

## Financial inputs
Rooms; assumed ADR in PKR; assumed annual occupancy; annual operating costs; initial investment; local procurement share.

## Financial outputs
Room revenue = rooms × 365 × occupancy × ADR.
Operating surplus proxy = room revenue − entered operating costs.
Break-even occupancy = operating costs ÷ (rooms × 365 × ADR).
Simple payback = initial investment ÷ positive operating-surplus proxy.
Local procurement proxy = room revenue × assumed local procurement share.

The prototype excludes financing, taxes, depreciation, replacement capex, working capital and non-room revenue.
