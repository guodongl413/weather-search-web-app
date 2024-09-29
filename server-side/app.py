from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 加载 .env 文件中的环境变量
load_dotenv()

# 获取环境变量
TOMORROW_API_KEY = os.getenv('TOMORROW_API_KEY')
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
IPINFO_API_TOKEN = os.getenv('IPINFO_API_TOKEN')

if not TOMORROW_API_KEY or not GOOGLE_MAPS_API_KEY or not IPINFO_API_TOKEN:
    raise EnvironmentError("One or more API keys are not set. Please check your .env file.")

@app.route('/')
def index():
    # 返回简单的欢迎信息以确认后端正常运行
    return "Welcome to the Weather App Backend!"

@app.route('/get_location', methods=['GET'])
def get_location():
    use_current_location = request.args.get('use_current_location', '').lower() == 'true'
    street = request.args.get('street')
    city = request.args.get('city')
    state = request.args.get('state')

    if use_current_location:
        # 使用 ipinfo.io 获取当前位置信息
        ip_info_response = requests.get(f'https://ipinfo.io?token={IPINFO_API_TOKEN}')
        if ip_info_response.status_code != 200:
            return jsonify({'error': 'Failed to retrieve current location'}), 400
        location_data = ip_info_response.json()
        lat_lng = location_data.get('loc')
        if not lat_lng:
            return jsonify({'error': 'Failed to retrieve current location coordinates'}), 400

        # 获取地理位置信息的具体地址
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
        # 检查用户是否手动输入了街道、城市和州
        if not street or not city or not state:
            return jsonify({'error': 'Street, City, and State are required'}), 400

        # 使用 Google Maps Geocoding API 获取纬度和经度
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

    # 构建 Tomorrow.io 的 API 请求来获取天气数据
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

    # 发起请求，使用 headers 来传递 API Key
    weather_response = requests.get(weather_url, headers=headers, params=query_params)
    if weather_response.status_code != 200:
        return jsonify({'error': 'Tomorrow.io API request failed'}), 400
    weather_data = weather_response.json()

    # 检查 Tomorrow.io API 响应是否有效
    if 'data' not in weather_data:
        return jsonify({'error': 'Failed to retrieve weather data'}), 400

    # 返回天气数据和位置
    return jsonify({'address': formatted_address, 'weather': weather_data})

if __name__ == '__main__':
    app.run(debug=True)
