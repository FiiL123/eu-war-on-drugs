# EU Drug War Map — Data Sources Research

Comprehensive inventory of available data sources for mapping drug-related incidents, seizures, enforcement actions, and trafficking across the European Union.

---

## 1. Official EU Data Sources

### 1.1 EUDA — European Union Drugs Agency (formerly EMCDDA)

**Primary URL:** https://www.euda.europa.eu

The EMCDDA was re-established as the **European Union Drugs Agency (EUDA)** in July 2024 with an expanded mandate. This is the single most important data source for this project.

#### Key Data Products

| Dataset | URL | Description |
|---------|-----|-------------|
| **Statistical Bulletin 2026** | https://www.euda.europa.eu/data/stats_en | Annual statistical compendium with interactive data explorer. Covers prevalence, deaths, infections, seizures, prices, purity, offences. Downloadable Excel files. |
| **Data Catalogue** | https://www.euda.europa.eu/data/data-catalogue_en | Searchable catalogue of 137+ datasets. Covers: seizures, prices, purity, wastewater, drug law offences, treatment, deaths, and more. Continuously expanding as part of open data commitment. |
| **Seizures of drugs** | Part of Statistical Bulletin | Number and quantity of seizures by drug type, by country, by year. Data from 27 EU Member States + Norway and Turkey. |
| **Price, purity and potency** | Part of Statistical Bulletin | Street-level and wholesale prices by country and drug type. Purity/potency data. Critical for price heatmap mapping. |
| **Drug law offences** | Part of Statistical Bulletin | Number of offences by drug type and country. Supply-related vs. use-related offences. |
| **Drug-induced deaths** | Part of Statistical Bulletin | Deaths by country, substance, age, gender. |
| **Wastewater analysis (SCORE)** | https://www.euda.europa.eu/topics/wastewater_en | SCORE wastewater data from ~100+ European cities. Near-real-time drug consumption estimates. Excellent for heatmap mapping. |
| **Drug checking (TEDI)** | Part of Statistical Bulletin | Trans European Drugs Information network data on substance composition. |
| **ESCAPE syringe residues** | Part of Statistical Bulletin | Syringe analysis data showing injected substances by city. |
| **Euro-DEN Plus** | Part of Statistical Bulletin | Hospital emergency department data on acute drug toxicity. |
| **ESPAD survey** | https://www.euda.europa.eu/topics/young-people_en | European School Survey Project on Alcohol and Other Drugs. Youth drug use data. |
| **European Web Survey on Drugs** | https://www.euda.europa.eu/activities/european-web-survey-on-drugs_en | Self-reported drug use patterns. |

#### Major Publications

| Publication | URL | Description |
|-------------|-----|-------------|
| **European Drug Report 2026** | https://www.euda.europa.eu/publications/european-drug-report_en | Annual flagship report with interactive visuals and open data. |
| **EU Drug Markets: In-depth analysis** | https://www.euda.europa.eu/publications/eu-drug-markets_en | Joint EMCDDA-Europol analysis. Modular — separate modules for cocaine, cannabis, heroin, MDMA, amphetamine, methamphetamine, NPS. Covers trafficking routes, organized crime groups, distribution. |
| **EU Drug Markets: Key insights** | Same as above | Strategic summary for policymakers. |

#### Data Access

- **Format:** Interactive on-screen data + Excel downloads
- **Geographic coverage:** 27 EU Member States + Norway + Turkey + EU candidate/potential candidate countries
- **Update frequency:** Annual (Statistical Bulletin), continuous (Early Warning System)
- **No formal API** — data is accessed via web interface or downloaded as Excel files
- **Reitox Network:** National focal points in each country that feed data to EUDA — these national reports can contain more granular sub-national data

### 1.2 Europol

**Primary URL:** https://www.europol.europa.eu

#### Key Products

| Product | URL | Description |
|---------|-----|-------------|
| **EU Drug Markets: In-depth analysis** | Joint with EUDA (see above) | The definitive analysis of EU drug trafficking. Includes trafficking routes, organized crime group profiles, seizure data, market analysis. |
| **SOCTA (Serious and Organised Crime Threat Assessment)** | https://www.europol.europa.eu/cms/socta | Includes drug trafficking as a major threat area. Strategic intelligence on routes, actors, methods. |
| **EU Terrorism Situation & Trend Report** | Less relevant | — |
| **Internet Organised Crime Threat Assessment (IOCTA)** | Covers darknet drug markets | Analysis of online drug distribution, darknet marketplaces. |

#### Data Access

- **Limited raw data access** — Europol publishes reports and analysis, not granular datasets
- **Operational data is classified** — only aggregated strategic intelligence is public
- **Drug trafficking page:** https://www.europol.europa.eu/cms/drug-trafficking
- **JS-rendered site** — scraping requires browser automation

### 1.3 Eurostat

**Primary URL:** https://ec.europa.eu/eurostat

#### Relevant Datasets

| Dataset | Code | Description |
|---------|------|-------------|
| **Drug-induced deaths** | `hlth_cd_dg` | Deaths by drug type, age, sex, country |
| **Drug law offences** | Available via EUDA collaboration | Offences reported to Eurostat by national statistical offices |
| **Causes of death** | `hlth_cd_anr` | Includes drug-related mortality (ICD codes F11-F19, X40-X44, Y10-Y14) |
| **Population data** | Various | Denominators for rate calculations |

#### Data Access

- **Data Browser:** https://ec.europa.eu/eurostat/databrowser/
- **REST API available:** `https://ec.europa.eu/eurostat/api/dissemination/`
- **SDMX format:** Standard statistical data exchange format
- **Bulk downloads:** https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing

### 1.4 EU Drugs Action Plan / EU Drugs Strategy

- **EU Drugs Strategy 2021-2025:** Framework document, not a data source per se
- **EMPACT (European Multidisciplinary Platform Against Criminal Threats):** Operational action plans against drug trafficking — classified but summaries available
- **URL:** https://www.euda.europa.eu/topics/drug-markets_en (references to EMPACT)

---

## 2. News/Event Data Sources

### 2.1 GDELT Project (Global Database of Events, Language, and Tone)

**Primary URL:** https://gdeltproject.org

**The single best event-level data source for real-time mapping.**

| Feature | Details |
|---------|---------|
| **Coverage** | News media from every country, in 100+ languages, updated every 15 minutes |
| **Records** | Over a quarter-billion event records spanning 215+ years |
| **Event types** | CAMEO event taxonomy — can filter for law enforcement actions, seizures, arrests |
| **Geocoding** | Events are geolocated to city/district level where possible |
| **Global Knowledge Graph** | Connects people, organizations, locations, themes, emotions |

#### Access Methods

| Method | URL | Notes |
|--------|-----|-------|
| **GDELT Analysis Service** | https://analysis.gdeltproject.org/ | Free cloud-based. Visualize and export from browser. No coding required. Exports CSV, KML (Google Earth), Gephi formats. |
| **Google BigQuery** | `gdelt-bq` dataset | Query entire dataset with SQL. Updated every 15 minutes. Free tier available (1TB queries/month). Best for production use. |
| **Raw data files** | https://gdeltproject.org/data.html | Download CSV files. ~2.5TB/year for GKG alone. Requires significant storage/processing. |
| **API (2.0)** | https://api.gdeltproject.org/api/v2/doc/doc?query=drug%20seizure%20Europe&mode=ArtList | REST API for querying. Returns JSON. Free, no auth required. |

#### Example Queries for Drug Events

```
# BigQuery: Drug seizure events in Europe (2024)
SELECT Date, Actor1Name, Actor2Name, EventCode, GoldsteinScale, ActionGeo_FullName, SOURCEURL
FROM `gdelt-bq.gdeltv2.events`
WHERE EventBaseCode IN ('173', '174', '175')  # coerce, arrest, detain
  AND ActionGeo_CountryCode IN ('UK', 'FR', 'DE', 'IT', 'ES', 'NL', 'BE', ... )
  AND (SOURCEURL LIKE '%drug%' OR SOURCEURL LIKE '%seizure%' OR SOURCEURL LIKE '%narcotic%')
  AND SQL_DATE >= '2024-01-01'

# API: Recent drug trafficking articles about Europe
https://api.gdeltproject.org/api/v2/doc/doc?query=drug%20trafficking%20seizure%20Europe&sourcelang:english&maxrecords=250&format=json
```

#### Key GDELT Tables in BigQuery

- `gdelt-bq.gdeltv2.events` — Event database (CAMEO-coded events from news)
- `gdelt-bq.gdeltv2.gkg` — Global Knowledge Graph (themes, locations, emotions from news)
- `gdelt-bq.gdeltv2.gkg_partitioned` — Partitioned GKG for cost-efficient queries

### 2.2 ACLED (Armed Conflict Location & Event Data Project)

**Primary URL:** https://acleddata.com

| Feature | Details |
|---------|---------|
| **Coverage** | Political violence and protest events globally |
| **Relevance** | Limited — focuses on armed conflict, not drug enforcement. Could capture drug-related violence in some contexts. |
| **Access** | Registration required. Free for non-commercial use. API available. |
| **URL** | https://acleddata.com/data/ |

**Verdict:** Low relevance for this project. ACLED tracks political violence and protests, not drug seizures or trafficking events.

### 2.3 News APIs

| Service | URL | Notes |
|---------|-----|-------|
| **NewsAPI.org** | https://newsapi.org | Aggregate of 150,000+ sources. Free tier: 100 requests/day. Can filter by keyword ("drug seizure Europe"). |
| **MediaStack** | https://mediastack.com | Free news API. 100 requests/month free. |
| **CurrentsAPI** | https://currentsapi.services | Free news aggregation API. |
| **The News Explorer (GDELT)** | https://explorer.gdeltproject.org/ | Browser-based GDELT news explorer. |
| **Event Registry** | https://eventregistry.org | Academic news event extraction. Free for research. API access. |

### 2.4 RSS Feeds from European Law Enforcement

| Agency | RSS/News URL | Notes |
|--------|-------------|-------|
| **Europol** | https://www.europol.europa.eu/newsroom | Press releases on operations. No standard RSS — needs scraping. |
| **Frontex** | https://frontex.europa.eu/media-centre/news/ | May cover maritime drug interceptions. |
| **MAOC-N (Maritime Analysis Operations Centre – Narcotics)** | https://maoc.eu/ | NATO/EU joint maritime drug interdiction info. Limited public data. |
| **CEPOL** | https://www.cepol.europa.eu/ | EU law enforcement training agency. |
| **National LEAs** | Various | BKA (Germany), Guardia Civil (Spain), Polizia di Stato (Italy), DNRED (France), etc. Each has press releases on seizures. |

#### Scraping Strategy

For national law enforcement agencies, a scraper approach would work:
- **Germany:** Bundeskriminalamt (BKA) press releases
- **Spain:** Guardia Civil news, Policía Nacional news
- **France:** Gendarmerie, Police nationale, Douanes (customs seizures)
- **Italy:** Guardia di Finanza, Polizia di Stato
- **Netherlands:** Politie.nl, Marechaussee
- **Belgium:** Federale Politie / Police Fédérale
- **Portugal:** Polícia Judiciária
- **UK (post-Brexit):** NCA (National Crime Agency)

---

## 3. Existing Drug Mapping Projects

### 3.1 EUDA Interactive Tools

| Tool | URL | Description |
|------|-----|-------------|
| **European Drug Report Interactive** | https://www.euda.europa.eu/publications/european-drug-report_en | Interactive charts and maps in the annual report. |
| **Wastewater dashboard** | https://www.euda.europa.eu/topics/wastewater_en | Interactive map of wastewater monitoring cities across Europe. |
| **Country profiles** | https://www.euda.europa.eu/countries_en | Per-country data visualization dashboards. |
| **Data explorer** | Part of Statistical Bulletin | Interactive data tables with charting. |

### 3.2 UNODC Data Portal

**URL:** https://dataunodc.un.org

| Feature | Details |
|---------|---------|
| **Drug Use & Treatment** | Prevalence, treatment demand by country |
| **Drug Trafficking & Cultivation** | Seizure data, trafficking routes, cultivation estimates |
| **Interactive charts** | Built-in visualization tools |
| **Data export** | CSV/Excel downloads |
| **World Drug Report** | https://www.unodc.org/unodc/en/data-and-analysis/WDR.html — Annual flagship with interactive data portal |

### 3.3 Notable Existing Maps/Visualizations

| Project | URL | Description |
|---------|-----|-------------|
| **EUDA Wastewater Map** | https://www.euda.europa.eu/topics/wastewater_en | City-level drug consumption estimates from wastewater. The best existing EU drug data map. |
| **UNODC World Drug Report maps** | Part of annual WDR | Global trafficking flow maps, cultivation maps |
| **Cocaine Route Programme** | EU-funded programme for mapping cocaine trafficking routes from South America to Europe. Limited public-facing maps. |
| **OCCRP (Organized Crime and Corruption Reporting Project)** | https://www.occrp.org | Investigative journalism. Occasional interactive maps of trafficking networks. |
| **InSight Crime** | https://insightcrime.org | Focuses on Latin American organized crime but covers European connections extensively. |
| **Global Initiative Against Transnational Organized Crime** | https://globalinitiative.net | Research and analysis on organized crime including drug trafficking routes. |
| **Border Monitoring** | Various academic projects | EU-funded research projects sometimes produce trafficking route maps. |

### 3.4 GitHub / Open Source Projects

Search for existing drug mapping code:
- `drug trafficking map` on GitHub — limited results, mostly academic
- `EMCDDA data` on GitHub — some data analysis notebooks
- `GDELT visualization` on GitHub — many examples of mapping GDELT events

---

## 4. Open Source Intelligence (OSINT) Sources

### 4.1 Telegram Monitoring

**Context:** Drug dealers increasingly use Telegram for distribution in Europe. Journalists and researchers have documented this extensively.

| Approach | Notes | Feasibility |
|----------|-------|-------------|
| **Telegram API** | https://core.telegram.org/api | Free API. Can monitor public channels. Requires channel IDs/names. |
| **Telethon / Pyrogram** | Python libraries for Telegram API | Can scrape messages from public channels. |
| **Channel discovery** | Academic papers and journalists have published lists of drug-dealing Telegram channels | Bellingcat and others have published OSINT guides for Telegram monitoring. |
| **Limitations** | Private channels require invitation. Ethical/legal concerns around monitoring. End-to-end encryption on secret chats. | **Medium** feasibility, **high** legal/ethical complexity |

### 4.2 Dark Web Monitoring

| Tool/Source | URL | Notes |
|-------------|-----|-------|
| **Darknet market archives** | Academic datasets exist (e.g., from Gwern Branwen) | Historical data from Silk Road, AlphaBay, etc. |
| **EUDA Darknet Markets topic** | https://www.euda.europa.eu/topics/darknet-markets_en | EUDA publishes analysis of darknet drug markets. |
| **DarkOwl** | https://www.darkowl.com | Commercial dark web intelligence. Paid API. |
| **Flashpoint** | https://www.flashpoint.io | Commercial threat intelligence including dark web. |
| **Webhose/Cyberrisk** | Various | Dark web monitoring services. |

**Verdict:** Commercial dark web monitoring is expensive. Academic datasets are historical. The EUDA publications provide good strategic analysis without needing direct dark web access.

### 4.3 Social Media Monitoring

| Platform | Approach | Notes |
|----------|----------|-------|
| **Twitter/X API** | Filter for drug seizure keywords, geolocation | API is now paid (Basic tier: $100/month). Lower-cost alternatives: use GDELT which already monitors Twitter/X. |
| **Reddit** | Monitor subreddits like r/Europe, r/drugs for location-relevant posts | Reddit API is rate-limited but still accessible. |
| **Snapchat** | Used for drug dealing but no API for monitoring | Not feasible for automated collection. |
| **Instagram** | Visual drug market posts | Meta API restrictions make large-scale monitoring impractical. |

### 4.4 Academic OSINT Resources

| Resource | URL | Notes |
|----------|-----|-------|
| **Bellingcat** | https://www.bellingcat.com | OSINT methodology guides. Has covered drug trafficking investigations. |
| **GI-TOC Observatory** | https://globalinitiative.net/observatory/ | Organized crime indexes and maps. |
| **OCCRP Aleph** | https://aleph.occrp.org | Cross-referencing documents and data for investigative journalism. |
| **EU4MD (EU4Monitoring Drugs)** | EUDA project | Monitors digital media for emerging drug trends. |

---

## 5. Recommended Data Types for Mapping

### 5.1 Priority Data Matrix

| Data Type | Best Source | Granularity | Update Freq. | Map Value |
|-----------|------------|-------------|--------------|-----------|
| **Drug seizures (qty, type, location)** | EUDA Statistical Bulletin | National | Annual | **Critical** — but only country-level |
| **Seizure incidents (location, date)** | GDELT + News scraping | City-level | Real-time | **Critical** — fills the granularity gap |
| **Drug prices (street & wholesale)** | EUDA Statistical Bulletin | National | Annual | **High** — price heatmap by country |
| **Overdose deaths** | EUDA + Eurostat | National/Regional | Annual | **High** — mortality heatmap |
| **Wastewater drug levels** | EUDA SCORE | City-level | Annual | **Very High** — city consumption map |
| **Trafficking routes** | EU Drug Markets report + UNODC | Regional | Annual | **Very High** — flow map |
| **Drug lab discoveries** | GDELT + news scraping | City-level | Real-time | **High** — point map |
| **Arrests** | GDELT + news scraping | City-level | Real-time | **High** — incident map |
| **Dark web activity** | EUDA reports | National | Periodic | **Medium** — supplementary layer |
| **Hospital emergencies** | Euro-DEN Plus | City-level | Annual | **Medium** — health impact layer |

### 5.2 Recommended Architecture

```
┌─────────────────────────────────────────────────┐
│                 DATA SOURCES                      │
├──────────────────┬──────────────────────────────┤
│  STATIC (Annual) │  REAL-TIME (Daily/15min)     │
│                  │                               │
│  • EUDA seizures │  • GDELT events API           │
│  • EUDA prices   │  • GDELT BigQuery             │
│  • EUDA deaths   │  • News API (keyword filter)  │
│  • Eurostat      │  • RSS scrapers (LEAs)        │
│  • UNODC         │  • Telegram monitors (optional)│
│  • Wastewater    │                               │
└──────────────────┴──────────────────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────────────────────────────────────┐
│              DATA PIPELINE                        │
│                                                   │
│  • Python scripts (scheduled with cron/GH Actions)│
│  • Normalize to common schema:                    │
│    { date, lat, lon, type, drug, quantity,        │
│      source, source_url, description }            │
│  • Geocode location strings → lat/lon             │
│  • Store in SQLite / PostgreSQL / GeoJSON         │
└─────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────┐
│              MAP FRONTEND                         │
│                                                   │
│  • MapLibre GL JS / Leaflet                      │
│  • Layers:                                       │
│    - Seizure points (clustered)                  │
│    - Price heatmap (choropleth by country)       │
│    - Trafficking route flows (animated arcs)     │
│    - Wastewater city markers                     │
│    - Death rate choropleth                       │
│    - Timeline slider (year/month)                │
│  • Filter by: drug type, date range, country     │
│  • Click incident → details panel with source    │
└─────────────────────────────────────────────────┘
```

### 5.3 Common Data Schema

```typescript
interface DrugIncident {
  id: string;
  date: string;           // ISO 8601
  location: {
    name: string;         // e.g. "Rotterdam"
    country: string;      // ISO 3166-1 alpha-2
    lat: number | null;
    lon: number | null;
  };
  type: "seizure" | "arrest" | "lab_discovery" | "overdose_cluster" | "interception" | "other";
  drugs: {
    name: string;         // e.g. "cocaine", "heroin", "cannabis", "mdma", "amphetamine", "methamphetamine", "nps"
    quantity_kg: number | null;
    quantity_estimated: boolean;
    street_value_eur: number | null;
    purity_percent: number | null;
  }[];
  source: {
    name: string;         // e.g. "GDELT", "EUDA", "Guardia Civil"
    url: string;
    date_accessed: string;
  };
  description: string;
  actors: string[];       // e.g. ["Guadian Civil", "Europol"]
}
```

---

## 6. Quick-Start Recommendations

### For an MVP (Minimum Viable Product):

1. **GDELT BigQuery** — Pull drug seizure/trafficking events for Europe from the last 2 years. This gives you geolocated, timestamped incidents with source URLs. This alone can power a compelling map.

2. **EUDA Statistical Bulletin** — Download the Excel files for:
   - Seizures (country-level aggregates)
   - Prices (country-level)
   - Wastewater (city-level)
   - Deaths (country-level)

3. **EUDA EU Drug Markets** — Extract trafficking route descriptions from the cocaine, heroin, and cannabis modules to create route overlays.

4. **UNODC Data Portal** — Supplement with global context data.

### For a Production System:

5. Add **news scraping** of 5-10 major European LEA press release pages.
6. Add **GDELT real-time API** polling every 15 minutes for new drug events.
7. Add **Telegram monitoring** for specific channels (with legal review).
8. Add **Eurostat API** integration for mortality data.
9. Add **EUDA data catalogue** scraping for annual data updates.

---

## 7. Key URLs Summary

| Source | URL |
|--------|-----|
| EUDA (formerly EMCDDA) | https://www.euda.europa.eu |
| EUDA Statistical Bulletin | https://www.euda.europa.eu/data/stats_en |
| EUDA Data Catalogue | https://www.euda.europa.eu/data/data-catalogue_en |
| EUDA EU Drug Markets | https://www.euda.europa.eu/publications/eu-drug-markets_en |
| EUDA Wastewater | https://www.euda.europa.eu/topics/wastewater_en |
| Europol | https://www.europol.europa.eu |
| UNODC Data Portal | https://dataunodc.un.org |
| UNODC World Drug Report | https://www.unodc.org/unodc/en/data-and-analysis/WDR.html |
| GDELT Project | https://gdeltproject.org |
| GDELT Analysis Service | https://analysis.gdeltproject.org/ |
| GDELT API 2.0 | https://api.gdeltproject.org/api/v2/doc/doc |
| GDELT BigQuery | `gdelt-bq` dataset on Google BigQuery |
| ACLED | https://acleddata.com |
| Eurostat Data Browser | https://ec.europa.eu/eurostat/databrowser/ |
| Eurostat API | https://ec.europa.eu/eurostat/api/dissemination/ |
| OCCRP | https://www.occrp.org |
| GI-TOC | https://globalinitiative.net |
| Bellingcat | https://www.bellingcat.com |
| InSight Crime | https://insightcrime.org |
| MAOC-N | https://maoc.eu |
| NewsAPI | https://newsapi.org |

---

*Research conducted June 2026. The EMCDDA was re-established as EUDA (European Union Drugs Agency) in July 2024. Some legacy URLs may still reference "emcdda" — both `www.emcdda.europa.eu` and `www.euda.europa.eu` domains may work for some pages.*
