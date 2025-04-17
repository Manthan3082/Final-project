import gradio as gr
from diagnosis_engine import diagnose
from user_profile import save_user_profile
from health_history import save_health_history
from action_plan import generate_7_day_plan

all_symptoms = [
    "fever", "cough", "sneezing", "sore throat", "fatigue", "chills", "muscle aches",
    "headache", "nausea", "light sensitivity", "shortness of breath", "loss of smell",
    "diarrhea", "vomiting", "stomach pain", "chest tightness", "wheezing"
]

def run_safe_diagnosis(name, age, gender, symptoms):
    if not name or not age or not symptoms:
        return "Please complete all fields.", "No diagnosis.", {}

    try:
        # Save user profile
        save_user_profile(name, age, gender)

        # Basic symptom weighting
        symptom_severity_dict = {symptom: 2 for symptom in symptoms}
        results = diagnose(symptom_severity_dict)

        # Save to history
        save_health_history(name, symptoms, results)

        top_disease = results[0]['disease']
        plan = generate_7_day_plan(top_disease)

        result = results[0]
        output_text = f"Disease: {result['disease']}\nSymptoms: {', '.join(result['matched'])}\nAdvice: {result['advice']}"

        return "Diagnosis completed.", output_text, plan

    except Exception as e:
        return f"Error: {str(e)}", "Error occurred.", {}

demo = gr.Interface(
    fn=run_safe_diagnosis,
    inputs=[
        gr.Textbox(label="Name"),
        gr.Textbox(label="Age"),
        gr.Radio(["Male", "Female", "Other"], label="Gender"),
        gr.CheckboxGroup(choices=all_symptoms, label="Select Symptoms")
    ],
    outputs=[
        gr.Textbox(label="Status"),
        gr.Textbox(label="Diagnosis Summary"),
        gr.Dataframe(label="7-Day Health Plan")
    ],
    title="🧠 Health Diagnosis Helper (Safe Mode)",
    description="Lightweight version to avoid browser crashes. Just enter details and get your result!"
)

if __name__ == "__main__":
    demo.launch()