from sqlalchemy import Column, Integer, String, Float, Date
from database import Base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

class WeatherData(Base):
    __tablename__ = "weather_data"
    
    id = Column(Integer, primary_key=True, index=True)
    station = Column(String, index=True)
    date = Column(Date)
    latitude = Column(Float)
    longitude = Column(Float)
    elevation = Column(Float)
    name = Column(String)
    temp = Column(Float)
    visib = Column(Float)
    wdsp = Column(Float)
    max = Column(Float)
    min = Column(Float)
    prcp = Column(Float)

