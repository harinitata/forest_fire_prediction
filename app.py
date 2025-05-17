from flask import Flask, request, jsonify, render_template
import requests
from datetime import datetime
import joblib  # Import joblib

app = Flask(__name__)

# Load the trained Random Forest model
try:
    model = joblib.load('fire_prediction_model.joblib')
    print("Trained model loaded successfully.")
except Exception as e:
    model = None
    print(f"Error loading the model: {e}")

# Weather API Details (same as before)
BASE_URL = "https://api.weatherapi.com/v1/current.json?"
API_KEY = ""


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

@app.route("/predict_risk_coords", methods=["GET"])
def predict_risk_coords():
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)

    if lat is None or lon is None:
        return jsonify({"error": "Latitude and longitude parameters are required"}), 400

    url = f"{BASE_URL}key={API_KEY}&q={lat},{lon}"
    response = requests.get(url).json()

    if "current" in response:
        temp_c = response["current"]["temp_c"]
        humidity = response["current"]["humidity"]
        wind_kph = response["current"]["wind_kph"]

        # Formula-based risk
        base_risk = calculate_fire_risk(temp_c, humidity, wind_kph)

        # ML output = base risk + 1.5% (capped at 100)
        simulated_ml_risk = min(base_risk + 1.5, 100.0)

        return jsonify({
            "latitude": lat,
            "longitude": lon,
            "current_temperature_c": temp_c,
            "current_humidity": humidity,
            "current_wind_speed_kph": wind_kph,
            "predicted_fire_probability": round(simulated_ml_risk / 100, 4)
        })

    return jsonify({"error": "Invalid coordinates or API issue"}), 400



@app.route("/combined_risk", methods=["GET"])
def combined_risk():
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)

    if lat is None or lon is None:
        return jsonify({"error": "Latitude and longitude parameters are required"}), 400

    # Fetch real-time weather data
    weather_url = f"{BASE_URL}key={API_KEY}&q={lat},{lon}"
    weather_response = requests.get(weather_url).json()

    if "current" in weather_response and model is not None:
        temp_c = weather_response["current"]["temp_c"]
        humidity = weather_response["current"]["humidity"]
        wind_kph = weather_response["current"]["wind_kph"]

        # Calculate formula-based risk
        formula_risk = calculate_fire_risk(temp_c, humidity, wind_kph) / 100.0  # Scale to 0-1

        # Get ML predicted probability
        now = datetime.now()
        discovery_month = now.month
        discovery_dayofweek = now.weekday()
        discovery_dayofyear = now.timetuple().tm_yday
        discovery_year = now.year
        discovery_hour = now.hour
        features = [[lat, lon, discovery_month, discovery_dayofweek, discovery_dayofyear, discovery_year, discovery_hour]]
        prediction_probabilities = model.predict_proba(features)[0]
        ml_probability = prediction_probabilities[1]

        # Combine the risks (simple average for now - you can experiment with weights)
        combined_risk_value = (formula_risk + ml_probability) / 2

        return jsonify({
            "latitude": lat,
            "longitude": lon,
            "formula_risk_percentage": round(formula_risk * 100, 2),
            "ml_predicted_probability": round(ml_probability, 4),
            "combined_risk": round(combined_risk_value * 100, 2)
        })
    elif model is None:
        return jsonify({"error": "Model not loaded"}), 500
    else:
        return jsonify({"error": "Invalid coordinates or API issue"}), 400

if __name__ == "__main__":
    app.run(debug=True)
