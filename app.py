from flask import Flask, request, jsonify, render_template
import requests
from datetime import datetime

app = Flask(__name__)

# Weather API Details
BASE_URL = "https://api.weatherapi.com/v1/current.json?"
API_KEY = "edddd5aeaba8424f88595759251602"

def calculate_fire_risk(temp, humidity, wind_speed):
    """Calculates wildfire risk based on temperature, humidity, and wind speed."""
    risk_percentage = (temp * 0.4) + ((100 - humidity) * 0.3) + (wind_speed * 0.3)
    return round(risk_percentage, 2)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_risk", methods=["POST"])
def get_risk():
    city = request.form["location"]
    url = f"{BASE_URL}key={API_KEY}&q={city}"
    
    response = requests.get(url).json()

    if "current" in response:
        temp = response["current"]["temp_c"]
        humidity = response["current"]["humidity"]
        wind_speed = response["current"]["wind_kph"]
        feels_like = response["current"]["feelslike_c"]
        location = response["location"]["name"]
        country = response["location"]["country"]
        local_time = response["location"]["localtime"]

        # Calculate wildfire risk
        risk = calculate_fire_risk(temp, humidity, wind_speed)

        return jsonify({
            "location": f"{location}, {country}",
            "date_time": local_time,
            "temperature": temp,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "feels_like": feels_like,
            "risk_percentage": risk
        })
    
    return jsonify({"error": "Invalid city or API issue"})

if __name__ == "__main__":
    app.run(debug=True)