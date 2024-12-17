
from flask import Flask, render_template, request, redirect, url_for, jsonify # type: ignore
import requests
from datetime import datetime
from dotenv import load_dotenv
import os
import pdb
load_dotenv()


app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home/home.html')

@app.route("/history")
def history():
    return render_template('history/history.html')	

@app.route("/weather", methods=["GET", "POST"])
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
    return render_template("home/home.html",test="test")
    
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=8080)

def main():
    # print("Hello, world!")
    if __name__ == "__main__":
        main()