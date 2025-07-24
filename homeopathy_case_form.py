import streamlit as st
from io import BytesIO
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
        "Symptoms", "ManualSymptom", "Notes", "PrescribedMedicine",
        "GeneralComplaints", "MentalSymptoms", "Modalities", "Sleep", "Appearance",
        "Appetite", "Thirst", "Perspiration", "Stool", "Urine", "Menstrual",
        "Obstetric", "FamilyHistory", "PastHistory", "PersonalHistory"
    ])

st.set_page_config(page_title="Dr. Sneha Amit Dharnaik - Homeopathy", layout="wide")

# --- Logout Button ---
st.sidebar.markdown("## Doctor Account")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.success("Logged out!")
    st.stop()

# --- Doctor Login ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Doctor Login")
    reset = st.checkbox("Forgot Password?")
    if reset:
        new_password = st.text_input("Enter new password")
        confirm_password = st.text_input("Confirm new password", type="password")
        if st.button("Reset Password"):
            if new_password == confirm_password and new_password.strip():
                st.success("Password reset is not yet implemented in cloud deployment. Please contact admin.")
            else:
                st.error("Passwords do not match or are empty.")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "doctor" and password == "dharnaik@14":
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
            st.stop()
        else:
            st.error("Invalid credentials")
    st.stop()

st.title("Homeopathy Patient Service - Dr. Sneha Amit Dharnaik")
tabs = st.tabs(["Case Taking Form", "Patient History", "Medical Certificate"])

with tabs[0]:
        
    # --- Patient Selection ---
    existing_patients = df["Name"].unique().tolist()
    selected_patient = st.selectbox("Select Existing Patient or Type New Name", ["<New Patient>"] + existing_patients)

    # --- Prefill if existing ---
    general_complaints_options = ["Pain", "Weakness", "Fever", "Cough", "Headache", "Fatigue", "Other"]
    general_complaints = st.selectbox("General Complaints", general_complaints_options)
    if general_complaints == "Other":
        general_complaints = st.text_input("Enter other general complaints")
    mental_symptoms_options = ["Anxiety", "Depression", "Irritability", "Fear", "Mood Swings", "Other"]
    mental_symptoms = st.selectbox("Mental and Emotional Symptoms", mental_symptoms_options)
    if mental_symptoms == "Other":
        mental_symptoms = st.text_input("Enter other mental symptoms")
    modalities_options = ["Better by Rest", "Worse in Cold", "Worse in Evening", "Better in Open Air", "Other"]
    modalities = st.selectbox("Modalities (What makes it better/worse)", modalities_options)
    if modalities == "Other":
        modalities = st.text_input("Enter other modalities")
    sleep_options = ["Sound", "Disturbed", "Insomnia", "Nightmares", "Excessive", "Other"]
    sleep = st.selectbox("Sleep Pattern", sleep_options)
    if sleep == "Other":
        sleep = st.text_input("Enter other sleep pattern")
    appearance_options = ["Pale", "Healthy", "Obese", "Thin", "Other"]
    appearance = st.selectbox("General Appearance", appearance_options)
    if appearance == "Other":
        appearance = st.text_input("Enter other appearance")
    appetite_options = ["Normal", "Increased", "Decreased", "Cravings", "Aversions", "Other"]
    appetite = st.selectbox("Appetite & Food Desires/Aversions", appetite_options)
    if appetite == "Other":
        appetite = st.text_input("Enter other appetite detail")
    thirst_options = ["Normal", "Increased", "Decreased", "Dry Mouth", "Other"]
    thirst = st.selectbox("Thirst", thirst_options)
    if thirst == "Other":
        thirst = st.text_input("Enter other thirst detail")
    perspiration_options = ["Normal", "Excessive", "Less", "Offensive", "Other"]
    perspiration = st.selectbox("Perspiration", perspiration_options)
    if perspiration == "Other":
        perspiration = st.text_input("Enter other perspiration detail")
    stool_options = ["Normal", "Constipation", "Loose", "Incomplete", "Other"]
    stool = st.selectbox("Stool Pattern", stool_options)
    if stool == "Other":
        stool = st.text_input("Enter other stool pattern")
    urine_options = ["Normal", "Burning", "Frequent", "Scanty", "Other"]
    urine = st.selectbox("Urine Pattern", urine_options)
    if urine == "Other":
        urine = st.text_input("Enter other urine pattern")
    menstrual = st.text_area("Menstrual History (if applicable)")
    obstetric = st.text_area("Obstetric History (if applicable)")
    family_history = st.text_area("Family History")
    past_history = st.text_area("Past Medical History")
    personal_history = st.text_area("Personal History")

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
        age = st.number_input("Age", min_value=0, max_value=120, step=1, key="case_age")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        contact = st.text_input("Contact Number")
        address = st.text_area("Address")
        followup = date.today()
        previous_symptoms = ""
        previous_manual = ""
        previous_notes = ""
        previous_medicine = ""

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
        homeopathy_medicines = [
            "Belladonna", "Nux Vomica", "Bryonia", "Sulphur", "Rhus Tox",
            "Coffea Cruda", "Natrum Mur", "Graphites", "Apis", "Carbo Veg",
            "Pulsatilla", "Aconite", "Arnica", "Ignatia", "Phosphorus"
        ]
        prescribed = st.multiselect("Select Prescribed Medicines", homeopathy_medicines)
        prescribed_str = ", ".join(prescribed)
        followup_new = st.date_input("Next Follow-Up Date", value=date.today())

        st.header("Download Case History")
        include_info = st.multiselect("Select sections to include in PDF", [
            "Patient Info", "Symptoms", "Manual Symptom", "Repertory", "Notes", "Medicine", "Follow-Up"
        ], default=["Patient Info", "Symptoms", "Notes", "Medicine"])

        import tempfile
from PyPDF2 import PdfReader, PdfWriter

st.header("Download Case History")
include_info = st.multiselect("Select sections to include in PDF", [
    "Patient Info", "Symptoms", "Manual Symptom", "Repertory", "Notes", "Medicine", "Follow-Up"
], default=["Patient Info", "Symptoms", "Notes", "Medicine"])

if st.button("Download PDF"):
    # Step 1: Create the case PDF as usual, but save to a temp file
    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf = FPDF()
    pdf.set_margins(10, 15, 10)
    pdf.add_page()
    pdf.set_font("Times", size=12)
    
    # (Add all your PDF content creation code here as before...)
    # For example:
    if "Patient Info" in include_info:
        pdf.set_font("Times", "B", 14)
        pdf.cell(200, 10, "Patient Information", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 8, f"Name: {name}", ln=True)
        pdf.cell(200, 8, f"Age: {age}", ln=True)
        pdf.cell(200, 8, f"Gender: {gender}", ln=True)
        pdf.cell(200, 8, f"Contact: {contact}", ln=True)
        pdf.multi_cell(200, 8, f"Address: {address}")

    # ... [add all other sections as before, unchanged] ...

    pdf.output(temp_pdf.name)
    temp_pdf.close()
    
    # Step 2: Overlay your letterhead.pdf onto the first page
    with open("letterhead.pdf", "rb") as f:
        letterhead_reader = PdfReader(f)
        letterhead_page = letterhead_reader.pages[0]

    with open(temp_pdf.name, "rb") as f:
        case_reader = PdfReader(f)
        writer = PdfWriter()

        # Overlay the first page
        first_content_page = case_reader.pages[0]
        letterhead_page.merge_page(first_content_page)
        writer.add_page(letterhead_page)

        # Add remaining pages (without letterhead)
        for i in range(1, len(case_reader.pages)):
            writer.add_page(case_reader.pages[i])

        final_pdf_path = f"{name.replace(' ', '_')}_case_history.pdf"
        with open(final_pdf_path, "wb") as fout:
            writer.write(fout)

    # Step 3: Download
    with open(final_pdf_path, "rb") as f:
        st.download_button(
            label="Download Case History PDF",
            data=f,
            file_name=final_pdf_path,
            mime="application/pdf"
        )

include_info = st.multiselect("Select sections to include in PDF", [
    "Patient Info", "Symptoms", "Manual Symptom", "Repertory", "Notes", "Medicine", "Follow-Up"
], default=["Patient Info", "Symptoms", "Notes", "Medicine"])

if st.button("Download PDF"):
    pdf = FPDF()
    pdf.set_margins(10, 15, 10)
    pdf.add_page()
    pdf.set_font("Times", size=12)

    if "Patient Info" in include_info:
        pdf.set_font("Times", "B", 14)
        pdf.cell(200, 10, "Patient Information", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 8, f"Name: {name}", ln=True)
        pdf.cell(200, 8, f"Age: {age}", ln=True)
        pdf.cell(200, 8, f"Gender: {gender}", ln=True)
        pdf.cell(200, 8, f"Contact: {contact}", ln=True)
        pdf.multi_cell(200, 8, f"Address: {address}")

    if "Symptoms" in include_info:
        pdf.set_font("Times", "B", 14)
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

        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, "Detailed Case History", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(200, 8, f"General Complaints: {general_complaints}")
        pdf.multi_cell(200, 8, f"Mental & Emotional Symptoms: {mental_symptoms}")
        pdf.multi_cell(200, 8, f"Modalities: {modalities}")
        pdf.multi_cell(200, 8, f"Sleep: {sleep}")
        pdf.multi_cell(200, 8, f"Appearance: {appearance}")
        pdf.multi_cell(200, 8, f"Appetite: {appetite}")
        pdf.multi_cell(200, 8, f"Thirst: {thirst}")
        pdf.multi_cell(200, 8, f"Perspiration: {perspiration}")
        pdf.multi_cell(200, 8, f"Stool: {stool}")
        pdf.multi_cell(200, 8, f"Urine: {urine}")
        pdf.multi_cell(200, 8, f"Menstrual History: {menstrual}")
        pdf.multi_cell(200, 8, f"Obstetric History: {obstetric}")
        pdf.multi_cell(200, 8, f"Family History: {family_history}")
        pdf.multi_cell(200, 8, f"Past Medical History: {past_history}")
        pdf.multi_cell(200, 8, f"Personal History: {personal_history}")

    if "Medicine" in include_info:
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, "Prescribed Medicine", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(200, 8, prescribed_str)

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
                "GeneralComplaints": general_complaints,
                "MentalSymptoms": mental_symptoms,
                "Modalities": modalities,
                "Sleep": sleep,
                "Appearance": appearance,
                "Appetite": appetite,
                "Thirst": thirst,
                "Perspiration": perspiration,
                "Stool": stool,
                "Urine": urine,
                "Menstrual": menstrual,
                "Obstetric": obstetric,
                "FamilyHistory": family_history,
                "PastHistory": past_history,
                "PersonalHistory": personal_history,
                "PrescribedMedicine": prescribed_str
            }
            df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
            df.to_csv(data_file, index=False)
            st.success(f"Case for {name} saved successfully!")

with tabs[1]:
    st.header("Patient History Table")
    if st.button("Export All Records to Excel"):
        output = BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)
        st.download_button("Download Excel File", data=output, file_name="patient_records.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    if not df.empty:
        st.dataframe(df.drop(columns=["PrescribedMedicine"]))
        selected_name = st.selectbox("Select patient to view detailed case", df["Name"].unique())
        patient_details = df[df["Name"] == selected_name].iloc[-1]
        st.subheader("Patient Summary")
        st.markdown(f"**Name:** {patient_details['Name']}")
        st.markdown(f"**Age/Gender:** {patient_details['Age']} / {patient_details['Gender']}")
        st.markdown(f"**Symptoms:** {patient_details['Symptoms']}")
        st.markdown(f"**Prescribed Medicines:** {patient_details['PrescribedMedicine']}")
        with st.expander("View Full Case History"):
            for col in df.columns:
                st.markdown(f"**{col}**: {patient_details[col]}")
    else:
        st.info("No patient records found.")

with tabs[2]:
    st.header("Generate Medical Certificate")
    st.markdown("Upload your digital signature and clinic stamp (only once; saved locally).")
    sig_path = "signature.png"
    stamp_path = "stamp.png"
    sig_uploaded = st.file_uploader("Upload Signature (PNG)", type="png")
    stamp_uploaded = st.file_uploader("Upload Stamp (PNG)", type="png")
    if sig_uploaded:
        with open(sig_path, "wb") as f:
            f.write(sig_uploaded.read())
    if stamp_uploaded:
        with open(stamp_path, "wb") as f:
            f.write(stamp_uploaded.read())

    cert_name = st.text_input("Patient Full Name")
    cert_age = st.number_input("Age", min_value=0, max_value=120, step=1, key="cert_age")
    cert_illness = st.text_input("Illness / Reason")
    illness_start = st.date_input("Illness From Date")
    illness_end = st.date_input("Illness To Date")
    issue_date = st.date_input("Certificate Issue Date", value=date.today())

    if st.button("Download Medical Certificate"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Times", "B", 16)
        pdf.cell(200, 10, "Medical Certificate", ln=True, align='C')
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(200, 10, f"This is to certify that Mr./Ms. {cert_name}, aged {cert_age}, was suffering from {cert_illness} and was under my care from {illness_start.strftime('%d-%m-%Y')} to {illness_end.strftime('%d-%m-%Y')}.")
        pdf.ln(5)
        pdf.multi_cell(200, 10, f"The patient was advised medical rest during this period.\nIssued on {issue_date.strftime('%d-%m-%Y')} for official use.")

        # Add images if available
        if os.path.exists(sig_path):
            pdf.image(sig_path, x=10, y=220, w=40)
        if os.path.exists(stamp_path):
            pdf.image(stamp_path, x=150, y=220, w=40)

        cert_file = f"{cert_name.replace(' ', '_')}_medical_certificate.pdf"
        pdf.output(cert_file)
        with open(cert_file, "rb") as f:
            st.download_button("Download Certificate", data=f, file_name=cert_file, mime="application/pdf")
