import streamlit as st
import pandas as pd
import os
from datetime import date

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

st.title("Homeopathy Case History - Dr. Sneha Amit Dharnaik")

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
    followup = record["FollowUp"]
    previous_symptoms = record["Symptoms"]
    previous_manual = record["ManualSymptom"]
    previous_notes = record["Notes"]
    previous_medicine = record["PrescribedMedicine"]
else:
    name = st.text_input("Full Name")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    contact = st.text_input("Contact Number")
    address = st.text_area("Address")
    followup = st.date_input("Follow-Up Date", value=date.today())
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

# Symptom selection
dropdown_symptoms = [
    "Headache", "Constipation", "Cough", "Skin rash", "Joint pain",
    "Sleeplessness", "Acidity", "Back pain", "Nausea", "Fever",
    "Irritability", "Fatigue", "Vertigo", "Anxiety", "Other"
]
selected_symptoms = st.multiselect("Select Symptoms", dropdown_symptoms)
manual_symptom = ""
if "Other" in selected_symptoms:
    manual_symptom = st.text_area("Enter Additional Symptoms")

# Repertory reference
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
