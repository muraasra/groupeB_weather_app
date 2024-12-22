
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
 
@app.route("/download_history")
def download_history():
    try:
        #Load search history from JSON
        with open("search_history.json", "r") as file:
            search_history=json.load(file)
    except(FileNotFoundError, json.JSONDecodeError):
        search_history=[]
    #Create CSV in memory
    output= io.StringIO()
    writer=csv.writer(output)
    #Write CSV headers
    writer.writerow(["Ville", "Temperature ","Description","Date et Heure"])
    
    #Write each entry in the CSV
    for entry in search_history:
        weather_data = entry["weather"]
        writer.writerow([entry["city"], weather_data["temperature"], weather_data["description"], entry["timestamp"]])
        
    output.seek(0)

    #serve CSV as a response
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename= historique.csv"}
    )


#@app.route("/weather", methods=["GET", "POST"])
@app.route("/notuse", methods=["GET", "POST"])
def get_weather_data(city):
    API_KEY="02aacefe86b70d9accb3ee543d9b982b"
    API_URL="http://api.openweathermap.org/data/2.5/weather"

    params={
        "q":city,
        "appid": API_KEY,
        "units": "metric", #celsius
        "lang": "en" #language
    }

    try:
        #send the GET request to the OpenWeather API
        response=requests.get(API_URL,params=params)

        #Check if the response is successful
        if response.status_code==200:
            return response.json()# Return weather data as dictionary
        else:
            return None #handle cases when city is not found or an error occurs
    except Exception as e:
        print(f"Error fetching weather data:{e}")
        return None
    
def index():
    if request.method =="POST":
        city = request.form.get("city")
        weather_data= get_weather_data("city") #Function to fetch weather data
        if weather_data:
            #Extract necessary fields from the weather data
            #temperature= weather_data["main"]["temp"]
            #weather_description=weather_data["weather"][0]["description"]

            save_search(city, weather_data)# save the search
        return render_template("index.html", weather=weather_data , city=city)
        #return render_template("index.html", error="City not found or API error" , city=city)
    return render_template("index.html")

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
                save_search(city,weather)
                # Recuperer les previsions des prochain 7 jours 
                # lat = data['coord']['lat']
                # lon = data['coord']['lon']
                
                # # forecast_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={os.getenv("API_KEY")}"
                # forecast_url=f"http://pro.openweathermap.org/data/2.5/weather?q=London,uk&APPID=386218d81396d399cc00cf098a429bb1"
                # # forecast_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts&units=metric&appid={os.getenv("API_KEY")}"
                # forecast_response = requests.get(forecast_url)
                # pdb.set_trace()                
                # if forecast_response.status_code == 200:
                    
                #     forecast_data = forecast_response.json()['daily']  # Prévisions 7 jours
                
               
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