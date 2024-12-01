import os
import pandas as pd
import os
from tqdm import tqdm

from pyspark.sql import SparkSession


def spark_to_hadoop(filepath):

    # Créer une session Spark
    spark = SparkSession.builder.appName('UploadToHDFS').getOrCreate()

    # Charger le fichier CSV dans un DataFrame Spark
    df = spark.read.csv( filepath, header=True, inferSchema=True)

    # Sauvegarder le DataFrame dans HDFS
    df.write.csv('hdfs://namenode:9000/', header=True)




def save_to_csv(df, output_folder_path, year):
    """
    Sauvegarde le DataFrame en fichier CSV dans le dossier spécifié pour une année donnée.
    :param df: Le DataFrame à sauvegarder
    :param output_folder_path: Le dossier où sauvegarder le fichier
    :param year: L'année pour le nom du fichier CSV
    """
    os.makedirs(output_folder_path, exist_ok=True)  # Crée le dossier s'il n'existe pas
    file_name = f"weather_data_{year}.csv"  # Nom du fichier basé sur l'année
    output_file = os.path.join(output_folder_path, file_name)

    # Sauvegarder le DataFrame en CSV
    df.to_csv(output_file, index=False)  # Ne pas inclure l'index dans le fichier CSV
    print(f"\nDonnées sauvegardées dans {output_file}")


# Fonction pour sauvegarder les données en fichier JSON
def save_to_json(df, output_folder_path, year):
    """
    Sauvegarde le DataFrame en fichier JSON dans le dossier spécifié pour une année donnée.
    :param df: Le DataFrame à sauvegarder
    :param output_folder_path: Le dossier où sauvegarder le fichier
    :param year: L'année pour le nom du fichier JSON
    """
    os.makedirs(output_folder_path, exist_ok=True)
    file_name = f"weather_data_{year}.json"  # Nom du fichier basé sur l'année
    output_file = os.path.join(output_folder_path, file_name)
    
    # Convertir le DataFrame en JSON
    df.to_json(output_file, orient="records", indent=4)
    print(f"\nDonnées sauvegardées dans {output_file}")

def process_csv_files(input_folder, output_folder):
    """
    Convertit chaque fichier CSV d'un dossier en fichier JSON correspondant.
    :param input_folder: Chemin du dossier contenant les fichiers CSV.
    :param output_folder: Chemin du dossier où sauvegarder les fichiers JSON.
    """
    # Vérifier l'existence du dossier d'entrée
    if not os.path.exists(input_folder):
        print(f"Le dossier d'entrée {input_folder} n'existe pas.")
        return
    
    # Parcourir les fichiers CSV
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".csv"):
            csv_file_path = os.path.join(input_folder, file_name)
            try:
                # Charger le fichier CSV
                df = pd.read_csv(csv_file_path)
                
                # Sauvegarder en JSON
                json_file_name = file_name.rsplit(".", 1)[0]  # Retirer l'extension .csv
                save_to_json(df, output_folder, json_file_name)
            except Exception as e:
                print(f"Erreur lors du traitement du fichier {file_name} : {e}")




def load_gsod_to_hadoop(hdfs_client, GSOD_PROCESSED_DIR):
    for year in tqdm(os.listdir(GSOD_PROCESSED_DIR), desc="Chargement des GSOD dans HDFS", unit="fichier"):
        year_dir = os.path.join(GSOD_PROCESSED_DIR, year)

        if os.path.isdir(year_dir):
            hdfs_year_dir = f"/gsod/{year}"

            try:
                if not hdfs_client.status(hdfs_year_dir, strict=False):
                    hdfs_client.makedirs(hdfs_year_dir)
            except Exception as e:
                print(f"Erreur lors de la création du répertoire {hdfs_year_dir}: {e}")
                continue

            # Charger les fichiers CSV dans HDFS
            for file in os.listdir(year_dir):
                if file.endswith("_cleaned.csv"):
                    local_file_path = os.path.join(year_dir, file)
                    hdfs_file_path = os.path.join(hdfs_year_dir, file)

                    try:
                        hdfs_client.upload(hdfs_file_path, local_file_path)
                        print(f"Fichier {file} chargé vers HDFS sous {hdfs_file_path}")
                    except Exception as e:
                        print(f"Erreur lors du chargement du fichier {file} vers HDFS: {e}")


