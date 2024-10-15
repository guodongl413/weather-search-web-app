from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 加载 .env 文件中的环境变量
load_dotenv(dotenv_path="server-side/.env")

# 获取环境变量
TOMORROW_API_KEY = os.getenv('TOMORROW_API_KEY')
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
IPINFO_API_TOKEN = os.getenv('IPINFO_API_TOKEN')

if not TOMORROW_API_KEY or not GOOGLE_MAPS_API_KEY or not IPINFO_API_TOKEN:
    raise EnvironmentError("One or more API keys are not set. Please check your .env file.")

@app.route('/')
def index():
    return "Welcome to the Weather App Backend!"

@app.route('/get_location', methods=['GET'])
def get_location():
    use_current_location = request.args.get('use_current_location', '').lower() == 'true'
    street = request.args.get('street')
    city = request.args.get('city')
    state = request.args.get('state')

    # 获取当前 IP 地址的位置信息
    if use_current_location:
        ip_info_response = requests.get(f'https://ipinfo.io?token={IPINFO_API_TOKEN}')
        if ip_info_response.status_code != 200:
            return jsonify({'error': 'Failed to retrieve current location'}), 400
        location_data = ip_info_response.json()
        lat_lng = location_data.get('loc')
        if not lat_lng:
            return jsonify({'error': 'Failed to retrieve current location coordinates'}), 400

        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat_lng}&key={GOOGLE_MAPS_API_KEY}"
        geocode_response = requests.get(geocode_url)
        if geocode_response.status_code != 200:
            return jsonify({'error': 'Google Maps API request failed'}), 400
        geocode_data = geocode_response.json()

        if 'results' in geocode_data and geocode_data['results']:
            formatted_address = geocode_data['results'][0]['formatted_address']
        else:
            return jsonify({'error': 'Unable to retrieve formatted address'}), 400

        latitude, longitude = lat_lng.split(',')
    else:
        if not street or not city or not state:
            return jsonify({'error': 'Street, City, and State are required'}), 400

        address = f"{street}, {city}, {state}"
        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={GOOGLE_MAPS_API_KEY}"
        geocode_response = requests.get(geocode_url)
        if geocode_response.status_code != 200:
            return jsonify({'error': 'Google Maps API request failed'}), 400
        geocode_data = geocode_response.json()

        if 'results' not in geocode_data or not geocode_data['results']:
            return jsonify({'error': 'Unable to geocode the address'}), 400

        location = geocode_data['results'][0]['geometry']['location']
        latitude, longitude = location['lat'], location['lng']
        formatted_address = address

    weather_url = "https://api.tomorrow.io/v4/timelines"
    query_params = {
        "location": f"{latitude},{longitude}",
        "fields": ",".join([
            "temperature", "temperatureApparent", "temperatureMin", "temperatureMax",
            "windSpeed", "humidity", "uvIndex", "pressureSeaLevel", "sunriseTime",
            "sunsetTime", "cloudCover", "precipitationProbability", "precipitationType",
            "weatherCode", "visibility", "moonPhase"
        ]),
        "units": "imperial",
        "timesteps": "1d",
        "timezone": "America/Los_Angeles"
    }
    headers = {
        "apikey": TOMORROW_API_KEY
    }

    weather_response = requests.get(weather_url, headers=headers, params=query_params)
    if weather_response.status_code != 200:
        return jsonify({'error': 'Tomorrow.io API request failed'}), 400
    weather_data = weather_response.json()

    if 'data' not in weather_data:
        return jsonify({'error': 'Failed to retrieve weather data'}), 400

    return jsonify({'latitude': latitude, 'longitude': longitude, 'address': formatted_address, 'weather': weather_data})

def fetch_weather_data(latitude, longitude, timesteps, fields):
    url = "https://api.tomorrow.io/v4/timelines"
    params = {
        "location": f"{latitude},{longitude}",
        "fields": fields,
        "units": "imperial",
        "timesteps": timesteps,
        "timezone": "America/Los_Angeles"
    }
    headers = {"apikey": TOMORROW_API_KEY}

    response = requests.get(url, headers=headers, params=params)

    # 打印请求 URL 和状态码，方便调试
    print(f"Request URL: {response.url}")
    print(f"Status Code: {response.status_code}")

    if response.status_code != 200:
        print(f"Error: {response.text}")
        return None

    return response.json()


@app.route('/weather_data', methods=['GET'])
def weather_data():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')

    if not latitude or not longitude:
        return jsonify({'error': 'Latitude and Longitude are required'}), 400

    daily_fields = ",".join([
        "temperature", "temperatureApparent", "temperatureMin", "temperatureMax"
    ])

    hourly_fields = ",".join([
        "temperature", "windSpeed", "windDirection", "humidity", "pressureSeaLevel"
    ])

    daily_data = fetch_weather_data(latitude, longitude, "1d", daily_fields)
    hourly_data = fetch_weather_data(latitude, longitude, "1h", hourly_fields)

    if not daily_data or not hourly_data:
        return jsonify({'error': 'Failed to retrieve weather data'}), 400

    return jsonify({'daily': daily_data, 'hourly': hourly_data})


# if __name__ == '__main__':
#     app.run(debug=True)
