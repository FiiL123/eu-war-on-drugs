from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Optional, Annotated
from datetime import datetime
import os

from models import get_db, Event, TraffickingRoute
from pydantic import BaseModel

app = FastAPI(title="EU War on Drugs Map API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DbSession = Annotated[Session, Depends(get_db)]

STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)))


class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    event_time: datetime
    lat: float
    lng: float
    country: Optional[str] = None
    city: Optional[str] = None
    category: str
    drug_type: str
    quantity_kg: Optional[float] = None
    source_url: Optional[str] = None
    source_name: Optional[str] = None
    media_urls: Optional[list[str]] = None


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    drug_type: Optional[str] = None
    quantity_kg: Optional[float] = None
    status: Optional[str] = None


@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.get("/events")
async def list_events(
    db: DbSession,
    drug_type: Optional[str] = None,
    category: Optional[str] = None,
    country: Optional[str] = None,
    status: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    limit: int = Query(100, le=500),
    offset: int = 0,
):
    query = db.query(Event)

    if drug_type:
        query = query.filter(Event.drug_type == drug_type)
    if category:
        query = query.filter(Event.category == category)
    if country:
        query = query.filter(Event.country == country.upper())
    if status:
        query = query.filter(Event.status == status)
    if date_from:
        query = query.filter(Event.event_time >= datetime.fromisoformat(date_from))
    if date_to:
        query = query.filter(Event.event_time <= datetime.fromisoformat(date_to))

    events = query.order_by(Event.event_time.desc()).offset(offset).limit(limit).all()

    return [
        {
            "id": e.id,
            "title": e.title,
            "description": e.description,
            "event_time": e.event_time.isoformat() if e.event_time else None,
            "lat": e.lat,
            "lng": e.lng,
            "country": e.country,
            "city": e.city,
            "category": e.category,
            "drug_type": e.drug_type,
            "quantity_kg": e.quantity_kg,
            "source_url": e.source_url,
            "source_name": e.source_name,
            "media_urls": e.media_urls,
            "status": e.status,
        }
        for e in events
    ]


@app.get("/events/{event_id}")
async def get_event(event_id: int, db: DbSession):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return {
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "event_time": event.event_time.isoformat() if event.event_time else None,
        "lat": event.lat,
        "lng": event.lng,
        "country": event.country,
        "city": event.city,
        "category": event.category,
        "drug_type": event.drug_type,
        "quantity_kg": event.quantity_kg,
        "source_url": event.source_url,
        "source_name": event.source_name,
        "media_urls": event.media_urls,
        "status": event.status,
    }


@app.post("/events")
async def create_event(event: EventCreate, db: DbSession):
    db_event = Event(**event.model_dump(), status="pending")
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return {"id": db_event.id, "status": "created"}


@app.patch("/events/{event_id}")
async def update_event(event_id: int, update: EventUpdate, db: DbSession):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    for key, value in update.model_dump(exclude_unset=True).items():
        setattr(event, key, value)
    event.updated_at = datetime.utcnow()
    db.commit()
    return {"status": "updated"}


@app.delete("/events/{event_id}")
async def delete_event(event_id: int, db: DbSession):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    db.delete(event)
    db.commit()
    return {"status": "deleted"}


@app.get("/routes")
async def list_routes(db: DbSession):
    routes = db.query(TraffickingRoute).all()
    return [
        {
            "id": r.id,
            "name": r.name,
            "description": r.description,
            "drug_type": r.drug_type,
            "route_geojson": r.route_geojson,
            "severity": r.severity,
            "source": r.source,
        }
        for r in routes
    ]


@app.get("/stats")
async def get_stats(db: DbSession):
    total = db.query(Event).filter(Event.status == "verified").count()
    total_kg = sum(e.quantity_kg or 0 for e in db.query(Event).filter(Event.status == "verified").all())
    countries = set(e.country for e in db.query(Event.country).distinct().all() if e[0])

    return {
        "total_events": total,
        "total_seized_kg": total_kg,
        "countries_affected": len(countries),
        "pending_review": db.query(Event).filter(Event.status == "pending").count(),
    }
