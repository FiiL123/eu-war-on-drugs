import httpx
import re
import json
from datetime import datetime, timedelta
from typing import Optional
import logging
import asyncio

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from aiolimiter import AsyncLimiter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GDELT_RATE_LIMIT = AsyncLimiter(1, 8)
NOMINATIM_RATE_LIMIT = AsyncLimiter(1, 1.1)

EU_COUNTRIES = [
    "unitedkingdom", "germany", "france", "italy", "spain", "netherlands",
    "belgium", "austria", "poland", "czechrepublic", "portugal", "sweden",
    "denmark", "finland", "ireland", "greece", "croatia", "romania",
    "bulgaria", "hungary", "slovakia", "slovenia", "estonia", "latvia",
    "lithuania", "luxembourg", "cyprus", "malta", "norway", "switzerland",
    "serbia", "albania",
]

DRUG_KEYWORDS = [
    "drug seizure", "cocaine bust", "heroin arrest", "meth lab",
    "drug trafficking", "narcotics seized", "drug cartel", "fentanyl",
    "mdma seizure", "amphetamine", "cannabis seized", "hashish",
    "drug smuggling", "drug bust", "narco", "drug ring",
    "drug operation", "counter-narcotics", "drug enforcement",
    "ecstasy seizure", "drug lab", "precursor chemicals",
    "dark web drugs", "online drug market",
]

DRUG_TYPE_PATTERNS = {
    "cocaine": [r"\bcocaine\b", r"\bcrack\b"],
    "heroin": [r"\bheroin\b", r"\bdiamorphine\b"],
    "cannabis": [r"\bcannabis\b", r"\bmarijuana\b", r"\bhashish\b", r"\bweed\b"],
    "synthetic": [r"\bamphetamine\b", r"\bmethamphetamine\b", r"\bmeth\b", r"\bcrystal meth\b"],
    "fentanyl": [r"\bfentanyl\b", r"\bfentanil\b"],
    "mdma": [r"\bmdma\b", r"\becstasy\b"],
}

CATEGORY_PATTERNS = {
    "seizure": [r"\bseizure\b", r"\bseized\b", r"\bconfiscated\b", r"\bintercepted\b"],
    "arrest": [r"\barrested\b", r"\bdetained\b", r"\bapprehended\b"],
    "lab_bust": [r"\blab\b", r"\blaboratory\b", r"\bproduction facility\b"],
    "port_interdiction": [r"\bport\b", r"\bcustoms\b", r"\bshipping\b", r"\bcontainer\b", r"\bmaritime\b"],
    "dark_web": [r"\bdark ?web\b", r"\bdarknet\b", r"\bonline market\b"],
    "overdose": [r"\boverdose\b", r"\bod death\b"],
    "policy": [r"\blegislation\b", r"\bdecriminali[sz]", r"\bpolicy\b", r"\bregulation\b"],
}


def classify_drug_type(text: str) -> str:
    text_lower = text.lower()
    for drug_type, patterns in DRUG_TYPE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                return drug_type
    return "other"


def classify_category(text: str) -> str:
    text_lower = text.lower()
    for category, patterns in CATEGORY_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                return category
    return "seizure"


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=2, min=5, max=120),
    retry=retry_if_exception_type((httpx.HTTPStatusError, httpx.ConnectError, httpx.ReadTimeout)),
    before_sleep=lambda state: logger.warning(
        f"GDELT request failed (attempt {state.attempt_number}), retrying in {state.next_action.sleep}s..."
    ),
)
async def _fetch_gdelt_with_retry(client: httpx.AsyncClient, url: str, params: dict) -> dict:
    async with GDELT_RATE_LIMIT:
        response = await client.get(url, params=params)
        response.raise_for_status()
        try:
            return response.json()
        except json.JSONDecodeError:
            logger.warning(f"GDELT returned non-JSON response (status {response.status_code}, body: {response.text[:200]})")
            raise httpx.HTTPStatusError(
                f"Invalid JSON response", request=response.request, response=response
            )


async def fetch_gdelt_events(hours_back: int = 24) -> list[dict]:
    gdelt_base = "https://api.gdeltproject.org/api/v2/doc/doc"

    end_date = datetime.utcnow()
    start_date = end_date - timedelta(hours=hours_back)

    keyword_groups = [
        ["drug seizure", "cocaine bust", "heroin arrest", "meth lab", "drug trafficking"],
        ["narcotics seized", "fentanyl", "mdma seizure", "amphetamine", "drug bust"],
        ["cannabis seized", "hashish", "drug smuggling", "drug lab", "dark web drugs"],
    ]
    country_groups = [
        ["unitedkingdom", "germany", "france", "italy", "spain"],
        ["netherlands", "belgium", "austria", "poland", "portugal"],
        ["sweden", "denmark", "finland", "ireland", "greece"],
        ["croatia", "romania", "bulgaria", "hungary", "norway"],
    ]

    all_events = []
    seen_urls = set()

    async with httpx.AsyncClient(timeout=30) as client:
        for kw_group in keyword_groups:
            for cc_group in country_groups:
                keywords_query = " OR ".join(f'"{kw}"' for kw in kw_group)
                countries_query = " OR ".join(f"sourcecountry:{c}" for c in cc_group)

                params = {
                    "query": f"({keywords_query}) ({countries_query}) sourcelang:english",
                    "mode": "ArtList",
                    "maxrecords": 75,
                    "format": "json",
                    "STARTDATETIME": start_date.strftime("%Y%m%d%H%M%S"),
                    "ENDDATETIME": end_date.strftime("%Y%m%d%H%M%S"),
                }

                try:
                    data = await _fetch_gdelt_with_retry(client, gdelt_base, params)
                except Exception as e:
                    logger.warning(f"Skipping query batch: {e}")
                    continue

                for article in data.get("articles", []):
                    url = article.get("url", "")
                    if url in seen_urls:
                        continue
                    seen_urls.add(url)

                    title = article.get("title", "")
                    source = article.get("domain", "")
                    pub_date = article.get("seendate", "")

                    if not title or not url:
                        continue

                    lat = None
                    lng = None
                    if "latlong" in article and article["latlong"]:
                        try:
                            parts = article["latlong"].split(",")
                            lat = float(parts[0])
                            lng = float(parts[1])
                        except (ValueError, IndexError):
                            pass

                    all_events.append({
                        "title": title[:500],
                        "description": title,
                        "event_time": pub_date,
                        "lat": lat,
                        "lng": lng,
                        "country": None,
                        "city": None,
                        "category": classify_category(title),
                        "drug_type": classify_drug_type(title),
                        "quantity_kg": None,
                        "source_url": url,
                        "source_name": source,
                        "status": "pending",
                    })

    logger.info(f"Fetched {len(all_events)} drug-related events from GDELT")
    return all_events


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2, min=2, max=30),
    retry=retry_if_exception_type((httpx.HTTPStatusError, httpx.ConnectError)),
)
async def geocode_location(city: str, country: str) -> Optional[tuple[float, float]]:
    query = f"{city}, {country}" if city else country
    params = {
        "q": query,
        "format": "json",
        "limit": 1,
    }

    async with NOMINATIM_RATE_LIMIT:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                "https://nominatim.openstreetmap.org/search", params=params
            )
            response.raise_for_status()
            data = response.json()
            if data:
                return float(data[0]["lat"]), float(data[0]["lon"])

    return None


async def ingest_gdelt(hours_back: int = 24) -> int:
    from models import SessionLocal, Event

    try:
        events = await fetch_gdelt_events(hours_back)
    except Exception as e:
        logger.error(f"Failed to fetch GDELT events after all retries: {e}")
        return 0

    db = SessionLocal()
    count = 0

    try:
        for event_data in events:
            existing = (
                db.query(Event)
                .filter(Event.source_url == event_data["source_url"])
                .first()
            )
            if existing:
                continue

            if event_data["lat"] is None:
                try:
                    coords = await geocode_location(
                        event_data.get("city", ""), event_data.get("country", "")
                    )
                except Exception:
                    coords = None
                if coords:
                    event_data["lat"], event_data["lng"] = coords
                else:
                    continue

            if event_data["event_time"]:
                try:
                    event_data["event_time"] = datetime.strptime(
                        event_data["event_time"], "%Y%m%dT%H%M%Sz"
                    )
                except ValueError:
                    event_data["event_time"] = datetime.utcnow()
            else:
                event_data["event_time"] = datetime.utcnow()

            db_event = Event(**event_data)
            db.add(db_event)
            count += 1

        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Ingestion DB error: {e}")
    finally:
        db.close()

    logger.info(f"Ingested {count} new events")
    return count


if __name__ == "__main__":
    asyncio.run(ingest_gdelt(72))
