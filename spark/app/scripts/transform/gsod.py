import os
import pandas as pd
from tqdm import tqdm

# Chemin du dossier contenant les fichiers CSV
GSOD_RAW_DIR = "../app/data"  # Dossier où sont les fichiers bruts (CSV)
OUTPUT_DIR = "../app/data/processed_gsod"  # Dossier où les fichiers traités seront sauvegardés

# Fonction pour concaténer tous les fichiers CSV d'un dossier en une seule DataFrame
def concat_csv_files_from_folder(folder_path):
    """
    Cette fonction lit tous les fichiers CSV d'un dossier et les concatène dans une seule DataFrame.
    :param folder_path: Le chemin du dossier contenant les fichiers CSV
    :return: Une DataFrame contenant toutes les données concaténées
    """
    all_data = []

    # Liste les fichiers CSV dans le dossier
    files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]
    if not files:
        print(f"Aucun fichier CSV trouvé dans le dossier {folder_path}.")
        return None

    # Lire chaque fichier CSV et l'ajouter à la liste all_data
    for file in tqdm(files, desc="Chargement des fichiers CSV", unit="fichier"):
        file_path = os.path.join(folder_path, file)
        try:
            df = pd.read_csv(file_path)
            all_data.append(df)
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier {file}: {e}")
    
    # Concaténer toutes les DataFrame lues
    combined_df = pd.concat(all_data, ignore_index=True)
    return combined_df

# Fonction de traitement des données (exemple ici : nettoyage des colonnes)
def process_data(df):
    """
    Traite et nettoie la DataFrame. Exemple de traitement : suppression des colonnes inutiles et renaming.
    :param df: La DataFrame à traiter
    :return: La DataFrame traitée
    """
    # Exemple de traitement : garder certaines colonnes et renommer
    columns_to_keep = ["STATION", "DATE", "TEMP", "DEWP", "WDSP", "PRCP"]
    
    if all(col in df.columns for col in columns_to_keep):
        df = df[columns_to_keep]
    else:
        print(f"Certaines colonnes sont manquantes dans les données. Colonnes disponibles : {df.columns}")

    # Renommer les colonnes pour correspondre à un format plus lisible
    df.columns = ["station", "date", "temp", "dew_point", "wind_speed", "precipitation"]
    
    # Supprimer les lignes avec des valeurs manquantes
    df = df.dropna()
    
    return df

# Fonction pour sauvegarder la DataFrame traitée en CSV
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

# Fonction pour sauvegarder la DataFrame traitée en JSON
# def save_to_json(df, output_folder_path, year):
#     """
#     Sauvegarde le DataFrame en fichier JSON dans le dossier spécifié pour une année donnée.
#     :param df: Le DataFrame à sauvegarder
#     :param output_folder_path: Le dossier où sauvegarder le fichier
#     :param year: L'année pour le nom du fichier JSON
#     """
#     os.makedirs(output_folder_path, exist_ok=True)
#     file_name = f"weather_data_{year}.json"  # Nom du fichier basé sur l'année
#     output_file = os.path.join(output_folder_path, file_name)
    
#     # Convertir le DataFrame en JSON
#     df.to_json(output_file, orient="records", indent=4)
#     print(f"\nDonnées sauvegardées dans {output_file}")

# Fonction principale pour traiter les fichiers d'un dossier et sauvegarder les résultats
def process_and_save_data():
    # Concatenate all CSV files from the folder into one DataFrame
    combined_df = concat_csv_files_from_folder(GSOD_RAW_DIR)
    
    if combined_df is not None:
        # Appliquer un traitement à la DataFrame
        processed_df = process_data(combined_df)
        
        # Enregistrer la DataFrame traitée en CSV et JSON
        save_to_csv(processed_df, OUTPUT_DIR, "all_years")
        # save_to_json(processed_df, OUTPUT_DIR, "all_years")


