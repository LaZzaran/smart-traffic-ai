"""
Database models for the application
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class TrafficData(Base):
    """Traffic data model"""
    __tablename__ = "traffic_data"
    
    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    speed = Column(Float)  # Ortalama hız (km/h)
    density = Column(Float)  # Trafik yoğunluğu (0-1 arası)
    timestamp = Column(DateTime, default=datetime.utcnow)
    source = Column(String)  # Veri kaynağı (OSM, sensor, etc.)

class Route(Base):
    """Route model"""
    __tablename__ = "routes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    start_latitude = Column(Float)
    start_longitude = Column(Float)
    end_latitude = Column(Float)
    end_longitude = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="routes")

# User modeline route ilişkisini ekle
User.routes = relationship("Route", back_populates="user") 