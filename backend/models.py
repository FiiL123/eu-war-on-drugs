import os
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ARRAY, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://drugmap:drugmap@localhost:5432/drugmap")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    description = Column(Text)
    event_time = Column(DateTime(timezone=True), nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    country = Column(String(3))
    city = Column(Text)
    category = Column(String(50))
    drug_type = Column(String(50))
    quantity_kg = Column(Float)
    source_url = Column(Text)
    source_name = Column(Text)
    media_urls = Column(ARRAY(Text))
    status = Column(String(20), default="pending")
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)


class TraffickingRoute(Base):
    __tablename__ = "trafficking_routes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    description = Column(Text)
    drug_type = Column(String(50))
    route_geojson = Column(Text)
    severity = Column(String(20))
    source = Column(Text)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
