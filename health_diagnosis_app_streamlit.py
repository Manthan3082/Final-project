import streamlit as st
import json
import os
from datetime import datetime
from diagnosis_engine import diagnose
from action_plan import generate_7_day_plan

# Paths
CURRENT_DIR = os.path.dirname(__file__)
PROFILE_DIR = os.path.join(CURRENT_DIR, "profiles")
HISTORY_DIR = PROFILE_DIR
DISEASE_PATH = os.path.join(CURRENT_DIR, "data", "diseases.json")

# UI
st.set_page_config(page_title="Health Diagnosis Helper", layout="centered")
st.title("🧠 Health Diagnosis Helper - Streamlit Edition")
st.write("Enter your profile, select symptoms, and get AI-powered diagnosis and a 7-day plan.")

# Input
with st.form("diagnosis_form"):
    name = st.text_input("Name")
    age = st.text_input("Age")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])

    all_symptoms = [
        "fever", "cough", "sneezing", "sore throat", "fatigue", "chills", "muscle aches",
        "headache", "nausea", "light sensitivity", "shortness of breath", "loss of smell",
        "diarrhea", "vomiting", "stomach pain", "chest tightness", "wheezing"
    ]
    symptoms = st.multiselect("Select Symptoms", all_symptoms)

    submit = st.form_submit_button("Get Diagnosis")

if submit:
    if not name or not age or not symptoms:
        st.error("Please fill out all fields and select at least one symptom.")
    else:
        # Save profile
        os.makedirs(PROFILE_DIR, exist_ok=True)
        profile = {"username": name, "age": age, "gender": gender}
        with open(os.path.join(PROFILE_DIR, f"{name}.json"), "w") as f:
            json.dump(profile, f, indent=4)

        # Diagnose
        symptom_severity_dict = {s: 2 for s in symptoms}
        results = diagnose(symptom_severity_dict)

        # Save history
        entry = {
            "timestamp": datetime.now().isoformat(),
            "symptoms": symptoms,
            "diagnosis": results
        }
        history_path = os.path.join(HISTORY_DIR, f"{name}_history.json")
        history = []
        if os.path.exists(history_path):
            with open(history_path, "r") as f:
                history = json.load(f)
        history.append(entry)
        with open(history_path, "w") as f:
            json.dump(history, f, indent=4)

        # Display results
        top = results[0]
        st.success("✅ Diagnosis Complete")
        st.subheader(f"Top Match: {top['disease']}")
        st.write(f"**Matched Symptoms**: {', '.join(top['matched'])}")
        st.write(f"**Advice**: {top['advice']}")
        if top["link"]:
            st.markdown(f"[More info]({top['link']})")

        # Display plan
        st.subheader("📅 7-Day Action Plan")
        plan = generate_7_day_plan(top['disease'])
        st.table(plan)