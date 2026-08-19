import streamlit as st  # type: ignore[import-not-found]
import requests  # type: ignore[import-not-found]
import datetime

st.set_page_config(page_title="IT Status Hub", layout="centered")

st.title(" Chris's Live IT Operations Hub")
st.caption(f"System Status Report | Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

st.markdown("---")

# Interactive Controls
st.subheader("🌐 Network & API Diagnostic Test")
target_site = st.selectbox("Select Cloud Target to Probe:", ["google.com", "github.com", "cloudflare.com"])

if st.button("Run Ping & Health Check"):
    with st.spinner("Executing HTTP GET probe..."):
        try:
            response = requests.get(f"https://{target_site}", timeout=5)
            if response.status_code == 200:
                st.success(f"SUCCESS: {target_site} responded with HTTP Status 200 (OK) in {response.elapsed.total_seconds():.2f}s")
            else:
                st.warning(f"WARNING: Returned Status Code {response.status_code}")
        except Exception as e:
            st.error(f"FAILURE: Could not reach target. Error: {e}")

st.markdown("---")

# Real-Time Weather API Call
st.subheader("☀️ Live Telemetry Data")
city = st.text_input("Enter a City Name:", "Atlanta")

if city:
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    geo_res = requests.get(geo_url).json()
    
    if "results" in geo_res:
        lat = geo_res["results"][0]["latitude"]
        lon = geo_res["results"][0]["longitude"]
        
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        w_res = requests.get(weather_url).json()["current_weather"]
        
        col1, col2 = st.columns(2)
        col1.metric("Temperature", f"{w_res['temperature']} °C")
        col2.metric("Wind Speed", f"{w_res['windspeed']} km/h")
    else:
        st.error("City not found.")