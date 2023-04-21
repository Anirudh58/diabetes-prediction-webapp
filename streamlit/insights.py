import os
import sys

import numpy as np
import pandas as pd

import streamlit as st
import matplotlib.pyplot as plt
import altair as alt

# append the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


def run_ui():

    # read the df
    data = pd.read_csv('./data/diabetes.csv')

    # input section
    _, col1, col2, _ = st.columns([1, 2, 2, 1])

    with col1:
        feature_1 = st.selectbox("Select feature 1", options=data.columns, key='feature_1')

    with col2:
        feature_2 = st.selectbox("Select feature 2", options=data.columns, key='feature_2')

    # line separator
    st.markdown(" --- ")

    # plot section
    _, col3, _ = st.columns([1, 1, 1])

    with col3:

        # center the title
        st.markdown("<h3 style='text-align: center; color: white;'> Overall Distribution of Patients</h3>", unsafe_allow_html=True)

        # bar chart to show the distribution of patients
        df1 = data['Outcome'].value_counts()
        df1.index = ['Negative', 'Positive']
        df1.name = 'Count'

        # plot a bar chart with altair,
        st.altair_chart(alt.Chart(df1.reset_index()).mark_bar().encode(
            x=alt.X('index:O', axis=alt.Axis(title='Outcome')),
            y=alt.Y('Count:Q', axis=alt.Axis(title='Count')),
            color=alt.Color('index', scale=alt.Scale(domain=['Negative', 'Positive'], range=['#1f77b4', '#d62728'])),
            tooltip=['index', 'Count']
        ).interactive(), use_container_width=True)

        

    # line separator
    st.markdown(" --- ")

    col4, col5, col6 = st.columns([1, 1.5, 1])

    with col4:

        # center the title
        st.markdown(f"<h3 style='text-align: center; color: white;'> {feature_1} Distribution </h3>", unsafe_allow_html=True)

        df2 = data.groupby('Outcome')[feature_1].mean()
        df2.index = ['Negative', 'Positive']
        df2.name = 'Mean'
    
        # plot a bar chart with altair,
        st.altair_chart(alt.Chart(df2.reset_index()).mark_bar().encode(
            x=alt.X('index:O', axis=alt.Axis(title='Outcome')),
            y=alt.Y('Mean:Q', axis=alt.Axis(title='Mean')),
            color=alt.Color('index', scale=alt.Scale(domain=['Negative', 'Positive'], range=['#1f77b4', '#d62728'])),
            tooltip=['index', 'Mean']
        ).interactive(), use_container_width=True)
        

    with col5:
        
        # scatter plot showing the relationship between the two features
        st.markdown(f"<h3 style='text-align: center; color: white;'> {feature_1} vs {feature_2} </h3>", unsafe_allow_html=True)

        # altair plot
        
        st.altair_chart(alt.Chart(data).mark_circle().encode(
            x=feature_1,
            y=feature_2,
            # red for positive and blue for negative
            color=alt.Color('Outcome', scale=alt.Scale(domain=[0, 1], range=['#1f77b4', '#d62728'])),
            tooltip=['Outcome']
        ).interactive(), use_container_width=True)



    with col6:
            
        # center the title
        st.markdown(f"<h3 style='text-align: center; color: white;'> {feature_2} Distribution </h3>", unsafe_allow_html=True)

        df3 = data.groupby('Outcome')[feature_2].mean()
        df3.index = ['Negative', 'Positive']
        df3.name = 'Mean'

        # plot a bar chart with altair,
        st.altair_chart(alt.Chart(df3.reset_index()).mark_bar().encode(
            x=alt.X('index:O', axis=alt.Axis(title='Outcome')),
            y=alt.Y('Mean:Q', axis=alt.Axis(title='Mean')),
            color=alt.Color('index', scale=alt.Scale(domain=['Negative', 'Positive'], range=['#1f77b4', '#d62728'])),
            tooltip=['index', 'Mean']
        ).interactive(), use_container_width=True)

    