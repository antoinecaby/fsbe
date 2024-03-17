# fsbe

Projet Full-Stack Back-End

# Documentation

Une documentation est automatiquement disponible à localhost:port/docs ou /redocs. Par défaut le domaine est localhost sur le port 80.

# Prérequis

Avant de pouvoir lancer l'application il faut que vous ayez installé :

- Docker Desktop : https://www.docker.com/products/docker-desktop/
- DB Browser for SQLite : https://sqlitebrowser.org/dl/
- Python : https://www.python.org/downloads/

# Lancer le projet

1. Lancer l'application Docker

2. Supprimer le fichier fsbe.db dans app/db si déjà existant (c'est le fichier de la base de donnée, il est généré automatiquement au lancement du projet)

3. Ouvrir un terminal de commande et effectuer les commandes suivantes

   - poetry install
   - docker compose up --build

4. Lancez l'application DB Browser for SQLite et ouvrez le fichier app/db/fsbe qui vient d'être généré par "docker-compose up --build"
