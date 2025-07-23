import streamlit as st
import requests
from datetime import datetime
from streamlit_lottie import st_lottie
import time

# API Setup
API_KEY = st.secrets["api"]["openweather"]
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# City aliases (if needed)
CITY_NAME_MAPPING = {
    "Bangalore, IN": "Bengaluru, IN",
    "Bombay, IN": "Mumbai, IN",
    "Madras, IN": "Chennai, IN",
    "Calcutta, IN": "Kolkata, IN"
}

def normalize_city_name(city):
    return CITY_NAME_MAPPING.get(city, city)

def get_weather(city):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("cod") == 200:
            return data
        else:
            st.error(f"⚠️ API Error: {data.get('message')}")
    else:
        st.error(f"⚠️ HTTP Error: {response.status_code}")
    return None

def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None

def get_background_color(weather_main):
    colors = {
        "Clear": "#fdd835",
        "Clouds": "#90a4ae",
        "Rain": "#4fc3f7",
        "Snow": "#e1f5fe",
        "Thunderstorm": "#ce93d8",
        "Drizzle": "#80deea",
        "Mist": "#cfd8dc",
        "Haze": "#e0e0e0"
    }
    return colors.get(weather_main, "#ffffff")

def show_weather_alerts(temp, wind_speed, weather_main):
    alerts = []
    if temp >= 38:
        alerts.append("🔥 **Heatwave Alert**: Stay hydrated!")
    elif temp <= 5:
        alerts.append("❄️ **Cold Alert**: Wear layers to stay warm.")
    if wind_speed >= 10:
        alerts.append("🌬️ **High Wind Alert**: Be cautious outdoors.")
    if weather_main == "Thunderstorm":
        alerts.append("⛈️ **Thunderstorm Warning**: Stay indoors.")
    if weather_main in ["Rain", "Drizzle"] and wind_speed > 7:
        alerts.append("🌧️ **Heavy Rain**: Watch for flooding.")
    if weather_main == "Snow":
        alerts.append("🌨️ **Snow Alert**: Roads may be slippery.")

    if alerts:
        st.warning("🚨 Weather Alerts:")
        for a in alerts:
            st.markdown(f"- {a}")

def clothing_suggestion(temp, weather_main):
    outfit = []
    if temp >= 35:
        outfit.append("🧢 Light cap, 👕 cotton t-shirt, 🩳 shorts, 🕶️ sunglasses.")
    elif 25 <= temp < 35:
        outfit.append("👕 T-shirt, 👖 jeans, 🧴 sunscreen.")
    elif 15 <= temp < 25:
        outfit.append("🧥 Light jacket or hoodie, 👟 closed shoes.")
    elif 5 <= temp < 15:
        outfit.append("🧣 Scarf, 🧥 warm jacket, 🧤 gloves.")
    else:
        outfit.append("🧣 Thick scarf, 🧥 heavy coat, 🧤 thermal gloves.")

    if weather_main in ["Rain", "Drizzle"]:
        outfit.append("☔ Umbrella or waterproof jacket.")
    if weather_main == "Snow":
        outfit.append("❄️ Insulated boots, thermal wear.")
    if weather_main == "Thunderstorm":
        outfit.append("⚡ Avoid metal accessories.")

    return outfit

# Lottie animations
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

POPULAR_INDIAN_CITIES = [
    "Mumbai, IN", "Delhi, IN", "Bangalore, IN", "Chennai, IN", "Kolkata, IN",
    "Hyderabad, IN", "Pune, IN", "Ahmedabad, IN", "Jaipur, IN", "Lucknow, IN",
    "Bhopal, IN", "Chandigarh, IN", "Patna, IN", "Indore, IN"
]

# Streamlit UI
st.set_page_config(page_title="Weather Dashboard", layout="wide")
st.title("🌤️ Real-Time Weather Dashboard")

# Auto-refresh every 60 seconds
# Top-right manual refresh button
col_refresh, col_title = st.columns([1, 6])
with col_refresh:
    if st.button("🔄 Refresh", help="Click to reload data"):
        st.experimental_rerun()

# Location selection
with st.expander("📍 Choose Your Location", expanded=True):
    mode = st.radio("Mode", ["Select from List", "Manual Entry"], horizontal=True)
    if mode == "Select from List":
        city = st.selectbox("Choose a City", POPULAR_INDIAN_CITIES)
    else:
        city = st.text_input("Enter City Name (e.g., 'Delhi, IN')", value="Delhi, IN")

if city:
    city = normalize_city_name(city)
    data = get_weather(city)

    if data:
        weather = data["weather"][0]
        weather_main = weather["main"]
        description = weather["description"].title()
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        timezone = data["timezone"]
        local_time = datetime.utcfromtimestamp(data["dt"] + timezone)
        formatted_time = local_time.strftime("%Y-%m-%d %H:%M:%S")

        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"📍 {city}")
            st.write(f"**🌡️ Temp:** {temp} °C")
            st.write(f"**💧 Humidity:** {humidity}%")
            st.write(f"**💨 Wind Speed:** {wind_speed} m/s")
            st.write(f"**🌈 Condition:** {description}")
            st.write(f"**🕒 Local Time:** {formatted_time}")
            if weather_main in LOTTIE_MAP:
                st_lottie(load_lottie_url(LOTTIE_MAP[weather_main]), height=240)
            show_weather_alerts(temp, wind_speed, weather_main)

        with col2:
            plant_animation = load_lottie_url(PLANT_MAP.get(weather_main, PLANT_MAP["Clear"]))
            if plant_animation:
                st_lottie(plant_animation, height=200)
            else:
                st.markdown("🌱 Plant animation unavailable.")

        st.markdown("👕 **AI-Based Clothing Suggestions:**")
        for item in clothing_suggestion(temp, weather_main):
            st.markdown(f"- {item}")
