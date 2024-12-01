from sqlalchemy.orm import Session
from models import WeatherData

def get_weather_data(db: Session, skip: int = 0, limit: int = 100):
    return db.query(WeatherData).offset(skip).limit(limit).all()
