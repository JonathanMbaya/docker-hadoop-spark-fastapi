from hdfs import InsecureClient
from extraction.extraction import (inspect_data)
from transformation.transformation import (
    load_data_from_directory,
    load_and_concat_data_from_directory,
    clean_column_names,
    replace_missing_values,
    # fahrenheit_to_celsius,
    convert_temperature_columns,
    # normalize_dates,
    handle_precipitations,
    filter_columns,
    add_id_column
)
from loading.loading import (save_to_csv,save_to_json,process_csv_files,load_gsod_to_hadoop)


def main():

    start_year = 2019
    end_year = 2023  # Année actuelle ou dernière année de données disponibles
    # station_id = "07156099999"
    # output_dir = "./data/download_data"  # Dossier pour les fichiers CSV téléchargés

    # # Télécharger les données
    # download_weather_data(start_year, end_year, station_id, output_dir)

    """
    Pipeline principal pour nettoyer et transformer les données météo.
    """
    input_folder_path  = "./data/download_data"
    output_folder_path_json = "./loaded_files/json/"
    output_folder_path_csv = "./loaded_files/csv/"


    try:
        # Étape 1 : Charger les données
        df = load_data_from_directory(input_folder_path)
        df = load_and_concat_data_from_directory(input_folder_path)

        # Étape 2 : Inspection des données
        inspect_data(df)

        # Étape 3 : Renommer les colonnes
        df = clean_column_names(df)

        # Étape 4 : Remplacer les valeurs manquantes
        missing_values = {
            'temp': 9999.9,
            'dewp': 9999.9,
            'slp': 9999.9,
            'stp': 9999.9,
            'visib': 999.9,
            'wdsp': 999.9,
            'mxspd': 999,
            'gust': 999.9,
            'max': 9999.9,
            'min': 9999.9,
            'prcp': 99.99,
            'sndp': 999.9,
        }
        df = replace_missing_values(df, missing_values)

        # Étape 5 : Conversion des températures
        temp_f = ['temp', 'max', 'min', 'dewp']
        df = convert_temperature_columns(df, temp_f)

        # Étape 6 : Normalisation des dates
        # df = normalize_dates(df, 'date')

        # Étape 7 : Gestion des précipitations
        df = handle_precipitations(df, 'prcp')

        # Étape  8 : Filtrage des colonnes à conserver
        columns_to_keep = [
            'name','longitude', 'latitude','temp', 'max', 'min', 'prcp',
            'elevation', 'visib', 'wdsp', 'date'
        ]

        df = filter_columns(df, columns_to_keep)  # Filtrage des colonnes

        df = add_id_column(df)

        # Étape 10 : Sauvegarde au format JSON
        save_to_csv(df, output_folder_path_csv, year=[start_year,end_year])
        save_to_json(df, output_folder_path_json, year=[start_year,end_year])

        # Étape 11 : Vérification du fichier JSON sauvegardé
        process_csv_files(input_folder_path, output_folder_path_json)

        # Paramètres de connexion PostgreSQL
        # db_params = {
        #     "host": "localhost",
        #     "database": "weather_data",
        #     "user": "postgres",
        #     "password": "admin"
        # }

        # # insert_json_to_postgres(output_folder_path, db_params)

        # load_storm_events_to_hadoop(hdfs_client)
        hdfs_client = InsecureClient('hdfs://namenode:9000', user='root')
        GSOD_PROCESSED_DIR = "./loaded_files/"

        load_gsod_to_hadoop(hdfs_client, GSOD_PROCESSED_DIR)


    except Exception as e:
        print(f"Erreur dans le pipeline : {e}")


# Exécuter le pipeline principal
if __name__ == "__main__":
    main()
