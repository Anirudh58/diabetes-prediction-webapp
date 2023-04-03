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

    # "pregnancies": 0, 
    # "glucose" : 168, 
    # "bloodPressure": 72, 
    # "skinThickness": 29, 
    # "insulin": 0, 
    # "BMI": 28.1, 
    # "diabetesPedigreeFunction": 0.672,
    # "age": 59
    with st.form('My Form'):
        name = st.text_input('Enter your name')
        pregnancies = st.text_input('Enter number of pregnancies')
        glucose = st.text_input('Enter glucose levels')
        bloodPressure = st.text_input('Enter blood pressure levels')
        skinThickness = st.text_input('Enter skin thickness')
        insulin = st.text_input('Enter insulin levels')
        bmi = st.text_input('Enter BMI')
        age = st.text_input('Enter your age')
        submit_button = st.form_submit_button(label='Submit')

