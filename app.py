import streamlit as st
import requests
import geocoder
from datetime import datetime
from streamlit_lottie import st_lottie
import time

# OpenWeatherMap API Key
API_KEY = "your_api_key_here"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

