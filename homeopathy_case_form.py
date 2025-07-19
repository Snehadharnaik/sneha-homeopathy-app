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
    followup = record.get("FollowUp", str(date.today()))
    previous_symptoms = record.get("Symptoms", "")
    previous_manual = record.get("ManualSymptom", "")
    previous_notes = record.get("Notes", "")
    previous_medicine = record.get("PrescribedMedicine", "")
else:
    name = st.text_input("Full Name")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    contact = st.text_input("Contact Number")
    address = st.text_area("Address")
    followup = date.today()
    previous_symptoms = ""
    previous_manual = ""
    previous_notes = ""
    previous_medicine = ""

if service_type == "Case Taking":
    if selected_patient != "<New Patient>":
        st.write("### Previous Case Details")
        st.markdown(f"**Symptoms:** {previous_symptoms}")
        st.markdown(f"**Manual Symptoms:** {previous_manual}")
        st.markdown(f"**Notes:** {previous_notes}")
        st.markdown(f"**Prescribed Medicine:** {previous_medicine}")
        st.markdown(f"**Follow-Up:** {followup}")

    st.header("Current Visit")
    dropdown_symptoms = [
        "Headache", "Constipation", "Cough", "Skin rash", "Joint pain",
        "Sleeplessness", "Acidity", "Back pain", "Nausea", "Fever",
        "Irritability", "Fatigue", "Vertigo", "Anxiety", "Other"
    ]
    selected_symptoms = st.multiselect("Select Symptoms", dropdown_symptoms)
    manual_symptom = ""
    if "Other" in selected_symptoms:
        manual_symptom = st.text_area("Enter Additional Symptoms")

    repertory_map = {
        "Headache": ["Head - Pain - forehead - morning", "Belladonna, Natrum Mur"],
        "Constipation": ["Rectum - Constipation - ineffectual", "Nux Vomica, Bryonia"],
        "Sleeplessness": ["Sleep - Sleeplessness - from thoughts", "Coffea Cruda, Nux Vomica"],
        "Joint pain": ["Extremities - Pain - joints - rheumatic", "Rhus Tox, Bryonia"],
        "Skin rash": ["Skin - Eruptions - itching", "Sulphur, Apis, Graphites"]
    }

    st.subheader("Repertory Reference")
    for symptom in selected_symptoms:
        if symptom in repertory_map:
            rubric, remedies = repertory_map[symptom]
            st.markdown(f"**{symptom}** → *{rubric}*  ")
            st.markdown(f"Suggested: `{remedies}`")

    notes = st.text_area("Doctor's Notes")
    prescribed = st.text_input("Prescribed Medicines (Doctor Selected)")
    followup_new = st.date_input("Next Follow-Up Date", value=date.today())

    st.header("Download Case History")
    include_info = st.multiselect("Select sections to include in PDF", [
        "Patient Info", "Symptoms", "Manual Symptom", "Repertory", "Notes", "Medicine", "Follow-Up"
    ], default=["Patient Info", "Symptoms", "Notes", "Medicine"])

    if st.button("Download PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        if "Patient Info" in include_info:
            pdf.set_font("Arial", "B", 14)
            pdf.cell(200, 10, "Patient Information", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 8, f"Name: {name}", ln=True)
            pdf.cell(200, 8, f"Age: {age}", ln=True)
            pdf.cell(200, 8, f"Gender: {gender}", ln=True)
            pdf.cell(200, 8, f"Contact: {contact}", ln=True)
            pdf.multi_cell(200, 8, f"Address: {address}")

        if "Symptoms" in include_info:
            pdf.set_font("Arial", "B", 14)
            pdf.cell(200, 10, "Symptoms", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(200, 8, ", ".join([s for s in selected_symptoms if s != "Other"]))

        if "Manual Symptom" in include_info and manual_symptom:
            pdf.set_font("Arial", "B", 14)
            pdf.cell(200, 10, "Additional Symptoms", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(200, 8, manual_symptom)

        if "Repertory" in include_info:
            pdf.set_font("Arial", "B", 14)
            pdf.cell(200, 10, "Repertory Reference", ln=True)
            pdf.set_font("Arial", size=12)
            for symptom in selected_symptoms:
                if symptom in repertory_map:
                    rubric, remedies = repertory_map[symptom]
                    pdf.multi_cell(200, 8, f"{symptom} → {rubric}\nSuggested: {remedies}")

        if "Notes" in include_info:
            pdf.set_font("Arial", "B", 14)
            pdf.cell(200, 10, "Doctor's Notes", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(200, 8, notes)

        if "Medicine" in include_info:
            pdf.set_font("Arial", "B", 14)
            pdf.cell(200, 10, "Prescribed Medicine", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(200, 8, prescribed)

        if "Follow-Up" in include_info:
            pdf.set_font("Arial", "B", 14)
            pdf.cell(200, 10, "Follow-Up Date", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(200, 8, str(followup_new))

        file_name = f"{name.replace(' ', '_')}_case_history.pdf"
        pdf.output(file_name)

        with open(file_name, "rb") as f:
            st.download_button(
                label="Download Case History PDF",
                data=f,
                file_name=file_name,
                mime="application/pdf"
            )

    if st.button("Save Case Record"):
        new_record = {
            "Name": name,
            "Age": age,
            "Gender": gender,
            "Contact": contact,
            "Address": address,
            "FollowUp": followup_new,
            "Symptoms": ", ".join([s for s in selected_symptoms if s != "Other"]),
            "ManualSymptom": manual_symptom,
            "Notes": notes,
            "PrescribedMedicine": prescribed
        }
        df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
        df.to_csv(data_file, index=False)
        st.success(f"Case for {name} saved successfully!")

elif service_type == "Medical Certificate":
    st.header("Medical Leave Certificate Form")

    illness_reason = st.text_input("Diagnosis / Reason for Medical Leave")
    illness_start = st.date_input("Start Date of Leave")
    illness_end = st.date_input("End Date of Leave")
    issue_date = st.date_input("Date of Issue", value=date.today())
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
        cert.multi_cell(200, 10, f"This is to certify that Mr./Ms. {name}, aged {age}, was suffering from {illness_reason} and was under my care from {illness_start.strftime('%d-%m-%Y')} to {illness_end.strftime('%d-%m-%Y')}.

The patient was advised to refrain from work during this period.

This certificate is issued for medical leave purposes only.")
        cert.ln(10)
        cert.multi_cell(200, 10, f"Date: {issue_date}")

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
