import streamlit as st
import requests
from datetime import datetime
from streamlit_lottie import st_lottie

# === CONFIG ===
API_KEY = st.secrets["api"]["openweather"]
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

CITY_NAME_MAPPING = {
    "Bangalore, IN": "Bengaluru, IN",
    "Bombay, IN": "Mumbai, IN",
    "Madras, IN": "Chennai, IN",
    "Calcutta, IN": "Kolkata, IN"
}

POPULAR_INDIAN_CITIES = [
    "Mumbai, IN", "Delhi, IN", "Bangalore, IN", "Chennai, IN",
    "Kolkata, IN", "Hyderabad, IN", "Pune, IN", "Ahmedabad, IN",
    "Jaipur, IN", "Lucknow, IN"
]

LOTTIE_MAP = {
    "Clear": "https://assets4.lottiefiles.com/packages/lf20_ukvg3jub.json",
    "Clouds": "https://assets10.lottiefiles.com/private_files/lf30_mn53fgpa.json",
    "Rain": "https://assets2.lottiefiles.com/packages/lf20_jmBauI.json",
    "Thunderstorm": "https://assets2.lottiefiles.com/packages/lf20_iwmd6pyr.json",
    "Drizzle": "https://assets1.lottiefiles.com/packages/lf20_nazjrc1e.json",
    "Snow": "https://assets7.lottiefiles.com/packages/lf20_oGlWy5.json",
    "Mist": "https://assets3.lottiefiles.com/packages/lf20_xx9fzzxl.json",
    "Haze": "https://assets10.lottiefiles.com/private_files/lf30_obidsi0t.json",
    "Fog": "https://assets3.lottiefiles.com/packages/lf20_xx9fzzxl.json",
    "Smoke": "https://assets10.lottiefiles.com/packages/lf20_T9zVG5.json",
    "Dust": "https://assets2.lottiefiles.com/packages/lf20_Stt1R1.json",
    "Sand": "https://assets2.lottiefiles.com/packages/lf20_Stt1R1.json",
    "Ash": "https://assets2.lottiefiles.com/packages/lf20_tjsjre.json",
    "Squall": "https://assets2.lottiefiles.com/packages/lf20_gbfwtkzw.json",
    "Tornado": "https://assets3.lottiefiles.com/packages/lf20_u4yrau.json"
}

PLANT_MAP = {
    "Clear": "https://assets5.lottiefiles.com/packages/lf20_tll0j4bb.json",
    "Clouds": "https://assets5.lottiefiles.com/packages/lf20_k8nL1n.json",
    "Rain": "https://assets5.lottiefiles.com/packages/lf20_8xlcgjiz.json",
    "Drizzle": "https://assets5.lottiefiles.com/packages/lf20_8xlcgjiz.json",
    "Thunderstorm": "https://assets2.lottiefiles.com/packages/lf20_gbfwtkzw.json",
    "Snow": "https://assets4.lottiefiles.com/packages/lf20_6ijgwtux.json",
    "Fog": "https://assets10.lottiefiles.com/packages/lf20_lnhvvs.json",
    "Haze": "https://assets10.lottiefiles.com/packages/lf20_lnhvvs.json",
    "Smoke": "https://assets10.lottiefiles.com/packages/lf20_lnhvvs.json",
    "Dust": "https://assets10.lottiefiles.com/packages/lf20_lnhvvs.json",
    "Tornado": "https://assets3.lottiefiles.com/packages/lf20_2sl5dckk.json"
}

LOTTIE_MAP.setdefault("Default", LOTTIE_MAP["Clear"])
PLANT_MAP.setdefault("Default", PLANT_MAP["Clear"])


# === FUNCTIONS ===
def normalize_city_name(city):
    return CITY_NAME_MAPPING.get(city, city)

def load_lottie_url(url):
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return res.json()
    except Exception as e:
        st.error(f"Lottie load failed: {e}")
    return None

def get_weather(city):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    resp = requests.get(BASE_URL, params=params)
    if resp.status_code == 200:
        data = resp.json()
        if data.get("cod") == 200:
            return data
        else:
            st.error(f"⚠️ API Error: {data.get('message')}")
    else:
        st.error(f"⚠️ HTTP Error: {resp.status_code}")
    return None

def show_weather_alerts(temp, wind, main):
    alerts = []
    if temp >= 38:
        alerts.append("🔥 Heatwave: Stay hydrated!")
    elif temp <= 5:
        alerts.append("❄️ Cold: Dress warmly.")
    if wind >= 10:
        alerts.append("🌬️ High wind: Be cautious.")
    if main == "Thunderstorm":
        alerts.append("⛈️ Thunderstorm: Stay indoors.")
    if main in ["Rain", "Drizzle"] and wind > 7:
        alerts.append("🌧 Heavy rain: Watch flooding.")
    if main == "Snow":
        alerts.append("🌨️ Snow alert: Roads may be slippery.")
    if alerts:
        st.warning("🚨 Weather Alerts:")
        for a in alerts:
            st.markdown(f"- {a}")

def clothing_suggestion(temp, main):
    outfit = []
    if temp >= 35:
        outfit.append("🧢 Cap, 👕 Cotton T-shirt, 🩳 Shorts")
    elif 25 <= temp < 35:
        outfit.append("👕 T-shirt, 👖 Jeans, 🧴 Sunscreen")
    elif 15 <= temp < 25:
        outfit.append("🧥 Light Jacket, 👟 Sneakers")
    elif 5 <= temp < 15:
        outfit.append("🧣 Scarf, 🧥 Warm Coat, 🧤 Gloves")
    else:
        outfit.append("🧥 Heavy Coat, ❄️ Thermals, 🧤 Woolen Gloves")
    if main in ["Rain", "Drizzle"]:
        outfit.append("☔ Umbrella or waterproof jacket")
    if main == "Snow":
        outfit.append("❄️ Insulated boots and layered clothing")
    if main == "Thunderstorm":
        outfit.append("⚡ Avoid metal items; stay indoors")
    return outfit

# === APP UI ===
st.set_page_config(page_title="Weather Dashboard", layout="wide")

# Manual Refresh button
col_refresh, col_title = st.columns([1, 6])
with col_refresh:
    if st.button("🔄 Refresh", help="Click to reload"):
        st.experimental_rerun()
with col_title:
    st.title("🌤️ Real-Time Weather Dashboard")

# City Selector
with st.expander("📍 Select Your Location", expanded=True):
    mode = st.radio("Mode", ["Select from List", "Manual Entry"], horizontal=True)
    if mode == "Select from List":
        city = st.selectbox("Choose City", POPULAR_INDIAN_CITIES)
    else:
        city = st.text_input("Enter City Name (e.g., Delhi, IN)", value="Delhi, IN")

# Weather Display
if city:
    city = normalize_city_name(city)
    data = get_weather(city)

    if data:
        weather = data["weather"][0]
        main = weather["main"]
        desc = weather["description"].title()
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        tz = data["timezone"]
        local_time = datetime.utcfromtimestamp(data["dt"] + tz)
        formatted_time = local_time.strftime("%Y-%m-%d %H:%M:%S")

        lottie_weather = load_lottie_url(LOTTIE_MAP.get(main, LOTTIE_MAP["Default"]))
        plant_weather = load_lottie_url(PLANT_MAP.get(main, PLANT_MAP["Default"]))

        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"📍 {city}")
            st.write(f"🌡️ Temperature: {temp}°C")
            st.write(f"💧 Humidity: {humidity}%")
            st.write(f"💨 Wind Speed: {wind} m/s")
            st.write(f"🌈 Condition: {desc}")
            st.write(f"🕒 Local Time: {formatted_time}")
            if lottie_weather:
                st_lottie(lottie_weather, height=250, key="weather")
            else:
                st.info("No weather animation available.")
            show_weather_alerts(temp, wind, main)

        with col2:
            if plant_weather:
                st_lottie(plant_weather, height=180, key="plant")
            else:
                st.info("No plant animation available.")

        st.markdown("👕 **Clothing Suggestions:**")
        for item in clothing_suggestion(temp, main):
            st.markdown(f"- {item}")
