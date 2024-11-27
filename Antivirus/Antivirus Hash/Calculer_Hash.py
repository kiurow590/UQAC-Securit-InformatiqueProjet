import hashlib

def get_file_hash(file_path):
    """
    Calcule le hash SHA-256 d'un fichier.
    :param file_path: Chemin du fichier
    :return: Hash SHA-256 du fichier sous forme de chaîne hexadécimale
    """
    try:
        sha256_hash = hashlib.sha256()
        # Lecture en mode binaire
        with open(file_path, "rb") as f:
            # Lire par blocs de 4096 octets pour éviter les problèmes de mémoire
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        print(f"Erreur : Le fichier {file_path} est introuvable.")
        return None
    except Exception as e:
        print(f"Erreur : {e}")
        return None


if __name__ == "__main__":
    file_path = input("Entrez le chemin du fichier .exe à vérifier : ").strip()
    file_hash = get_file_hash(file_path)

    if file_hash:
        print(f"Hash SHA-256 du fichier '{file_path}' : {file_hash}")
    else:
        print("Impossible de calculer le hash.")
