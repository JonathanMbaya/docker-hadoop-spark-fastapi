from fastapi import FastAPI
from pyspark.sql import SparkSession

app = FastAPI()

# Créer une session Spark et se connecter au Spark Master
spark = SparkSession.builder \
    .appName("FastAPI-Spark") \
    .master("spark://spark-master:7077") \  # Connexion à Spark Master
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:8020") \  # Connexion HDFS
    .getOrCreate()

@app.get("/data")
async def get_data():
    # Lire les données depuis HDFS
    df = spark.read.csv("hdfs://namenode:8020/path/to/file.csv", header=True)

    # Appliquer une transformation (ex. sélectionner les 10 premières lignes et quelques colonnes)
    df_filtered = df.select("column1", "column2").limit(10)

    # Retourner les résultats sous forme de liste de dictionnaires (récupéré avec collect())
    data = df_filtered.collect()

    # Convertir chaque ligne en dictionnaire pour un format JSON
    result = [{"column1": row["column1"], "column2": row["column2"]} for row in data]
    
    return {"data": result}