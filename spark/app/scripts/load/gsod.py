import os
from tqdm import tqdm
from hdfs import InsecureClient  # Assurez-vous que vous utilisez la bonne bibliothèque HDFS

GSOD_PROCESSED_DIR = "/app/data/processed_gsod"  # Dossier local contenant les fichiers traités

def load_gsod_to_hadoop():
    # Créer un client HDFS
    hdfs_client = InsecureClient('http://localhost:9870', user='root')
    
    # Définir le répertoire de destination dans HDFS
    hdfs_base_dir = "/gsod"  # Répertoire de base dans HDFS pour les fichiers CSV

    # Créer le répertoire HDFS si nécessaire
    try:
        if not hdfs_client.status(hdfs_base_dir, strict=False):
            hdfs_client.makedirs(hdfs_base_dir)
            print(f"Répertoire {hdfs_base_dir} créé avec succès dans HDFS.")
    except Exception as e:
        print(f"Erreur lors de la création du répertoire de base {hdfs_base_dir}: {e}")
        return  # Si la création du répertoire échoue, arrêter la fonction

    # Parcours des fichiers dans le répertoire local
    for file in tqdm(os.listdir(GSOD_PROCESSED_DIR), desc="Chargement des GSOD dans HDFS", unit="fichier"):
        local_file_path = os.path.join(GSOD_PROCESSED_DIR, file)

        # Vérifie si c'est un fichier CSV
        if os.path.isfile(local_file_path) and file.endswith("all_years.csv"):
            hdfs_file_path = os.path.join(hdfs_base_dir, file)  # Chemin complet de destination dans HDFS

            try:
                # Charger le fichier CSV dans HDFS
                hdfs_client.upload(hdfs_file_path, local_file_path)
                print(f"Fichier {file} chargé avec succès vers HDFS sous {hdfs_file_path}")
            except Exception as e:
                print(f"Erreur lors du chargement du fichier {file} vers HDFS: {e}")
