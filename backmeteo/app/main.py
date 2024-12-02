from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from bson import ObjectId  # Nécessaire pour gérer les ObjectId MongoDB

app = FastAPI()

# Configurer les paramètres CORS
origins = [
    "http://localhost:5173",
    "http://localhost:8000/"  # Origine de votre application React & Postgres
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Autoriser ces origines
    allow_credentials=True,  # Autoriser les cookies/sessions
    allow_methods=["*"],  # Autoriser toutes les méthodes HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Autoriser tous les headers
)

# Configuration de la connexion MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://rootuser:rootpass@mongo:27017/?authSource=admin")
client = AsyncIOMotorClient(MONGO_URI)
db = client.weather  # Remplacez "weather" par le nom de votre base de données
weather_collection = db.weather_data  # Remplacez "weather_data" par le nom de votre collection

# Pydantic model pour la réponse
class WeatherData(BaseModel):
    id: str  # Champ id sera une chaîne
    date: str
    latitude: float
    longitude: float
    elevation: float
    name: str
    temp: float
    visib: float
    wdsp: float
    max: float
    min: float
    prcp: float



@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.get("/weather", response_model=List[WeatherData])
async def read_all_weather():
    # Récupérer tous les documents dans la collection "weather_data"
    cursor = weather_collection.find()
    weather_list = []
    async for weather in cursor:
        # Convertir l'ObjectId en un string et ajouter à la liste
        weather_data = WeatherData(
            id=str(weather["id"]),  # Convertir ObjectId en string
            date=weather["date"],
            latitude=weather["latitude"],
            longitude=weather["longitude"],
            elevation=weather["elevation"],
            name=weather["name"],
            temp=weather["temp"],
            visib=weather["visib"],
            wdsp=weather["wdsp"],
            max=weather["max"],
            min=weather["min"],
            prcp=weather["prcp"]
        )
        weather_list.append(weather_data)
    return weather_list

@app.get("/items/{id}")
async def read_item(item_id: str):
    # Exemple d'accès à une collection MongoDB
    item = await db.items.find_one({"_id": ObjectId(item_id)})
    return item
