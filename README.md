# EU War on Drugs - Live Map

**A real-time interactive map of drug enforcement activity across Europe.**

Every day, hundreds of drug seizures, arrests, lab busts, and trafficking operations happen across the EU. This project brings them all onto a single, searchable, filterable map — updated in near real-time from thousands of news sources worldwide.

Inspired by [LiveUAMap](https://liveuamap.com), adapted for Europe's fight against the drug trade.

## What It Does

**See the war on drugs as it unfolds.** The map plots enforcement events — seizures, arrests, lab busts, port interdictions, dark web takedowns, overdose spikes, and policy changes — with color-coded markers showing what happened, where, and when.

- **Real-time news ingestion** — Automatically pulls drug-related events from 50,000+ global news sources via the GDELT Project
- **Smart classification** — Each event is tagged by drug type (cocaine, heroin, fentanyl, MDMA, etc.) and category (seizure, arrest, lab bust, etc.)
- **Interactive map** — Click any marker for the full story: what was seized, how much, who was arrested, and a link to the source
- **Filterable** — Toggle drug types and event categories to focus on what matters to you
- **Timeline sidebar** — Chronological feed of events with location, quantity, and source
- **Admin curation** — Human review panel to verify, reject, or edit automatically ingested events before they go live

## Why This Matters

Europe is the world's largest cocaine market. The Balkan route funnels heroin from Afghanistan through Southeast Europe. Synthetic drug labs in the Netherlands and Belgium produce billions of ecstasy pills annually. Fentanyl is creeping in from the east.

Yet there's no single, publicly accessible map that shows the full picture of drug enforcement across the EU. News reports are scattered across languages and outlets. Statistics come out months or years late.

**This project closes that gap.** A live, unified view of drug enforcement in Europe — open, transparent, and continuously updated.

## What's On the Map

| Event Type | What It Tracks |
|-----------|---------------|
| **Seizure** | Drug quantities intercepted by law enforcement |
| **Arrest** | Suspects detained in drug operations |
| **Lab Bust** | Synthetic drug production facilities dismantled |
| **Port Interdiction** | Drugs seized at ports — Rotterdam, Antwerp, Hamburg, and beyond |
| **Dark Web Bust** | Online drug marketplaces shut down by police |
| **Overdose Cluster** | Spikes in overdose incidents requiring public alerts |
| **Policy Change** | Drug legislation, decriminalization, and regulation updates |
| **Trafficking Route** | Known smuggling corridors mapped across the continent |

Each event is tagged by drug type — cocaine, heroin, cannabis, synthetic, fentanyl, MDMA — with distinct colors for instant visual recognition.

## Data Sources

The map aggregates from multiple sources for maximum coverage:

- **[GDELT Project](https://gdeltproject.org)** — Real-time news event data from 50,000+ sources in 65 languages (primary, auto-ingested)
- **[EUDA](https://euda.europa.eu)** (formerly EMCDDA) — EU drug agency statistics on seizures, prices, and deaths
- **[UNODC](https://dataunodc.un.org)** — Global trafficking routes and seizure data
- **Europol** — Cross-border operation press releases
- **National law enforcement** — Country-specific agencies via RSS feeds

## Getting Started

### Just want to see it?

Open `index.html` in any browser. It ships with 25 realistic sample events across 17 countries — no server needed.

### Full stack (real data)

```bash
docker compose up -d
```

One command starts everything — database, API, and automated news ingestion. The map is live at `http://localhost:8000`.

### Local development

```bash
cd backend
uv sync
uv run uvicorn main:app --reload
```

## How It Works

Events flow through a multi-stage pipeline before appearing on the map:

1. **Gather** — GDELT API is polled every 15 minutes for drug-related news in EU countries
2. **Classify** — NLP tags each event with a drug type and category
3. **Geocode** — Events without coordinates are geolocated via OpenStreetMap Nominatim
4. **Deduplicate** — Repeated coverage of the same event is collapsed
5. **Queue** — New events enter as "pending" in the database
6. **Review** — Admins verify, edit, or reject events via the curation panel
7. **Publish** — Verified events appear on the public map

---

## Technical Details

### Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML/CSS/JS + [Leaflet.js](https://leafletjs.com) |
| Backend | Python [FastAPI](https://fastapi.tiangolo.com) |
| Database | PostgreSQL + [PostGIS](https://postgis.net) |
| Data source | [GDELT Project](https://gdeltproject.org) API |
| Package manager | [uv](https://github.com/astral-sh/uv) |
| Ingestion | [tenacity](https://github.com/jd/tenacity) (retries) + [aiolimiter](https://aiolimiter.readthedocs.io) (rate limiting) |
| Containers | Docker Compose |

### Project Structure

```
eu-drug-war-map/
├── index.html                  # Main map page
├── css/style.css               # Light theme, sidebar, markers, popups
├── js/
│   ├── config.js               # Drug types, categories, colors, SVG icons
│   ├── data.js                 # 25 realistic sample events
│   ├── markers.js              # Leaflet pin markers (SVG), popups
│   ├── filters.js              # Drug type & category toggle filters
│   ├── timeline.js             # Chronological sidebar + stats
│   ├── api.js                  # Backend API client (falls back to sample data)
│   └── app.js                  # Map initialization
├── backend/
│   ├── main.py                 # FastAPI REST API (CRUD events)
│   ├── models.py               # SQLAlchemy models (PostGIS)
│   ├── gdelt_ingester.py       # GDELT polling with retries + rate limiting
│   ├── pyproject.toml          # uv-managed dependencies
│   ├── uv.lock                 # Lockfile
│   ├── Dockerfile              # uv-based Docker image
│   └── admin/admin.html        # Event curation panel
├── data/
│   └── schema.sql              # PostgreSQL + PostGIS schema with indexes
└── docker-compose.yml          # db + api + ingest
```

### API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/events` | GET | List events (filterable by drug type, category, country, date) |
| `/events/{id}` | GET | Get single event |
| `/events` | POST | Create event |
| `/events/{id}` | PATCH | Update event (verify, reject, edit) |
| `/events/{id}` | DELETE | Delete event |
| `/routes` | GET | List trafficking route overlays |
| `/stats` | GET | Aggregate statistics |

### Manual Ingestion

```bash
cd backend
uv run python -c "import asyncio; from gdelt_ingester import ingest_gdelt; asyncio.run(ingest_gdelt(72))"
```

## License

MIT
