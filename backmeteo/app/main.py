from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os

# Configurer les paramètres CORS
origins = [
    "http://localhost:5173",
    "http://localhost:8000/"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Configuration de la connexion MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://rootuser:rootpass@mongo:27017/?authSource=admin")
client = AsyncIOMotorClient(MONGO_URI)
db = client.weather
weather_collection = db.weather_data

# Pydantic model pour la réponse
class WeatherData(BaseModel):
    station: str
    date: str
    temp: float
    dew_point: float
    wind_speed: str
    precipitation: int

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.get("/weather", response_model=List[WeatherData])
async def read_all_weather():
    try:
        # Récupérer tous les documents dans la collection "weather_data"
        cursor = weather_collection.find()
        weather_list = []

        async for weather in cursor:
            # Extraire et gérer les valeurs manquantes ou nulles
            station = str(weather.get("station", ""))  # Convertir station en chaîne
            date = weather.get("date", "1970-01-01")  # Valeur par défaut pour la date
            temp = weather.get("temp", 0.0)  # Température par défaut si manquante
            dew_point = weather.get("dew_point", 0.0)  # Point de rosée par défaut
            wind_speed = str(weather.get("wind_speed", 0.0))  # Convertir wind_speed en chaîne
            precipitation = int(weather.get("precipitation", 0.0))  # Convertir en entier (arrondi)

            # Créer l'objet WeatherData
            weather_data = WeatherData(
                station=station,
                date=date,
                temp=temp,
                dew_point=dew_point,
                wind_speed=wind_speed,
                precipitation=precipitation
            )
            weather_list.append(weather_data)

        return weather_list

    except Exception as e:
        print(f"Error occurred: {e}")  # Debug: Afficher l'erreur dans les logs
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/weather/date", response_model=List[WeatherData])
async def read_weather_between_dates(start_date: str, end_date: str):
    """
    Route permettant de récupérer les données météo entre deux dates.
    Les dates doivent être au format 'YYYY-MM-DD'.
    """
    try:
        # Convertir les dates en format datetime pour la recherche dans MongoDB
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")

        # Récupérer les documents dans la collection "weather_data" dont la date est entre les deux dates spécifiées
        cursor = weather_collection.find({
            "date": {
                "$gte": start_date_obj.strftime("%Y-%m-%d"),  # $gte signifie "greater than or equal"
                "$lte": end_date_obj.strftime("%Y-%m-%d")   # $lte signifie "less than or equal"
            }
        })

        weather_list = []

        async for weather in cursor:
            # Extraire et gérer les valeurs manquantes ou nulles
            station = str(weather.get("station", ""))  # Convertir station en chaîne
            date = weather.get("date", "1970-01-01")
            temp = weather.get("temp", 0.0)
            dew_point = weather.get("dew_point", 0.0)
            wind_speed = str(weather.get("wind_speed", 0.0))  # Convertir en chaîne
            precipitation = int(weather.get("precipitation", 0.0))  # Convertir en entier

            # Créer l'objet WeatherData
            weather_data = WeatherData(
                station=station,
                date=date,
                temp=temp,
                dew_point=dew_point,
                wind_speed=wind_speed,
                precipitation=precipitation
            )
            weather_list.append(weather_data)

        return weather_list

    except Exception as e:
        print(f"Error occurred: {e}")  # Debug: Afficher l'erreur dans les logs
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
