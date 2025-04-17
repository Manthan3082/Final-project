from fpdf import FPDF

class DiagnosisPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Health Diagnosis Report", ln=True, align="C")
        self.ln(10)

    def add_user_info(self, name, age, gender):
        self.set_font("Arial", "", 12)
        self.cell(0, 10, f"Name: {name}", ln=True)
        self.cell(0, 10, f"Age: {age}", ln=True)
        self.cell(0, 10, f"Gender: {gender}", ln=True)
        self.ln(5)

    def add_diagnosis(self, diagnosis):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Diagnosis:", ln=True)
        self.set_font("Arial", "", 12)
        for res in diagnosis:
            self.multi_cell(0, 10, f"- {res['disease']} (Score: {res['score']})\nAdvice: {res['advice']}")
        self.ln(5)

    def add_action_plan(self, plan):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "7-Day Health Plan:", ln=True)
        self.set_font("Arial", "", 12)
        for day, advice in plan.items():
            self.cell(0, 10, f"{day}: {advice}", ln=True)
        self.ln(5)

def generate_pdf(name, age, gender, diagnosis, plan, filename="diagnosis_report.pdf"):
    pdf = DiagnosisPDF()
    pdf.add_page()
    pdf.add_user_info(name, age, gender)
    pdf.add_diagnosis(diagnosis)
    pdf.add_action_plan(plan)
    pdf.output(filename)
    return filename