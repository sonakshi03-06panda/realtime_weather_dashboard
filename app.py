import streamlit as st
import requests
from datetime import datetime
from streamlit_lottie import st_lottie
import geocoder

API_KEY = st.secrets["api"]["openweather"]
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

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
    resp = requests.get(BASE_URL, params=params)
    if resp.status_code == 200:
        d = resp.json()
        if d.get("cod") == 200:
            return d
        st.error(f"⚠️ API Error: {d.get('message')}")
    else:
        st.error(f"⚠️ HTTP Error: {resp.status_code}")
    return None

def load_lottie_url(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

def show_weather_alerts(temp, wind, main):
    alerts = []
    if temp >= 38: alerts.append("🔥 Heatwave: Stay hydrated!")
    elif temp <= 5: alerts.append("❄️ Cold: Dress warmly.")
    if wind >= 10: alerts.append("🌬️ High wind: Be cautious.")
    if main == "Thunderstorm": alerts.append("⛈️ Thunderstorm: Stay indoors.")
    if main in ["Rain","Drizzle"] and wind > 7: alerts.append("🌧 Heavy rain: Watch flooding.")
    if main == "Snow": alerts.append("🌨️ Snow alert: Slippery roads.")
    if alerts:
        st.warning("🚨 Weather Alerts:")
        for a in alerts: st.markdown(f"- {a}")

def clothing_suggestion(temp, main):
    outfit = []
    if temp >= 35:
        outfit.append("🧢 Cap, T‑shirt & shorts.")
    elif 25 <= temp < 35:
        outfit.append("👕 T‑shirt & jeans + sunscreen.")
    elif 15 <= temp < 25:
        outfit.append("🧥 Light jacket & sneakers.")
    elif 5 <= temp < 15:
        outfit.append("🧣 Scarf, warm jacket, gloves.")
    else:
        outfit.append("🧥 Heavy coat, thermal wear.")
    if main in ["Rain","Drizzle"]:
        outfit.append("☔ Bring umbrella / waterproof jacket.")
    if main == "Snow":
        outfit.append("❄️ Insulated boots & layers.")
    if main == "Thunderstorm":
        outfit.append("⚡ Avoid metal items; indoors advised.")
    return outfit

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
    "Mumbai, IN", "Delhi, IN", "Bangalore, IN", "Chennai, IN",
    "Kolkata, IN", "Hyderabad, IN", "Pune, IN", "Ahmedabad, IN",
    "Jaipur, IN", "Lucknow, IN"
]

st.set_page_config(page_title="Weather Dashboard", layout="wide")

# HEADER: Refresh button top-right
col_refresh, col_title = st.columns([0.5, 7])
with col_refresh:
    if st.button("🔄 Refresh"):
        st.experimental_rerun()
with col_title:
    st.title("🌤️ Real-Time Weather Dashboard")

# LOCATION SELECTOR
with st.expander("📍 Choose Location", expanded=True):
    mode = st.radio("", ["Select from List", "Manual Entry"], horizontal=True)
    if mode == "Select from List":
        city = st.selectbox("Choose a City", POPULAR_INDIAN_CITIES)
    else:
        city = st.text_input("Enter City (e.g., 'Delhi, IN')", value="Delhi, IN")

if city:
    city = normalize_city_name(city)
    data = get_weather(city)
    if data:
        w = data["weather"][0]; main = w["main"]
        desc = w["description"].title()
        temp = data["main"]["temp"]; hum = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        tz = data["timezone"]
        local = datetime.utcfromtimestamp(data["dt"] + tz)

        col1, col2 = st.columns([3,1])
        with col1:
            st.subheader(f"📍 {city}")
            st.write(f"🌡️ Temp: {temp}°C  | 💧 Humidity: {hum}%  | 💨 Wind: {wind} m/s")
            st.write(f"🌈 Condition: {desc}  | 🕒 {local.strftime('%Y-%m-%d %H:%M:%S')}")
            if main in LOTTIE_MAP:
                st_lottie(load_lottie_url(LOTTIE_MAP[main]), height=240)
            show_weather_alerts(temp, wind, main)
        with col2:
            animation = load_lottie_url(PLANT_MAP.get(main, PLANT_MAP["Clear"]))
            if animation:
                st_lottie(animation, height=200)

        st.markdown("👕 **Clothing Suggestions:**")
        for item in clothing_suggestion(temp, main):
            st.markdown(f"- {item}")