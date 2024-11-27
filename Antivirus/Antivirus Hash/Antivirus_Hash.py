import os
import hashlib
import mysql.connector
from mysql.connector import Error
import logging
import subprocess

# Configuration des logs
logging.basicConfig(
    filename="logs/file_execution.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Configuration pour la connexion sécurisée
db_config = {
    'user': 'nouvel_utilisateur',
    'password': 'MotDePasse_123!',
    'host': '172.19.8.80',  # Adresse IP de WSL
    'database': 'BDD_Antivirus',
    'port': 3306,
    'ssl_ca': 'certs/ca-cert.pem',
    'ssl_cert': 'certs/client-cert.pem',
    'ssl_key': 'certs/client-key.pem'
}


def convert_windows_path_to_wsl(path):
    """
    Convertit un chemin Windows en chemin compatible WSL.
    """
    if path.startswith("\\\\wsl.localhost\\Ubuntu\\"):
        converted_path = path.replace("\\\\wsl.localhost\\Ubuntu\\", "/").replace("\\", "/")
        print(f"Chemin converti pour WSL : {converted_path}")
        return converted_path
    return path


def get_file_hash(file_path):
    """
    Calcule le hash SHA-256 d'un fichier.
    """
    try:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        logging.error(f"Le fichier {file_path} est introuvable.")
        print(f"Erreur : Le fichier {file_path} est introuvable.")
        return None
    except Exception as e:
        logging.error(f"Erreur lors du calcul du hash pour {file_path} : {e}")
        print(f"Erreur lors du calcul du hash pour {file_path} : {e}")
        return None


def check_file_in_db(file_hash):
    """
    Vérifie si le hash du fichier existe dans la base de données.
    """
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Vérification du fichier dans la base
        query = "SELECT description FROM Hash_256 WHERE file_hash = %s"
        cursor.execute(query, (file_hash,))
        result = cursor.fetchone()
        if result:
            return {"status": "blocked", "description": result["description"]}
        else:
            return {"status": "allowed"}
    except Error as e:
        logging.error(f"Erreur lors de la connexion à la base de données : {e}")
        print(f"Erreur lors de la connexion à la base de données : {e}")
        return {"status": "error", "message": str(e)}
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()


def block_execution(file_path):
    """
    Change l'extension du fichier pour empêcher son exécution.
    """
    try:
        # Ajouter une extension pour rendre le fichier non exécutable
        new_path = file_path + ".blocked"
        os.rename(file_path, new_path)
        print(f"Extension changée : {file_path} -> {new_path}")
        logging.info(f"Extension changée pour bloquer l'exécution : {file_path} -> {new_path}")
    except FileNotFoundError:
        print(f"Erreur : Le fichier spécifié est introuvable ({file_path}).")
        logging.error(f"Le fichier spécifié est introuvable : {file_path}")
    except Exception as e:
        print(f"Erreur inattendue lors du changement d'extension : {e}")
        logging.error(f"Erreur inattendue lors du changement d'extension pour {file_path} : {e}")


def execute_file(file_path):
    """
    Vérifie le hash du fichier avant de l'exécuter.
    Si malveillant, les permissions d'exécution sont révoquées.
    """
    # Convertir le chemin si nécessaire
    file_path = convert_windows_path_to_wsl(file_path)
    print(f"Chemin converti pour WSL : {file_path}")

    """
    # Vérification explicite avec os.path.exists
    print(f"Vérification du chemin (Python) : {os.path.exists(file_path)}")
    logging.info(f"Vérification du chemin : {file_path}")
    """

    # Vérification du fichier
    if not os.path.exists(file_path):
        print(f"Erreur : {file_path} n'existe pas ou n'est pas un fichier exécutable.")
        logging.error(f"Fichier invalide ou introuvable : {file_path}")
        return

    # Calcul du hash
    file_hash = get_file_hash(file_path)
    if not file_hash:
        print("Erreur : Impossible de calculer le hash du fichier.")
        return

    # Affichage du hash calculé
    print(f"Hash SHA-256 du fichier : {file_hash}")

    # Vérification dans la base de données
    result = check_file_in_db(file_hash)
    if result["status"] == "blocked":
        print(f"ALERTE : Ce fichier est identifié comme malveillant et ne peut pas être exécuté.")
        print(f"Raison : {result['description']}")
        logging.warning(f"Exécution bloquée pour {file_path} : {result['description']}")
        # Révoquer les permissions d'exécution
        block_execution(file_path)
    elif result["status"] == "allowed":
        print(f"Le fichier est autorisé à être exécuté.")
        logging.info(f"Fichier autorisé : {file_path}")
    else:
        print(f"Erreur lors de la vérification de la base de données : {result['message']}")




def main():
    """
    Programme principal pour vérifier et exécuter un fichier.
    """
    while True:
        file_path = input("\nEntrez le chemin complet du fichier exécutable à vérifier (ou 'q' pour quitter) : ")

        if file_path.lower() == 'q':
            print("Programme terminé.")
            break

        execute_file(file_path)


if __name__ == "__main__":
    main()
