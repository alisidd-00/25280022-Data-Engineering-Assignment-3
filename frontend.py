import streamlit as st
import requests

st.set_page_config(page_title="PakWheels Price Predictor", page_icon="🚗", layout="centered")

st.title("PakWheels Used Car Price Predictor")
st.markdown("Enter car specifications to predict whether it falls in the **High Price** or **Low Price** category.")

API_URL = "http://localhost:8000/predict"

st.sidebar.header("Car Specifications")

year = st.sidebar.slider("Year", min_value=1990, max_value=2026, value=2018, step=1)

engine = st.sidebar.number_input("Engine Capacity (cc)", min_value=100, max_value=8000, value=1300, step=100)

mileage = st.sidebar.number_input("Mileage (km)", min_value=0, max_value=500000, value=45000, step=1000)

transmission = st.sidebar.selectbox("Transmission", ["Manual", "Automatic"])

fuel = st.sidebar.selectbox("Fuel Type", ["Petrol", "Diesel", "Hybrid", "CNG", "LPG"])

body = st.sidebar.selectbox("Body Type", [
    "Sedan", "Hatchback", "SUV", "Crossover", "Compact SUV",
    "Compact sedan", "Van", "Truck", "Double Cabin", "Mini Van",
    "Coupe", "Convertible", "Station Wagon", "MPV"
])

city = st.sidebar.selectbox("City", [
    "Lahore", "Karachi", "Islamabad", "Rawalpindi", "Faisalabad",
    "Peshawar", "Multan", "Gujranwala", "Sialkot", "Quetta"
])

st.markdown("---")
st.subheader("Selected Car Details")
col1, col2 = st.columns(2)
with col1:
    st.write(f"**Year:** {year}")
    st.write(f"**Engine:** {engine} cc")
    st.write(f"**Mileage:** {mileage:,} km")
    st.write(f"**Transmission:** {transmission}")
with col2:
    st.write(f"**Fuel Type:** {fuel}")
    st.write(f"**Body Type:** {body}")
    st.write(f"**City:** {city}")

st.markdown("---")

if st.button("Predict Price Category", type="primary"):
    payload = {
        "year": float(year),
        "engine": float(engine),
        "mileage": float(mileage),
        "transmission": transmission,
        "fuel": fuel,
        "body": body,
        "city": city,
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        if response.status_code == 200:
            result = response.json()
            prediction = result["prediction"]
            category = result["price_category"]

            if prediction == 1:
                st.success(f"Prediction: **{category}**")
                st.balloons()
            else:
                st.info(f"Prediction: **{category}**")

            st.json(result)
        else:
            st.error(f"API Error: {response.status_code} — {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the backend API. Make sure the FastAPI server is running on http://localhost:8000")
    except Exception as e:
        st.error(f"Error: {str(e)}")

st.markdown("---")
st.caption("AI 620 — Assignment 3, Part 2 | Roll Number: 25280022")
