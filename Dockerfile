# Étape 1 : Choisir l'image de base
FROM python:3.10-slim

# Étape 2 : Définir le répertoire de travail
WORKDIR /app

# Étape 3 : Copier les fichiers requirements.txt et installer les dépendances
COPY requirements.txt /app/

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Étape 4 : Copier le code de l'application
COPY . /app/

# Étape 5 : Exposer le port sur lequel l'application va tourner
EXPOSE 8000

# Étape 6 : Lancer l'application avec la commande Django runserver
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]