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

    # TODO: Add interactive widgets here to show some insights based on user input.


    data = pd.read_csv('./data/diabetes.csv')

    # add bar chart to show the distribution of the diabetes positive and negative cases
    st.write(""" Ratio of diabetes positive and negative cases in the dataset: """)
    st.bar_chart(data['Outcome'].value_counts())

    # find out if the pregnancies has anything to do with the outcome
    st.write(""" Number of pregnancies vs Outcome:  """)
    st.bar_chart(data.groupby('Outcome')['Pregnancies'].mean())

    # find out if the glucose has anything to do with the outcome
    st.write(""" Glucose vs Outcome: """)
    st.bar_chart(data.groupby('Outcome')['Glucose'].mean())

    # find out if the blood pressure has anything to do with the outcome
    st.write(""" Blood Pressure vs Outcome: """)
    st.bar_chart(data.groupby('Outcome')['BloodPressure'].mean())

    # find out if the skin thickness has anything to do with the outcome
    st.write(""" Skin Thickness vs Outcome: """)
    st.bar_chart(data.groupby('Outcome')['SkinThickness'].mean())

    # find out if the insulin has anything to do with the outcome
    st.write(""" Insulin vs Outcome: """)
    st.bar_chart(data.groupby('Outcome')['Insulin'].mean())

    # find out if the bmi has anything to do with the outcome
    st.write(""" BMI vs Outcome: """)
    st.bar_chart(data.groupby('Outcome')['BMI'].mean())

    # find out if the diabetes pedigree function has anything to do with the outcome
    st.write(""" Diabetes Pedigree Function vs Outcome: """)
    st.bar_chart(data.groupby('Outcome')['DiabetesPedigreeFunction'].mean())

    # find out if the age has anything to do with the outcome
    st.write(""" Age vs Outcome: """)
    st.bar_chart(data.groupby('Outcome')['Age'].mean())



