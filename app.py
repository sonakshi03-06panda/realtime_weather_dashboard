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

def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def get_background_color(weather_main):
    mapping = {
        "Clear": "#fdd835",
        "Clouds": "#90a4ae",
        "Rain": "#4fc3f7",
        "Snow": "#e1f5fe",
        "Thunderstorm": "#ce93d8",
        "Drizzle": "#80deea",
        "Mist": "#cfd8dc",
        "Haze": "#e0e0e0"
    }
    return mapping.get(weather_main, "#eeeeee")

def show_weather_alerts(temp, wind_speed, weather_main):
    alerts = []
    if temp >= 38:
        alerts.append("🔥 **Heatwave Alert:** Stay hydrated and avoid direct sunlight.")
    elif temp <= 5:
        alerts.append("❄️ **Cold Alert:** Dress warmly to avoid hypothermia.")
    if wind_speed >= 10:
        alerts.append("🌬️ **High Wind Alert:** Secure outdoor items and be cautious.")
    if weather_main in ["Thunderstorm"]:
        alerts.append("⛈️ **Thunderstorm Alert:** Stay indoors and unplug electronics.")
    if weather_main in ["Rain", "Drizzle"] and wind_speed > 7:
        alerts.append("🌧️ **Heavy Rain Warning:** Watch for flooding or roadblocks.")
    if weather_main == "Snow":
        alerts.append("🌨️ **Snowfall Alert:** Expect slippery roads and low visibility.")
    if alerts:
        st.warning("🚨 Weather Alerts:")
        for alert in alerts:
            st.markdown(f"- {alert}")

# ----------------- Lottie URLs -----------------

LOTTIE_MAP = {
    "Clear": "https://assets4.lottiefiles.com/packages/lf20_ukvg3jub.json",
    "Clouds": "https://assets10.lottiefiles.com/private_files/lf30_mn53fgpa.json",
    "Rain": "https://assets2.lottiefiles.com/packages/lf20_jmBauI.json",
    "Thunderstorm": "https://assets2.lottiefiles.com/packages/lf20_iwmd6pyr.json",
    "Drizzle": "https://assets1.lottiefiles.com/packages/lf20_nazjrc1e.json",
    "Snow": "https://assets7.lottiefiles.com/packages/lf20_oGlWy5.json",
    "Mist": "https://assets3.lottiefiles.com/packages/lf20_xx9fzzxl.json",
    "Haze": "https://assets10.lottiefiles.com/private_files/lf30_obidsi0t.json"
}

PLANT_MAP = {
    "Clear": "https://assets5.lottiefiles.com/packages/lf20_tll0j4bb.json",
    "Rain": "https://assets5.lottiefiles.com/packages/lf20_8xlcgjiz.json",
    "Thunderstorm": "https://assets2.lottiefiles.com/packages/lf20_gbfwtkzw.json",
    "Snow": "https://assets4.lottiefiles.com/packages/lf20_6ijgwtux.json",
    "Clouds": "https://assets5.lottiefiles.com/packages/lf20_k8nL1n.json"
}

# ----------------- Streamlit Layout -----------------

st.set_page_config(layout="wide", page_title="Real-Time Weather Dashboard")
st.title("🌤️ Real-Time Weather Dashboard")

# 🕒 Auto-refresh every 60 seconds
AUTO_REFRESH_INTERVAL = 60
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()
time_since_refresh = time.time() - st.session_state.last_refresh
refresh_remaining = AUTO_REFRESH_INTERVAL - time_since_refresh
with st.sidebar:
    st.markdown("⏱️ **Auto Refresh:** every 60s")
    st.progress(max(0, 1 - refresh_remaining / AUTO_REFRESH_INTERVAL))
if time_since_refresh >= AUTO_REFRESH_INTERVAL:
    st.session_state.last_refresh = time.time()
    st.experimental_rerun()

# Location input
with st.expander("🔍 Customize Location", expanded=True):
    auto_detect = st.toggle("📡 Use My Location", value=True)
    if auto_detect:
        city = get_location_by_ip()
        st.success(f"📍 Detected Location: **{city}**")
    else:
        city = st.text_input("📝 Enter City Name:", "Delhi")

if city:
    data = get_weather(city)
    if data:
        weather_main = data['weather'][0]['main']
        description = data['weather'][0]['description'].title()
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        timezone = data['timezone']
        local_time = datetime.utcfromtimestamp(data['dt'] + timezone)
        formatted_time = local_time.strftime("%Y-%m-%d %H:%M:%S")

        st.markdown(
            f"<style>.stApp {{ background-color: {get_background_color(weather_main)}; }}</style>",
            unsafe_allow_html=True
        )

        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"📍 {city.title()}")
            st.write(f"**🌡️ Temp:** {temp} °C")
            st.write(f"**💧 Humidity:** {humidity}%")
            st.write(f"**💨 Wind:** {wind_speed} m/s")
            st.write(f"**🌈 Condition:** {description}")
            st.write(f"**🕒 Local Time:** {formatted_time}")
            lottie_url = LOTTIE_MAP.get(weather_main, None)
            if lottie_url:
                st_lottie(load_lottie_url(lottie_url), height=250)
            show_weather_alerts(temp, wind_speed, weather_main)
        with col2:
            plant_url = PLANT_MAP.get(weather_main, None)
            if plant_url:
                st_lottie(load_lottie_url(plant_url), height=150)

        # ----------------- AI Clothing Suggestion -----------------
        def clothing_suggestion(temp, weather_main):
            suggestions = []
            if temp >= 35:
                suggestions.append("🧢 Light cap, 👕 cotton t-shirt, 🩳 shorts, and 🕶️ sunglasses.")
            elif 25 <= temp < 35:
                suggestions.append("👕 T-shirt, 👖 jeans or trousers, and 🧴 sunscreen.")
            elif 15 <= temp < 25:
                suggestions.append("🧥 Light jacket or hoodie, 👖 jeans, and 👟 closed shoes.")
            elif 5 <= temp < 15:
                suggestions.append("🧣 Scarf, 🧥 warm jacket, 🧤 gloves, and boots.")
            else:
                suggestions.append("🧣 Thick scarf, 🧥 heavy coat, 🧤 thermal gloves, and ❄️ snow boots.")

            if weather_main in ["Rain", "Drizzle"]:
                suggestions.append("☔ Carry an umbrella or wear a waterproof jacket.")
            if weather_main == "Snow":
                suggestions.append("⛷️ Wear insulated boots and thermal layers.")
            if weather_main == "Thunderstorm":
                suggestions.append("⚡ Avoid metal accessories and stay indoors if possible.")

            return suggestions

        st.markdown("👗 **AI-Based Clothing Suggestions:**")
        for line in clothing_suggestion(temp, weather_main):
            st.markdown(f"- {line}")
    else:
        st.error("City not found or API error.")
        