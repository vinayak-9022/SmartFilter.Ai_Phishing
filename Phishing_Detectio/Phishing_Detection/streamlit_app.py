
import streamlit as st
import requests

st.title("📧 AI Phishing Email Detector")

email = st.text_area("Paste the email content here:")

if st.button("Analyze"):
    response = requests.post('http://127.0.0.1:5000/predict', json={"email": email})
    result = response.json()['prediction']
    
    if result == "Phishing":
        st.error("⚠️ This email is likely a phishing attempt!")
    else:
        st.success("✅ This email seems safe.")
