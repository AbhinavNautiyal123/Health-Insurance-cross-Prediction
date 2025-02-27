import streamlit as st
import onnxruntime as rt
import numpy as np
import requests
import io

# ==============================
# CREATED BY ABHINAV NAUTIYAL 🚀
# ==============================

# Streamlit Page Configuration
st.set_page_config(page_title="Insurance Policy Predictor", page_icon="💰", layout="wide")

# Function to load ONNX model efficiently
@st.cache_resource  # Ensures model loads only once
def load_model():
    FILE_ID = "1p0SVNYD2NlT2J_hIPN3o7azBkEzxjqzF"
    DIRECT_URL = f"https://drive.google.com/uc?id={FILE_ID}&export=download"

    st.write("Loading ONNX model from Google Drive into memory...")
    
    response = requests.get(DIRECT_URL, stream=True)
    if response.status_code == 200:
        model_bytes = io.BytesIO(response.content)  # Convert response to file-like object
        return rt.InferenceSession(model_bytes.getvalue())  # Load ONNX model
    else:
        st.error(f"❌ Failed to fetch ONNX model. HTTP Status Code: {response.status_code}")
        return None

# Load the model
session = load_model()

# Function to make predictions
def predict(features):
    if session:
        input_name = session.get_inputs()[0].name
        output_name = session.get_outputs()[0].name
        prediction = session.run([output_name], {input_name: np.array([features], dtype=np.float32)})[0]
        return prediction[0]
    else:
        st.error("❌ Model not loaded. Please check the logs.")
        return None

# Custom CSS for better UI
st.markdown("""
    <style>
        body { background-color: #0e1117; color: white; }
        .stButton>button {
            background: linear-gradient(135deg, #ff7e5f, #feb47b);
            color: white;
            font-size: 18px;
            border-radius: 10px;
        }
        .stTextInput>div>div>input, .stNumberInput>div>div>input {
            background-color: #222;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown("<h1 style='text-align: center;'>🚀 Health Insurance Policy Predictor 💰</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #FEB47B;'>Find out if a customer will take the policy!</h3>", unsafe_allow_html=True)

# Layout for input fields
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📊 Customer Information")
    
    age_60_plus = st.checkbox("Age 60+")
    age_40_60 = st.checkbox("Age Between 40 and 60")
    age_20_40 = st.checkbox("Age Between 20 and 40")

    gender = st.radio("Gender", ["Male", "Female"], horizontal=True)
    gender_male = 1 if gender == "Male" else 0
    gender_female = 1 if gender == "Female" else 0

    driving_license = st.checkbox("Has Driving License")

    region_code = st.number_input("Region Code", min_value=0.0, value=28.0, step=1.0)

    previously_insured = st.radio("Previously Insured", ["Yes", "No"], horizontal=True)
    previously_insured_yes = 1 if previously_insured == "Yes" else 0
    previously_insured_no = 1 if previously_insured == "No" else 0

with col2:
    st.markdown("### 🚗 Vehicle & Policy Details")
    
    vehicle_age = st.radio("Vehicle Age", ["<1 year", "1-2 years", ">2 years"], horizontal=True)
    vehicle_age_1_2 = 1 if vehicle_age == "1-2 years" else 0
    vehicle_age_less_1 = 1 if vehicle_age == "<1 year" else 0
    vehicle_age_more_2 = 1 if vehicle_age == ">2 years" else 0

    annual_premium = st.number_input("Annual Premium", min_value=0.0, value=40000.0)

    policy_sales_channel = st.number_input("Policy Sales Channel", min_value=0.0, value=26.0, step=1.0)

    customer_type = st.radio("Customer Type", ["Long-term", "Mid-term", "Short-term"], horizontal=True)
    long_term = 1 if customer_type == "Long-term" else 0
    mid_term = 1 if customer_type == "Mid-term" else 0
    short_term = 1 if customer_type == "Short-term" else 0

# Predict Button
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
if st.button("🔥 Predict Now 🔥"):
    user_input = [
        int(age_60_plus), int(age_40_60), int(age_20_40), 
        gender_male, gender_female, int(driving_license), 
        float(region_code), vehicle_age_1_2, vehicle_age_less_1, vehicle_age_more_2, 
        float(annual_premium), previously_insured_yes, previously_insured_no, 
        float(policy_sales_channel), long_term, mid_term, short_term
    ]
    
    prediction = predict(user_input)
    if prediction is not None:
        result = "✅ Likely to Take the Policy!" if int(prediction) == 1 else "❌ Not Interested in the Policy"
        st.success(result)
        
        # 🎉 Confetti effect for positive prediction
        if int(prediction) == 1:
            st.balloons()
st.markdown("</div>", unsafe_allow_html=True)
