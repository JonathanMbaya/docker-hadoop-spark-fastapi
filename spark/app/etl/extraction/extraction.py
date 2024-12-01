import requests
import os
import pandas as pd

def download_weather_data(start_year, end_year, station_id, output_dir):
    """
    Télécharge les fichiers CSV de données météorologiques pour une plage d'années.
    
    :param start_year: Année de début (ex: 2019)
    :param end_year: Année de fin (ex: 2023)
    :param station_id: ID de la station météo (ex: 07156099999)
    :param output_dir: Dossier de sauvegarde pour les fichiers téléchargés
    """
    # Assurez-vous que le dossier de sortie existe
    os.makedirs(output_dir, exist_ok=True)
    
    base_url = "https://www.ncei.noaa.gov/data/global-summary-of-the-day/access/{year}/{station_id}.csv"
    
    for year in range(start_year, end_year + 1):
        url = base_url.format(year=year, station_id=station_id)
        output_file = os.path.join(output_dir, f"{station_id}_{year}.csv")
        
        print(f"Téléchargement des données pour l'année {year}...")
        
        response = requests.get(url)
        if response.status_code == 200:  # Vérifie si le fichier existe
            with open(output_file, "wb") as f:
                f.write(response.content)
            print(f"Fichier sauvegardé : {output_file}")
        else:
            print(f"Échec du téléchargement pour l'année {year}. Statut HTTP : {response.status_code}")



# Télécharger un fichier CSV de données météorologiques
url = "https://www.ncei.noaa.gov/data/global-summary-of-the-day/access/{year}/07156099999.csv"
response = requests.get(url)

# Sauvegarder le fichier localement
with open("weather_data.csv", "wb") as f:
    f.write(response.content)


# Charger les données CSV dans un DataFrame
def load_data(folder_path):
    """
    Charge tous les fichiers CSV d'un dossier et combine les données dans un seul DataFrame.
    """
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Le dossier spécifié n'existe pas : {folder_path}")

    # Liste des fichiers CSV dans le dossier
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    if not csv_files:
        raise FileNotFoundError(f"Aucun fichier CSV trouvé dans le dossier : {folder_path}")

    print(f"Fichiers CSV trouvés : {csv_files}")

    # Lire et concaténer tous les fichiers CSV
    dfs = []
    for file in csv_files:
        file_path = os.path.join(folder_path, file)
        print(f"Chargement du fichier : {file_path}")
        dfs.append(pd.read_csv(file_path))

    # Combinaison de tous les DataFrames
    combined_df = pd.concat(dfs, ignore_index=True)
    print(f"Nombre total de lignes après combinaison : {len(combined_df)}")
    return combined_df

def inspect_data(df):
    print("Aperçu des données :")
    print(df.head())
    print("\nInformations générales :")
    print(df.info())
    print("\nStatistiques descriptives :")
    print(df.describe())