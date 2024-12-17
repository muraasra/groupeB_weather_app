from flask import Flask, render_template, request, redirect, url_for, jsonify # type: ignore
import requests
from datetime import datetime
from dotenv import load_dotenv
import os
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
                request_url = f'https://api.openweathermap.org/data/2.5/weather?appid={os.getenv("API_KEY")}&q={city}&units=imperial'
                response = requests.get(request_url)
            except requests.exceptions.ConnectionError:
                error= "Connexion internet instable" 
                return render_template("home/home.html", error=error)
            if response.status_code == 404:
                error= "La ville n'a pas été trouvé" 
                return render_template("home/home.html", error=error)
                
            if response.status_code == 200:
                data = response.json()
                weather = {
                    "city": city,
                    "temperature": data["main"]["temp"],
                    "description": data["weather"][0]["description"],
                    "icon": data["weather"][0]["icon"],
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                return render_template("home/home.html", weather=weather)
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