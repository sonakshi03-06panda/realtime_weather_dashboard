import streamlit as st
import requests
import geocoder
from datetime import datetime
from streamlit_lottie import st_lottie
import time

# OpenWeatherMap API Key
API_KEY = "your_api_key_here"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# ----------------- Utility Functions -----------------

def get_weather(city):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    return None

def get_location_by_ip():
    g = geocoder.ip("me")
    if g.ok:
        return g.city or "Delhi"
    return "Delhi"