from pyspark.sql import SparkSession

def insert_csv_files_to_hdfs():
    try:
        # Créer une session Spark
        spark = SparkSession.builder \
            .appName("Insert CSV Files into HDFS") \
            .config("spark.hadoop.fs.defaultFS", "http://localhost:9870") \
            .getOrCreate()

        # Chemin vers le dossier local contenant les fichiers CSV
        local_csv_directory = "/app/data/processed_gsod/*.csv"  # Utilisez un chemin générique pour tous les CSV dans le dossier

        # Lire tous les fichiers CSV du dossier dans un DataFrame Spark
        df = spark.read.csv(local_csv_directory, header=True, inferSchema=True)

        # Chemin cible dans HDFS pour sauvegarder les fichiers CSV
        hdfs_target_path = "hdfs://namenode:9000/gsod/"

        # Écrire les données dans HDFS
        df.write.csv(hdfs_target_path, header=True, mode="overwrite")  # 'mode="overwrite"' pour écraser les fichiers existants

        print(f"Tous les fichiers CSV du dossier {local_csv_directory} ont été insérés dans HDFS à {hdfs_target_path}")
        
        # Arrêter Spark
        spark.stop()

    except Exception as e:
        print(f"Erreur : {e}")

# Appeler la fonction
insert_csv_files_to_hdfs()
