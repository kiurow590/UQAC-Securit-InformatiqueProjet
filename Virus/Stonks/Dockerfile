# Utiliser une image Python officielle
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires dans l'image
COPY app.py /app/

# Installer Flask
RUN pip install flask

# Créer un volume pour stocker les fichiers reçus
VOLUME ["/data"]

# Exposer le port 9002
EXPOSE 9002

# Lancer l'application
CMD ["python", "app.py"]
