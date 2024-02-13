# Utiliser une image de base Python
FROM python:3.10

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de dépendances et installer les packages
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier tous les autres fichiers et dossiers de l'application
COPY app .

# Commande pour lancer l'application
CMD ["python", "./main.py"]
