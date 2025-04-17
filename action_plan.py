def generate_7_day_plan(disease_name):
    base_advice = {
        "Common Cold": ["Rest", "Drink warm fluids", "Steam inhalation", "Eat light", "Avoid cold drinks", "Lozenges", "Doctor if worsens"],
        "Flu": ["Stay in bed", "Hydrate", "Digestible food", "Paracetamol", "Warm compress", "Monitor temp", "Visit doctor"],
        "Migraine": ["Avoid light", "Take meds", "Rest", "Hydrate", "Watch triggers", "Reduce screen time", "Neurologist visit"],
        "COVID-19": ["Isolate", "Monitor oxygen", "Paracetamol", "Hot water", "Pulse check", "Wear mask", "Emergency if needed"],
        "Food Poisoning": ["No solid food", "ORS", "Rest", "Rice & banana", "No dairy", "Monitor symptoms", "Doctor if vomiting"],
        "Asthma": ["Use inhaler", "Avoid triggers", "Stay indoors", "Meds", "Track breath", "Breathing exercises", "Emergency care"]
    }

    plan = base_advice.get(disease_name, ["Consult a doctor."] * 7)
    return {f"Day {i+1}": plan[i] for i in range(7)}