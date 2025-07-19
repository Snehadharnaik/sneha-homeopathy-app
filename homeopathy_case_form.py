import streamlit as st
from fpdf import FPDF

# --- Title ---
st.title("Homeopathy Case History Form")
st.subheader("Dr. Sneha Amit Dharnaik (Classical Homeopathy)")

# --- Patient Info ---
st.header("1. Patient Information")
name = st.text_input("Full Name")
age = st.number_input("Age", 0, 120, step=1)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
contact = st.text_input("Contact Number")
address = st.text_area("Address")

# --- Medical Case History ---
st.header("2. Medical Case History")
chief_complaints = st.text_area("Chief Complaints")
onset = st.text_input("Onset")
location = st.text_input("Location")
sensation = st.text_input("Sensation")
modalities = st.text_input("Modalities")
associated = st.text_input("Associated Symptoms")

# --- Symptoms and Remedies ---
st.header("3. Select Symptoms")
symptoms = [
    "Headache", "Constipation", "Cough", "Skin rash", "Joint pain",
    "Sleeplessness", "Acidity", "Back pain"
]
selected_symptoms = st.multiselect("Choose Presenting Symptoms", symptoms)

remedy_map = {
    "Headache": "Belladonna",
    "Constipation": "Nux Vomica",
    "Cough": "Bryonia",
    "Skin rash": "Sulphur",
    "Joint pain": "Rhus Tox",
    "Sleeplessness": "Coffea Cruda",
    "Acidity": "Carbo Veg",
    "Back pain": "Calcarea Phos"
}
suggested_remedies = [remedy_map[s] for s in selected_symptoms if s in remedy_map]

# --- Notes ---
st.header("4. Doctor's Notes")
doctor_notes = st.text_area("Additional Notes")

# --- Include in PDF ---
st.header("5. Select What to Include in PDF")
include = {
    "Patient Info": st.checkbox("Patient Information", True),
    "Medical History": st.checkbox("Medical Case History", True),
    "Symptoms": st.checkbox("Symptoms & Suggested Medicines", True),
    "Doctor Notes": st.checkbox("Doctor's Notes", True)
}

# --- Generate PDF ---
if st.button("Download PDF"):

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    if include["Patient Info"]:
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, "Patient Information", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 8, f"Name: {name}", ln=True)
        pdf.cell(200, 8, f"Age: {age}", ln=True)
        pdf.cell(200, 8, f"Gender: {gender}", ln=True)
        pdf.cell(200, 8, f"Contact: {contact}", ln=True)
        pdf.multi_cell(200, 8, f"Address: {address}")
        pdf.ln()

    if include["Medical History"]:
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, "Medical Case History", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(200, 8, f"Chief Complaints: {chief_complaints}")
        pdf.cell(200, 8, f"Onset: {onset}", ln=True)
        pdf.cell(200, 8, f"Location: {location}", ln=True)
        pdf.cell(200, 8, f"Sensation: {sensation}", ln=True)
        pdf.cell(200, 8, f"Modalities: {modalities}", ln=True)
        pdf.cell(200, 8, f"Associated Symptoms: {associated}", ln=True)
        pdf.ln()

    if include["Symptoms"]:
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, "Symptoms & Suggested Remedies", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(200, 8, f"Symptoms: {', '.join(selected_symptoms)}")
        pdf.multi_cell(200, 8, f"Suggested Remedies: {', '.join(set(suggested_remedies))}")
        pdf.ln()

    if include["Doctor Notes"]:
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, "Doctor's Notes", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(200, 8, doctor_notes)
        pdf.ln()

    # Save to file
    file_path = f"{name.replace(' ', '_')}_case_history.pdf"
    pdf.output(file_path)

    # Serve PDF to user
    with open(file_path, "rb") as f:
        st.download_button(
            label="Download Case History PDF",
            data=f,
            file_name=file_path,
            mime="application/pdf"
        )
