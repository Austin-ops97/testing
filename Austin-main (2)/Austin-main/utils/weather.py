import requests
from datetime import datetime, timedelta
from utils.pricing import fetch_price, fetch_lmp
from utils.graphs import create_trend_graph

BASE_URL = "https://api.weather.gov"
LOCATION_COORDS = {
    "PHR": {"lat": 29.5102, "lon": -94.9924},
    "Wharton": {"lat": 29.3116, "lon": -96.0978},
    "Ector": {"lat": 31.9176, "lon": -102.6162}
}

def fetch_temperature(location):
    """Fetches temperature from weather.gov."""
    coords = LOCATION_COORDS.get(location)
    if not coords:
        return "No data"
    try:
        points_url = f"{BASE_URL}/points/{coords['lat']},{coords['lon']}"
        headers = {"User-Agent": "Energy Dashboard (your_email@example.com)"}
        response = requests.get(points_url, headers=headers, timeout=10)
        response.raise_for_status()
        forecast_url = response.json()["properties"]["forecastHourly"]
        forecast = requests.get(forecast_url, headers=headers).json()
        temp = forecast["properties"]["periods"][0]["temperature"]
        return f"{temp}°F"
    except Exception as e:
        return f"Error: {e}"

def fetch_condition(location):
    """Fetches weather condition from weather.gov."""
    coords = LOCATION_COORDS.get(location)
    if not coords:
        return "No data"
    try:
        points_url = f"{BASE_URL}/points/{coords['lat']},{coords['lon']}"
        headers = {"User-Agent": "Energy Dashboard (your_email@example.com)"}
        response = requests.get(points_url, headers=headers, timeout=10)
        response.raise_for_status()
        forecast_url = response.json()["properties"]["forecastHourly"]
        forecast = requests.get(forecast_url, headers=headers).json()
        condition = forecast["properties"]["periods"][0]["shortForecast"]
        return condition
    except Exception as e:
        return f"Error: {e}"

def fetch_and_update_data(selected_locations):
    """Aggregates weather and pricing data."""
    data = {}
    for location in selected_locations:
        temp = fetch_temperature(location)
        condition = fetch_condition(location)
        price = fetch_price(location)
        lmp = fetch_lmp(location)
        graph_path = create_trend_graph(location, [(datetime.now(), price)] if price else [])
        data[location] = {
            "Temperature": temp,
            "Condition": condition,
            "Price": f"${price:.2f}" if price else "No data",
            "Trend_Graph_Path": graph_path
        }
    return data
