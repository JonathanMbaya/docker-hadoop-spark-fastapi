import pandas as pd
import numpy as np
import os

def load_data_from_directory(directory_path):
    """
    Charge tous les fichiers CSV d'un dossier dans une liste de DataFrames.
    :param directory_path: Le chemin du dossier contenant les fichiers CSV.
    :return: Une liste de DataFrames Pandas, un pour chaque fichier CSV.
    """
    data_frames = []
    
    # Vérifier que le dossier existe
    if not os.path.exists(directory_path):
        print(f"Le dossier {directory_path} n'existe pas.")
        return data_frames
    
    # Parcourir les fichiers du dossier
    for file_name in os.listdir(directory_path):
        # Vérifier que le fichier est un CSV
        if file_name.endswith(".csv"):
            file_path = os.path.join(directory_path, file_name)
            try:
                # Charger chaque fichier CSV dans un DataFrame
                df = pd.read_csv(file_path)
                data_frames.append(df)
                print(f"Fichier {file_name} chargé.")
            except Exception as e:
                print(f"Erreur lors du chargement du fichier {file_name}: {e}")
    
    return data_frames

def load_and_concat_data_from_directory(directory_path):
    """
    Charge tous les fichiers CSV d'un dossier et les concatène en un seul DataFrame.
    :param directory_path: Le chemin du dossier contenant les fichiers CSV.
    :return: Un DataFrame Pandas contenant les données concaténées.
    """
    data_frames = load_data_from_directory(directory_path)
    
    # Si des fichiers ont été chargés, les concaténer
    if data_frames:
        return pd.concat(data_frames, ignore_index=True)
    else:
        print("Aucun fichier CSV chargé.")
        return pd.DataFrame()  # Retourner un DataFrame vide si aucun fichier n'est trouvé

def clean_column_names(df):
    """
    Renomme les colonnes pour simplifier l'accès en supprimant les espaces et en mettant en minuscules.
    """
    df.columns = df.columns.str.strip().str.lower()
    return df

def replace_missing_values(df, missing_values):
    """
    Remplace les valeurs spécifiques indiquées par `missing_values` par NaN dans le DataFrame.
    """
    df.replace(missing_values, np.nan, inplace=True)
    return df

def fahrenheit_to_celsius(temp_f):
    """
    Convertit une température en Fahrenheit en Celsius.
    """
    return (temp_f - 32) * 5.0 / 9.0

def convert_temperature_columns(df, columns):
    """
    Convertit les colonnes de températures de Fahrenheit en Celsius.
    """
    for col in columns:
        celsius_col = f"{col}"
        df[celsius_col] = df[col].apply(fahrenheit_to_celsius)
    return df

def handle_precipitations(df, prcp_column):
    """
    Gère les précipitations en remplaçant les NaN par 0.0.
    """
    df[prcp_column] = df[prcp_column].fillna(0.0)
    return df

def filter_columns(df, columns_to_keep):
    """
    Supprime toutes les colonnes autres que celles spécifiées dans `columns_to_keep`.
    """
    columns_in_df = df.columns.tolist()
    columns_to_drop = [col for col in columns_in_df if col not in columns_to_keep]
    
    # Suppression des colonnes non désirées
    df = df.drop(columns=columns_to_drop)
    
    return df

def add_id_column(df):
    """
    Ajoute une colonne 'id' incrémentée comme première colonne du DataFrame.
    :param df: Le DataFrame auquel ajouter la colonne 'id'.
    :return: Le DataFrame avec la colonne 'id' ajoutée.
    """
    # Ajouter une colonne 'id' incrémentée, commence à 1
    df['id'] = range(1, len(df) + 1)
    
    # Réorganiser les colonnes pour que 'id' soit la première
    cols = ['id'] + [col for col in df.columns if col != 'id']
    df = df[cols]
    
    return df

