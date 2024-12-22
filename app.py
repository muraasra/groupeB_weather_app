
from flask import Flask, render_template, request, redirect, url_for, jsonify , Response# type: ignore
import requests
from datetime import datetime
from dotenv import load_dotenv
import os
import pdb
import json
import csv
import io

load_dotenv()


app = Flask(__name__)

#Affichage de L'historique
@app.route("/history")
def history():
    try:
        with open("search_history.json","r") as file:
            search_history=json.load(file)
    except (FileNotFoundError,json.JSONDecodeError):
        search_history=[]
    return render_template('history/history.html', searches=search_history)	

def save_search(city,weather_data):
    #Structure of the entry to save
    search_entry={
        "city":city,
       # "temperature": temperature,
        "weather": weather_data,
        "timestamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    #Read existing history or initialize an empty list
    try:
        with open("search_history.json", "r") as file:
            search_history= json.load(file)
    except(FileNotFoundError,json.JSONDecodeError):
        search_history=[]
        
    #Add the new search at the beginning of the list
    search_history.insert(0, search_entry)
    #Save the updated history back to the file
    with open ("search_history.json", "w") as file:
        json.dump(search_history,file,indent=4)

@app.route('/clear_history', methods=['POST'])
def clear_history():
    # Vide le fichier search_history.json en réécrivant un tableau vide
    with open("search_history.json", "w") as file:
        json.dump([], file, indent=4)
    
    # Redirige l'utilisateur vers la page d'historique après avoir vidé l'historique
    return redirect(url_for('history'))

 
@app.route("/download_history")

def download_history():
    try:
        # Charger l'historique des recherches
        with open("search_history.json", "r") as file:
            search_history = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        search_history = []

    # Vérifier si l'historique est vide
    if not search_history:
        error = "Aucune recherche dans l'historique. Impossible de télécharger."
        return render_template("history/history.html", error=error)
    
    # Créer un CSV en mémoire
    output = io.StringIO()
    writer = csv.writer(output, delimiter="|", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    
    # Ajouter les entêtes au fichier CSV
    writer.writerow(["Ville", "Temperature", "Description", "Date et Heure"])
    writer.writerow([])

    # Ajouter chaque entrée de l'historique
    table_data = []
    for entry in search_history:
        weather_data = entry["weather"]
        row = [
            entry["city"],
            weather_data.get("temperature", "N/A"),
            weather_data.get("description", "N/A"),
            entry["timestamp"]
        ]
        writer.writerow(row)
        table_data.append({
            "city": entry["city"],
            "temperature": weather_data.get("temperature", "N/A"),
            "description": weather_data.get("description", "N/A"),
            "timestamp": entry["timestamp"]
        })

    output.seek(0)

    # Créer l'option de téléchargement du fichier CSV
    return Response(
        output.getvalue().encode("utf-8-sig"),  # Encodage UTF-8 avec BOM
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=historique.csv"}
    )



@app.route("/", methods=["GET", "POST"])

def get_weather():
    if request.method == "POST":
            city = request.form.get("city")
            try:
                request_url = f'https://api.openweathermap.org/data/2.5/weather?appid={os.getenv("API_KEY")}&q={city}&units=metric&lang=fr'
                response = requests.get(request_url)
            except requests.exceptions.ConnectionError:
                error= "Connexion internet instable" 
                return render_template("home/home.html", error=error)
            if response.status_code == 404:
                error= "La ville n'a pas été trouvé" 
                return render_template("home/home.html", error=error)
                
            if response.status_code == 200:
                data = response.json()                
                # Recuperer les prevision du jour
                weather = {
                    "city": city,
                    "temperature": data["main"]["temp"],
                    "description": data["weather"][0]["description"],
                    "icon": data["weather"][0]["icon"],
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'country': data['sys']['country'],
                    'feels_like': data['main']['feels_like'],
                    'pressure': data['main']['pressure'],
                    'humidity': data['main']['humidity'],
                    'wind_speed': data['wind']['speed'],
                    'wind_direction': data['wind']['deg'],
                    'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M'),
                    'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M'),
                    'condition': data['weather'][0]['description'].title(),
                    'icon': data['weather'][0]['icon']
                }
                # enregistrer l'historique
                save_search(city,weather)
                
                
               
                return render_template("home/home.html", weather=weather,response=response.json(), city=city)
            else:
                error = "Ville non trouvée ou problème API."
                return render_template("home/home.html", error=error)
    return render_template("home/home.html",welcome="Bienvenue sur notre application météo ! Découvrez en un clic les prévisions détaillées de votre ville.")
    
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=8080)

def main():
    # print("Hello, world!")
    if __name__ == "__main__":
        main()