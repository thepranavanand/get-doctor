import streamlit as st
from openai import OpenAI
import os

api_key = ""
client = OpenAI(
    api_key=api_key
)
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def replace_placeholder(template, placeholder, replacement):
    return template.replace(placeholder, replacement)

def get_openai_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

st.title("Medical Condition Detailer and Doctor Finder")

patient_description = st.text_area("Describe your symptoms:")

def display_doctor_card(doctor, index):
    st.markdown(f"""
        <div style="border:1px solid #ccc; border-radius:10px; padding:10px; margin:10px; text-align:center;">
            <h4>{doctor['name']}</h4>
            <p>ID: {doctor['id']}</p>
            <p>Specialization: {doctor['specialization']}</p>
            <p>Reason: {doctor['reason']}</p>
            <button style="padding: 5px 10px; border:none; border-radius:5px; background-color:#4CAF50; color:white;" onclick="window.location.href = '?book={index}'">Book Appointment</button>
        </div>
    """, unsafe_allow_html=True)


if st.button("Find Details and Doctor"):
    if patient_description:
        detailer_template = read_file('detailer_prompt.txt')
        doctor_finder_template = read_file('doctor_finder_prompt.txt')
        doctors_list = read_file('doctors.txt')

        detailed_symptoms_prompt = replace_placeholder(detailer_template, '[PATIENT_SYMPTOMS]', patient_description)
        print(detailed_symptoms_prompt)
        detailed_symptoms = get_openai_response(detailed_symptoms_prompt)

        doctor_finder_prompt = replace_placeholder(doctor_finder_template, '[SYMPTOM_LIST]', detailed_symptoms)
        doctor_finder_prompt = replace_placeholder(doctor_finder_prompt, '[DOCTORS_LIST]', doctors_list)

        print(doctor_finder_prompt)

        doctor_suggestion = get_openai_response(doctor_finder_prompt)

        print(doctor_suggestion)
        doctor_list = eval(doctor_suggestion)

        st.subheader("Detailed Symptoms")
        st.write(detailed_symptoms)

        st.subheader("Doctor Suggestion")
        if doctor_list:
            for i, doctor in enumerate(doctor_list):
                display_doctor_card(doctor, i)
        else:
            st.write("No doctors found.")
    else:
        st.warning("Please enter your symptoms.")