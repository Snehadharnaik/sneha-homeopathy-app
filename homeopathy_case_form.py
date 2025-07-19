import streamlit as st
import pandas as pd
import os
from datetime import date
from fpdf import FPDF
from PyPDF2 import PdfReader, PdfWriter

# CSV file to store patient data
data_file = "patient_records.csv"

# Load existing data if exists
if os.path.exists(data_file):
    df = pd.read_csv(data_file)
else:
    df = pd.DataFrame(columns=[
        "Name", "Age", "Gender", "Contact", "Address", "FollowUp",
        "Symptoms", "ManualSymptom", "Notes", "PrescribedMedicine"
    ])

st.title("Homeopathy Patient Service - Dr. Sneha Amit Dharnaik")

# --- Service Selection ---
service_type = st.radio("Select Type of Form", ["Case Taking", "Medical Certificate"])

# --- Patient Selection ---
existing_patients = df["Name"].unique().tolist()
selected_patient = st.selectbox("Select Existing Patient or Type New Name", ["<New Patient>"] + existing_patients)

# --- Prefill if existing ---
if selected_patient != "<New Patient>":
    record = df[df["Name"] == selected_patient].iloc[-1]
    name = selected_patient
    age = record["Age"]
    gender = record["Gender"]
    contact = record["Contact"]
    address = record["Address"]
else:
    name = st.text_input("Full Name")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    contact = st.text_input("Contact Number")
    address = st.text_area("Address")

if service_type == "Medical Certificate":
    certificate_text = st.text_area("Customize Certificate Text", 
        f"This is to certify that Mr./Ms. {name}, aged {age}, has been examined and advised medical rest due to health condition.")
    issue_date = st.date_input("Date of Issue", value=date.today())
    signature_path = st.file_uploader("Upload Doctor's Digital Signature", type=["png", "jpg"])
    stamp_path = st.file_uploader("Upload Clinic Stamp", type=["png", "jpg"])
    secure_pdf = st.checkbox("Secure with password?", value=False)
    password = ""
    if secure_pdf:
        password = st.text_input("Enter PDF Password")

    if st.button("Download Medical Certificate"):
        cert = FPDF()
        cert.add_page()
        cert.set_font("Arial", "B", 16)
        cert.cell(200, 10, "Medical Certificate", ln=True, align='C')
        cert.set_font("Arial", size=12)
        cert.ln(10)
        cert.multi_cell(200, 10, certificate_text)
        cert.ln(10)
        cert.multi_cell(200, 10, f"Date: {issue_date}")

        # Save and draw images if uploaded
        if signature_path is not None:
            sign_file = f"sign_{name}.png"
            with open(sign_file, "wb") as f:
                f.write(signature_path.getbuffer())
            cert.image(sign_file, x=20, y=230, w=40)

        if stamp_path is not None:
            stamp_file = f"stamp_{name}.png"
            with open(stamp_file, "wb") as f:
                f.write(stamp_path.getbuffer())
            cert.image(stamp_file, x=140, y=230, w=40)

        cert_file = f"{name.replace(' ', '_')}_medical_certificate.pdf"
        cert.output(cert_file)

        # Apply password protection if selected
        if secure_pdf and password:
            reader = PdfReader(cert_file)
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            writer.encrypt(password)
            secure_file = f"secure_{cert_file}"
            with open(secure_file, "wb") as f:
                writer.write(f)
            with open(secure_file, "rb") as f:
                st.download_button("Download Secured Medical Certificate", data=f, file_name=secure_file, mime="application/pdf")
        else:
            with open(cert_file, "rb") as f:
                st.download_button("Download Medical Certificate", data=f, file_name=cert_file, mime="application/pdf")
