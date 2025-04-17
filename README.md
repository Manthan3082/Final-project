# Health Diagnosis Helper

This is a Streamlit-based health diagnosis app that allows users to:
- Select symptoms
- Get disease probability predictions
- Receive a 7-day action plan
- Export health reports as PDF
- Translate content dynamically
- Login and track their diagnosis history

## How to Run Locally

```bash
pip install -r requirements.txt
streamlit run health_diagnosis_with_reset_updated.py
```

## Deploy to Render

1. Push this folder to a GitHub repo.
2. Go to [Render.com](https://render.com) → New Web Service.
3. Connect your repo and select:
   - Runtime: Python
   - Start Command: `streamlit run health_diagnosis_with_reset_updated.py`
4. Deploy!