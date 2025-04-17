import json
import os

CURRENT_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(CURRENT_DIR, "data", "diseases.json")

with open(DATA_PATH) as f:
    DISEASES = json.load(f)

def diagnose(symptom_severity_dict):
    results = []

    for disease, details in DISEASES.items():
        score = 0
        matched_symptoms = []

        for symptom, weight in details["symptoms"].items():
            if symptom in symptom_severity_dict:
                severity = symptom_severity_dict[symptom]
                score += severity * weight
                matched_symptoms.append(f"{symptom} (x{severity})")

        if score > 0:
            results.append({
                "disease": disease,
                "score": score,
                "matched": matched_symptoms,
                "advice": details["advice"],
                "link": details["link"]
            })

    if not results:
        return [{
            "disease": "No clear match",
            "score": 0,
            "matched": [],
            "advice": "Please consult a doctor.",
            "link": ""
        }]

    # Normalize scores to percentage
    max_score = max(r["score"] for r in results)
    for r in results:
        r["probability"] = round((r["score"] / max_score) * 100, 2)

    results.sort(key=lambda x: x["score"], reverse=True)
    return results