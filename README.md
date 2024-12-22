### Application Météo avec Flask et OpenWeather API

Ce projet est une application web simple permettant de consulter les informations météorologiques actuelles d'une ville, de sauvegarder l'historique des recherches et de le télécharger au format CSV.

## Fonctionnalités
- Recherche de météo : Récupération des informations météorologiques actuelles d'une ville via l'API OpenWeather.
- Gestion des erreurs : Messages d'erreur clairs en cas de ville introuvable ou de problème API.
- Historique des recherches : Sauvegarde des recherches dans un fichier JSON et affichage sur une page dédiée.
- Téléchargement CSV : Exportation de l'historique sous forme de fichier CSV.

## Prérequis
- Python 3.8 ou supérieur
- Flask (framework Python)
- Une clé API OpenWeather (disponible sur [OpenWeather](https://openweathermap.org/api)) 
    (Cependant nous avons une clé gratuite directement disponible dans ce repos)

## Installation
1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/votre-utilisateur/nom-du-repo.git
   cd nom-du-repo
## Configuration
1. Installez les dependances : 
    Creer l'environnement virtuel : 
    ```bash
    python -m venv venv 
2. L'activer :
    ```bash
    .\venv\scripts\activate (sur windows)
3. Installer les dependances
    ```bash
    pip install -r requierements.txt
4. Lancer l'Appication avec : python app.py et connectez vous sur l'adrrese :
    127.0.0.1:8080
