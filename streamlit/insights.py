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
    col1, col2 = st.columns([1, 1])

    # TODO: Add interactive widgets here to show some insights based on user input.
    data = pd.read_csv('./data/diabetes.csv')

    # input section
    with col1:
        bar_chart_feature = st.selectbox("Select a feature", options=data.columns)

    # output section
    with col2:

        # add bar chart to show the distribution of the diabetes positive and negative cases
        st.write(" ### Overall Distribution of Diabetes Positive and Negative Cases")
        st.bar_chart(data['Outcome'].value_counts())

        # add bar chart to show the distribution of the selected feature
        st.write(f"### {bar_chart_feature} Distribution")
        st.bar_chart(data.groupby('Outcome')[bar_chart_feature].mean())
