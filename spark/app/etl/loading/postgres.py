from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import psycopg2
import pandas as pd
import json
from io import StringIO

app = FastAPI()

# Connexion à PostgreSQL
db_params = {
    "host": "postgres-container",
    "database": "mydatabase",
    "user": "myuser",
    "password": "mypassword_eee"
}

# Modèle Pydantic pour valider les requêtes
class WeatherData(BaseModel):
    station: int
    date: str
    latitude: float
    longitude: float
    elevation: float
    name: str
    temp: float
    temp_attributes: int
    dewp: float
    dewp_attributes: int
    slp: float
    slp_attributes: int
    stp: float
    stp_attributes: int
    visib: float
    visib_attributes: int
    wdsp: float
    wdsp_attributes: int
    mxspd: float
    gust: float
    max: float
    max_attributes: str
    min: float
    min_attributes: str
    prcp: float
    prcp_attributes: str
    sndp: float
    frshtt: int

@app.get("/")
def read_root():
    return {"message": "Welcome to the Weather API"}

@app.get("/weather")
def get_weather():
    """
    Récupère toutes les données météorologiques.
    """
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM weather_data;")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"data": rows}
    except Exception as e:
        return {"error": str(e)}

@app.post("/weather")
def add_weather(data: WeatherData):
    """
    Ajoute une nouvelle donnée météorologique.
    """
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        cursor.execute(""" 
            INSERT INTO weather_data (
                station, date, latitude, longitude, elevation, name, temp, 
                temp_attributes, dewp, dewp_attributes, slp, slp_attributes,
                stp, stp_attributes, visib, visib_attributes, wdsp, wdsp_attributes,
                mxspd, gust, max, max_attributes, min, min_attributes, 
                prcp, prcp_attributes, sndp, frshtt
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                      %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                      %s, %s, %s, %s)
        """, (
            data.station, data.date, data.latitude, data.longitude, data.elevation,
            data.name, data.temp, data.temp_attributes, data.dewp, data.dewp_attributes,
            data.slp, data.slp_attributes, data.stp, data.stp_attributes,
            data.visib, data.visib_attributes, data.wdsp, data.wdsp_attributes,
            data.mxspd, data.gust, data.max, data.max_attributes, data.min,
            data.min_attributes, data.prcp, data.prcp_attributes, data.sndp, data.frshtt
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Données insérées avec succès."}
    except Exception as e:
        return {"error": str(e)}

@app.post("/upload/csv")
async def upload_csv(file: UploadFile = File(...)):
    """
    Endpoint pour uploader un fichier CSV et insérer les données dans la base de données.
    """
    try:
        # Lire le fichier CSV
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode('utf-8')))

        # Connexion à PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Insertion des données ligne par ligne
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO weather_data (
                    station, date, latitude, longitude, elevation, name, temp, 
                    temp_attributes, dewp, dewp_attributes, slp, slp_attributes,
                    stp, stp_attributes, visib, visib_attributes, wdsp, wdsp_attributes,
                    mxspd, gust, max, max_attributes, min, min_attributes, 
                    prcp, prcp_attributes, sndp, frshtt
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                          %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                          %s, %s, %s, %s)
            """, (
                row['station'], row['date'], row['latitude'], row['longitude'], row['elevation'],
                row['name'], row['temp'], row['temp_attributes'], row['dewp'], row['dewp_attributes'],
                row['slp'], row['slp_attributes'], row['stp'], row['stp_attributes'],
                row['visib'], row['visib_attributes'], row['wdsp'], row['wdsp_attributes'],
                row['mxspd'], row['gust'], row['max'], row['max_attributes'], row['min'],
                row['min_attributes'], row['prcp'], row['prcp_attributes'], row['sndp'], row['frshtt']
            ))

        # Commit et fermer la connexion
        conn.commit()
        cursor.close()
        conn.close()

        return {"message": f"Les données ont été insérées avec succès à partir de {file.filename}"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/upload/json")
async def upload_json(file: UploadFile = File(...)):
    """
    Endpoint pour uploader un fichier JSON et insérer les données dans la base de données.
    """
    try:
        # Lire le fichier JSON
        contents = await file.read()
        data = json.loads(contents.decode('utf-8'))

        # Connexion à PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Insertion des données
        for entry in data:
            cursor.execute("""
                INSERT INTO weather_data (
                    station, date, latitude, longitude, elevation, name, temp, 
                    temp_attributes, dewp, dewp_attributes, slp, slp_attributes,
                    stp, stp_attributes, visib, visib_attributes, wdsp, wdsp_attributes,
                    mxspd, gust, max, max_attributes, min, min_attributes, 
                    prcp, prcp_attributes, sndp, frshtt
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                          %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                          %s, %s, %s, %s)
            """, (
                entry['station'], entry['date'], entry['latitude'], entry['longitude'], entry['elevation'],
                entry['name'], entry['temp'], entry['temp_attributes'], entry['dewp'], entry['dewp_attributes'],
                entry['slp'], entry['slp_attributes'], entry['stp'], entry['stp_attributes'],
                entry['visib'], entry['visib_attributes'], entry['wdsp'], entry['wdsp_attributes'],
                entry['mxspd'], entry['gust'], entry['max'], entry['max_attributes'], entry['min'],
                entry['min_attributes'], entry['prcp'], entry['prcp_attributes'], entry['sndp'], entry['frshtt']
            ))

        # Commit et fermer la connexion
        conn.commit()
        cursor.close()
        conn.close()

        return {"message": f"Les données ont été insérées avec succès à partir de {file.filename}"}
    except Exception as e:
        return {"error": str(e)}
