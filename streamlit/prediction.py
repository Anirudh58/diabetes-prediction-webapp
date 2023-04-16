import os
import sys

import numpy as np
import pandas as pd

import streamlit as st
import streamlit.components.v1 as components

# append the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


def run_ui():

    # define columns for the nodes and edges csv upload widgets
    col1, col2 = st.columns([1,1])

    # input section
    with col1:

        st.write("""
            ## Input Fields
            Please enter the values for the following fields:
        """)

        pregnancies = st.slider("Pregnancies", min_value=0, max_value=20)
        glucose = st.number_input("Glucose")
        bloodPressure = st.number_input("Blood Pressure")
        skinThickness = st.number_input("Skin Thickness")
        insulin = st.number_input("Insulin")
        bmi = st.slider("BMI", min_value=5.0, max_value=60.0)
        diabetesPedigreeFunction = st.number_input("Diabetes Pedigree Function")
        age = st.slider("Age", min_value=1, max_value=100)

    # output section
    with col2:
        st.write("""
            ## Output
            The probability of the person having diabetes is:
        """)

        # define the output field
        output = st.empty()

