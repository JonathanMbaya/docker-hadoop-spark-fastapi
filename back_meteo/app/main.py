from fastapi import FastAPI
from app.routers.user_router import router as user_router  # Routes utilisateur
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Créer toutes les tables au démarrage
WeatherData.metadata.create_all(bind=engine)

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

# Fonction pour obtenir la session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Inclusion des routes
app.include_router(user_router, prefix="/users", tags=["users"])

# Initialisation de la base de données au démarrage

@app.get("/")
async def read_root():
    return {"message": "Bienvenue dans l'API FastAPI avec PostgreSQL"}


# Route pour récupérer les données météo
@app.get("/weather_data")
async def get_all_weather_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    weather_data = crud.get_weather_data(db, skip=skip, limit=limit)
    return weather_data
