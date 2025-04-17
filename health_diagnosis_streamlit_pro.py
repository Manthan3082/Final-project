import streamlit as st
import json
import os
from datetime import datetime
import base64
from diagnosis_engine import diagnose
from action_plan import generate_7_day_plan
from pdf_export import generate_pdf
from translator import translate_text

CURRENT_DIR = os.path.dirname(__file__)
PROFILE_DIR = os.path.join(CURRENT_DIR, "profiles")
HISTORY_DIR = PROFILE_DIR

st.set_page_config(page_title="Health Diagnosis Pro", layout="centered")
st.title("🧠 Health Diagnosis Helper – Pro Edition")
st.write("Multilingual | PDF Export | Probability Scores")


language_options = {
    "English": "en",
    "Hindi (हिंदी)": "hi",
    "French (Français)": "fr",
    "Spanish (Español)": "es",
    "German (Deutsch)": "de"
}
selected_language_name = st.selectbox("🌐 Select Language", list(language_options.keys()))
lang = language_options[selected_language_name]


with st.form("diagnosis_form"):
    name = st.text_input(translate_text("Name", lang))
    age = st.text_input(translate_text("Age", lang))
    gender = st.selectbox(translate_text("Gender", lang), ["Male", "Female", "Other"])

    all_symptoms = [
        "fever", "cough", "sneezing", "sore throat", "fatigue", "chills", "muscle aches",
        "headache", "nausea", "light sensitivity", "shortness of breath", "loss of smell",
        "diarrhea", "vomiting", "stomach pain", "chest tightness", "wheezing"
    ]
    translated_symptoms = [translate_text(sym, lang) for sym in all_symptoms]
    selected = st.multiselect(translate_text("Select Symptoms", lang), translated_symptoms)

    submit = st.form_submit_button(translate_text("Get Diagnosis", lang))

selected_symptoms = [all_symptoms[translated_symptoms.index(sym)] for sym in selected] if selected else []

if submit:
    if not name or not age or not selected_symptoms:
        st.error(translate_text("Please complete all fields.", lang))
    else:
        os.makedirs(PROFILE_DIR, exist_ok=True)
        profile = {"username": name, "age": age, "gender": gender}
        with open(os.path.join(PROFILE_DIR, f"{name}.json"), "w") as f:
            json.dump(profile, f, indent=4)

        symptom_severity_dict = {s: 2 for s in selected_symptoms}
        results = diagnose(symptom_severity_dict)

        entry = {
            "timestamp": datetime.now().isoformat(),
            "symptoms": selected_symptoms,
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

        top = results[0]
        plan = generate_7_day_plan(top['disease'])

        st.success(translate_text("✅ Diagnosis Complete", lang))
        st.markdown(f"**{translate_text('Top Match', lang)}**: {translate_text(top['disease'], lang)}")
        st.markdown(f"**{translate_text('Probability', lang)}**: {top['probability']}%")
        st.markdown(f"**{translate_text('Matched Symptoms', lang)}**: {', '.join(top['matched'])}")
        st.markdown(f"**{translate_text('Advice', lang)}**: {translate_text(top['advice'], lang)}")
        if top["link"]:
            st.markdown(f"[{translate_text('More info', lang)}]({top['link']})")

        st.subheader(translate_text("📅 7-Day Action Plan", lang))
        translated_plan = {translate_text(k, lang): translate_text(v, lang) for k, v in plan.items()}
        st.table(translated_plan)

        if st.button(translate_text("Download PDF Report", lang)):
            filename = os.path.join(CURRENT_DIR, f"{name}_diagnosis_report.pdf")
            generate_pdf(name, age, gender, results[:3], plan, filename)
            with open(filename, "rb") as f:
                pdf_data = f.read()
                b64 = base64.b64encode(pdf_data).decode()
                href = f'<a href="data:application/pdf;base64,{b64}" download="diagnosis_report.pdf">📄 Click here to download PDF</a>'
                st.markdown(href, unsafe_allow_html=True)