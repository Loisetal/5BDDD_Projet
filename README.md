# 5-BDDD

Mathieu Perrot et Loïse Talluau 


# Cahier des charges

Le projet consiste à développer une API de gestion de
bibliothèque en ligne, permettant aux utilisateurs d'emprunter et de rendre des
livres, tout en gérant l'inventaire des livres et les utilisateurs inscrits. Ce projet
utilisera PostgreSQL comme base de données, Python pour la logique métier, FastAPI
pour le développement de l'API, SQLAlchemy et Alambic pour la gestion des
interactions avec la base de données et la gestion des migrations, et Pydantic pour
la validation des données.

# Démarrage 

Mettre en place d'un environnement virtuel et l'activer

## Docker

A la racine de projet, lancer la commande "docker compose up -d"

alembic upgrade head