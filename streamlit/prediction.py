import os
import sys
import time

import numpy as np
import pandas as pd

import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt

import json
import requests

# append the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


def get_probability(info_dict):
    """
    This function makes a POST request to the prediction API and returns the probability of the person having diabetes.
    """

    url = "http://localhost:5000/predict"

    
    while True:
    
        try:
            response = requests.post(url, json=info_dict, headers={"Content-Type": "application/json"})
            return response.json()
        except Exception as e:
            # wait for some time and try again
            time.sleep(1)
            continue

def compare_patient(info_dict):
    """
        Given a patient information, this function compares the patient with the existing patients in the database.
        Returns box plot of the patient's information compared to the existing patients.
    """

    url = "http://localhost:5000/compare"

    while True:

        try:
            response = requests.post(url, json=info_dict, headers={"Content-Type": "application/json"})
            return response.json()
        except Exception as e:
            # wait for some time and try again
            time.sleep(1)
            continue


def run_ui():

    # define columns for the nodes and edges csv upload widgets
    col1, col2 = st.columns([1,1])

    # input section
    with col1:

        st.write("""
            ## Input
        """)

        feature_list = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
                    'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']

        with st.form("input"):
            pregnancies = st.slider("Pregnancies", min_value=0, max_value=20, value=0)
            glucose = st.number_input("Glucose", value=168)
            bloodPressure = st.number_input("Blood Pressure", value=72)
            skinThickness = st.number_input("Skin Thickness", value=29)
            insulin = st.number_input("Insulin", value=0)
            bmi = st.slider("BMI", min_value=5.0, max_value=60.0, value=20.0)
            diabetesPedigreeFunction = st.number_input("Diabetes Pedigree Function", value=0.672)
            age = st.slider("Age", min_value=1, max_value=100, value=59)
            compare_feature = st.selectbox("Select a feature to compare against the population", options=feature_list)

            submit_button = st.form_submit_button(label='Submit')

    # output section
    with col2:
        st.write("""
            ## Output
        """)

        
        if submit_button:
            
            # invoke the model prediction API
            with st.spinner('Calculating...'):
                model_dict = {
                    "Pregnancies": pregnancies,
                    "Glucose": glucose,
                    "BloodPressure": bloodPressure,
                    "SkinThickness": skinThickness,
                    "Insulin": insulin,
                    "BMI": bmi,
                    "DiabetesPedigreeFunction": diabetesPedigreeFunction,
                    "Age": age
                }
                model_output = get_probability(model_dict)
                
                # display output in a table
                st.table(pd.DataFrame(model_output, columns=['Chance of not having Diabetes', 'Chance of having Diabetes']))

                # add key to input dict
                compare_dict = {}
                compare_dict['feature'] = compare_feature
                compare_dict['value'] = model_dict[compare_feature]

                # invoke the model comparison API
                compare_output = compare_patient(compare_dict)
                feature_values = np.array([x[0] for x in compare_output])
                target_values = np.array([x[1] for x in compare_output])

                # plot a scatter plot to compare the patient with the existing patients
                st.write(f"### Comparison of patient's {compare_feature} with the population")

                # table explaining the plot
                st.table(
                    pd.DataFrame([
                        ['Green', 'Patient without diabetes'], 
                        ['Red', 'Patient with diabetes'], 
                        ['Blue', 'Patient\'s value for the selected feature']
                    ], columns=['Color', 'Description']))

                fig = plt.figure(figsize=(10, 5))
                plt.scatter(x=range(len(feature_values)), y=feature_values, c=['g' if x == 0 else 'r' for x in target_values], s=5)
                plt.axhline(y=model_dict[compare_feature], color='b', linestyle='-', linewidth=1)
                plt.xlabel("Patient ID")
                plt.ylabel(compare_feature)
                plt.title(f"Comparison of patient's {compare_feature} with the population")
                st.pyplot(fig)
                



