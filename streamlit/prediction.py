import os
import sys
import time

import numpy as np
import pandas as pd

import streamlit as st
import matplotlib.pyplot as plt
import altair as alt

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

        #st.markdown(f"<h3 style='text-align: center; color: white;'> INPUT </h3>", unsafe_allow_html=True)

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
        #st.markdown(f"<h3 style='text-align: center; color: white;'> OUTPUT </h3>", unsafe_allow_html=True)

        
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
                st.table(pd.DataFrame(model_output, columns=['Diabetes Negative', 'Diabetes Positive']))

                # add key to input dict
                compare_dict = {}
                compare_dict['feature'] = compare_feature
                compare_dict['value'] = model_dict[compare_feature]

                # invoke the model comparison API
                compare_output = compare_patient(compare_dict)
                feature_values = np.array([x[0] for x in compare_output])
                target_values = np.array([x[1] for x in compare_output])

                # plot a scatter plot to compare the patient with the existing patients
                st.markdown(f"<h3 style='text-align: center; color: white;'> Comparison with the population </h3>", unsafe_allow_html=True)

                # scatter plot with altair
                df = pd.DataFrame({
                    'patient_id': range(len(feature_values)),
                    f'{compare_feature}': feature_values,
                    'label': ['green' if x == 0 else 'red' for x in target_values]
                })

                chart = alt.Chart(df).mark_circle(size=30).encode(
                    x='patient_id',
                    y=f'{compare_feature}',
                    color=alt.condition(
                        alt.datum.label == 'green',
                        alt.value('green'),
                        alt.value('red')
                    )
                ).properties(
                    width=600,
                    height=450
                )

                # add a horizontal line to show the patient's value for the selected feature
                rule = alt.Chart(pd.DataFrame({f'{compare_feature}': [model_dict[compare_feature]]})).mark_rule(color='yellow').encode(y=f'{compare_feature}')

                # add legend to show green for negative and red for positive and yellow for the patient's value
                legend = alt.Chart(pd.DataFrame({
                    'label': ['green', 'red', 'yellow'], 
                    'value': ['Negative', 'Positive', f"Patient's {compare_feature}"]
                    })).mark_point(size=100).encode(
                    y=alt.Y('value', axis=alt.Axis(orient='right', title=None)),
                    color=alt.Color('label', scale=None)
                )
                

                st.altair_chart(chart + rule | legend, use_container_width=True)

                



