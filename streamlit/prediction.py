import os
import sys

import numpy as np
import pandas as pd

import streamlit as st
import streamlit.components.v1 as components

import json
import requests

# append the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


def get_probability(info_dict):
    """
    This function makes a POST request to the prediction API and returns the probability of the person having diabetes.
    """

    url = "http://localhost:5000/predict"
    response = requests.post(url, json=info_dict)
    return response.json()

def run_ui():

    # define columns for the nodes and edges csv upload widgets
    col1, col2 = st.columns([1,1])

    # input section
    with col1:

        st.write("""
            ## Input Fields
            Please enter the values for the following fields:
        """)

        with st.form("input"):
            pregnancies = st.slider("Pregnancies", min_value=0, max_value=20, value=0)
            glucose = st.number_input("Glucose", value=168)
            bloodPressure = st.number_input("Blood Pressure", value=72)
            skinThickness = st.number_input("Skin Thickness", value=29)
            insulin = st.number_input("Insulin", value=0)
            bmi = st.slider("BMI", min_value=5.0, max_value=60.0, value=20.0)
            diabetesPedigreeFunction = st.number_input("Diabetes Pedigree Function", value=0.672)
            age = st.slider("Age", min_value=1, max_value=100, value=59)

            submit_button = st.form_submit_button(label='Submit')

    # output section
    with col2:
        st.write("""
            ## Output
            The probability for the given input is:
        """)

        
        if submit_button:

            with st.spinner('Calculating...'):
                input_dict = {
                    "pregnancies": pregnancies,
                    "glucose": glucose,
                    "bloodPressure": bloodPressure,
                    "skinThickness": skinThickness,
                    "insulin": insulin,
                    "BMI": bmi,
                    "diabetesPedigreeFunction": diabetesPedigreeFunction,
                    "age": age
                }
                output = get_probability(input_dict)
                
                # display output in a table
                st.table(pd.DataFrame(output, columns=['No Diabetes', 'Diabetes']))