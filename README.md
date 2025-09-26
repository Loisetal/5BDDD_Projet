# 5-BDDD

**Mathieu Perrot et Loïse Talluau**


# Cahier des charges

Le projet consiste à développer une API de gestion de
bibliothèque en ligne, permettant aux utilisateurs d'emprunter et de rendre des
livres, tout en gérant l'inventaire des livres et les utilisateurs inscrits. Ce projet
utilisera PostgreSQL comme base de données, Python pour la logique métier, FastAPI
pour le développement de l'API, SQLAlchemy et Alambic pour la gestion des
interactions avec la base de données et la gestion des migrations, et Pydantic pour
la validation des données.

# Démarrage 

Créer un environnement virtuel et l'activer
```bash
python -m venv venv
```

A la racine du projet, installer les libraires


Créer un environnement virtuel 
```bash
pip install -r requirements.txt
```

## Docker
A la racine de projet, lancer la commande :
```bash
docker compose up -d
```

## Appliquer les migrations Alembic
```bash
alembic upgrade head
```
Cette commande crée toutes les tables nécessaires dans la base PostgreSQL.

## Alimenter la base de données
Exécuter les requêtes du fichier Insert.sql via DBeaver pour insérer les données initiales.

## Lancer l'API 
```bash
uvicorn app.main:app --reload
```
- L’API sera accessible à : ```http://127.0.0.1:8000 ```
- La documentation Swagger se trouve sur : ```http://127.0.0.1:8000/docs```

## Tests
Exécuter les tests via :
```bash
python -m pytest tests/test_XXX.py -v    
```

## Gestion des utilisateurs dans Swagger
Pour accéder aux endpoints sécurisés :

1. **Créer un utilisateur** via `/auth/enregistrement`.  
2. **Se connecter** via `/auth/connexion` et récupérer le **token JWT** dans la réponse.  
3. Dans Swagger, cliquer sur **Authorize** (icône du cadenas en haut à droite).  
4. Entrer le token
5. Vous pouvez maintenant tester les endpoints nécessitant une authentification (création de livre, emprunt, etc.).
