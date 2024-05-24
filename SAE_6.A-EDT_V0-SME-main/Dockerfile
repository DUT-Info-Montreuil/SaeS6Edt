# Utilisez une image Alpine avec Python
FROM python:3.11.4-alpine

# Définissez un répertoire de travail dans le conteneur
WORKDIR /app

# Copiez les fichiers de votre projet dans le conteneur
COPY . /app

# Installez les dépendances de votre projet
RUN pip install --no-cache-dir -r requirements.txt

# Définissez une variable d'environnement pour Flask
ENV FLASK_APP=app.py

# Indiquez à Flask de fonctionner en mode de développement (facultatif)
ENV FLASK_ENV=development
ENV DATABASE_URL=mysql+mysqlconnector://courroux:root@db/courroux 

# Commande pour démarrer votre application Flask
CMD ["flask", "run", "--host=0.0.0.0"]