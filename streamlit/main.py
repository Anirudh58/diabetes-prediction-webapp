import os
import sys

import numpy as np
import pandas as pd

import streamlit as st

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# streamlit pages
import prediction
import insights

# TODO: Add more pages later
PAGES = [
    'PREDICTION',
    'INSIGHTS'
]

def run_ui():

    st.set_page_config(
        page_title="Glucowise - Diabetes Prediction",
        page_icon="🏠",
        initial_sidebar_state="expanded",
        layout="wide",
    )

    st.sidebar.title("Glucowise - Diabetes Prediction")
    page=st.sidebar.radio('Navigation', PAGES, index=st.session_state.page)


    if page == 'PREDICTION':
        st.sidebar.write("""
            ## Overview
            This page allows you to predict the probability of a person having diabetes based on their medical history.
        """)

        prediction.run_ui()

    elif page == 'INSIGHTS':
        st.sidebar.write("""
            ## Overview
            This page allows you to explore the data and get some general insights about the dataset.
        """)

        insights.run_ui()

if __name__ == "__main__":
    
    
    if st.experimental_get_query_params().get('page'):
        st.session_state.page = PAGES.index(st.experimental_get_query_params().get('page')[0])
    else:
        st.session_state.page = 0

    
    

    run_ui()