import streamlit as st
from joblib import load
import pandas as pd

st.title("Welcome to Cardio Predict")

# Initialize the submissions DataFrame in session state if it doesn't exist
if 'submissions' not in st.session_state:
    st.session_state.submissions = pd.DataFrame(columns=[
        "Name", "Age Years", "Age Months", "gender", "height", "weight", 
        "systolic BP", "diastolic BP", "cholesterol", "glucose", "smoke", "alcohol", "ctive"
    ])

with st.form(key='user_input_form'):
    name = st.text_input("Enter your full name")
    st.write("Please Enter your age in Years and Months.")
    age_years = st.number_input("Years", min_value=0, max_value=200, step=1)
    age_months = st.number_input("Months", min_value=0, max_value=11, step=1)
    age = (age_years*12)+age_months
    
    gender = st.radio("Select your gender:", options=['Select', 'Male', 'Female'], index=0)
    if gender == "Male":
        gender = 1
    elif gender == "Female":
        gender =0
    else:
        gender = -1
    
    
    height = st.number_input("Please enter your Height in cm", min_value=0.0, format="%0.2f")
    weight = st.number_input("Please enter your weight in Kilogram", min_value=0.0, format="%0.2f")
    ap_hi = st.number_input("Please enter Systolic Blood Pressure", min_value=0)
    ap_lo = st.number_input("Please enter Diastolic Blood Pressure", min_value=0)
    
    
    cholesterol = st.radio("Do you have Cholesterol", options=["Select", "Normal", "High", "Exceptionally high"])
    if cholesterol == "Normal":
        cholesterol = 0
    elif cholesterol == "High":
        cholesterol = 1
    elif cholesterol == "Exceptionally high":
        cholesterol =2    
    else:
        cholesterol = -1
    
    
    gluc = st.radio("What is the level of your glucose?", options=["Select", "Normal", "High", "Exceptionally high"])
    if gluc == "Normal":
        gluc = 0
    elif gluc == "High":
        gluc = 1
    elif gluc == "Exceptionally high":
        gluc =2    
    
    
    smoke = st.radio("Do you smoke?", options=["Select", "Yes", "No"])
    if smoke == "Yes":
        smoke = 1
    elif smoke == "No":
        smoke = 0
    else:
        smoke =-1

    
    alco = st.radio("Are you Alcoholic?", options=["Select", "Yes", "No"])
    if alco == "Yes":
        alco = 1
    elif alco == "No":
        alco = 0
    else:
        alco =-1
    
    
    active = st.radio("Are you physically active?", options=['Select', 'Yes', 'No'])
    if active == "Yes":
        active = 1
    elif active == "No":
        active = 0
    else:
        active =-1

    # Submit button for the form
    submit_button = st.form_submit_button(label='Submit')

# Logic to handle the form submission
if submit_button:
    new_data = {
        "Name": name,
        "Age Years": age_years,
        "Age Months": age_months,
        "age":age,
        "gender": gender,
        "height": height,
        "weight": weight,
        "ap_hi": ap_hi,
        "ap_lo": ap_lo,
        "cholesterol": cholesterol,
        "gluc": gluc,
        "smoke": smoke,
        "alco": alco,
        "active": active
    }

    # Convert the dictionary to a DataFrame
    new_df = pd.DataFrame([new_data])
    
    # Append the new data to the existing DataFrame in session state
    st.session_state.submissions = pd.concat([st.session_state.submissions, new_df], ignore_index=True)
    
    # Optionally display the updated DataFrame
  

    user_prediction = new_df[["age","gender","height","weight","ap_hi","ap_lo","cholesterol","gluc","smoke","alco","active"]]


    model = load("XGB.joblib")
    prediction = model.predict(user_prediction)
    if prediction == 0:
        st.markdown("## Congratulations, you are not at risk of Cardiovascular Diseases.")
    elif prediction == 1:
        st.wmarkdown("## I am sorry to inform you that you are at the risk of Cardiovascular diseases.")
