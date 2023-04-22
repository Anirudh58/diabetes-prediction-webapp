import os
import pickle
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

# Global config files

# paths
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(root_path, 'data')
dataset_path = os.path.join(data_path, 'diabetes.csv')
models_path = os.path.join(root_path, 'models')
model_folder_path = os.path.join(models_path, 'harsh_04212023')

# feature list
feature_list = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
                'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']

# model list
model_list = {
    'rf': 'Random Forest',
    'gb': 'Gradient Boosting',
    'dt': 'Decision Tree',
    'lr': 'Logistic Regression',
    'nn': 'Neural Network',
    'svm': 'Support Vector Machine'
}

# model descriptions
model_descriptions = {
    'rf': 'An ensemble learning method that constructs multiple decision trees and combines their results for accurate predictions.',
    'gb': 'A powerful machine learning technique that optimizes weak learners by minimizing the loss function using gradient descent.',
    'dt': 'A simple yet effective model that recursively splits data into subsets based on feature values, forming a tree structure.',
    'lr': 'A linear model for classification that predicts the probability of an event occurrence by fitting a logistic curve to the data.',
    'nn': 'A highly flexible, interconnected network of artificial neurons capable of learning complex patterns and approximating any function.',
    'svm': 'A classification algorithm that finds the optimal hyperplane to separate classes by maximizing the margin between support vectors.'
}

model_comments = {
    'rf': 'Test accuracy of 0.80. Not prone to overfitting. Strongly recommended for use.',
    'gb': 'Test accuracy of 0.72. It does not seem to be generalizing well.',
    'dt': 'Test accuracy of 0.79. Not prone to overfitting.',
    'lr': 'Test accuracy of 0.78. It does not seem to be generalizing well.',
    'nn': 'Test accuracy of 0.72. Works well. Can be used for prediction',
    'svm': 'Test accuracy of 0.78. Works well. Can be used for prediction.'
}


def get_probability(info_dict, models):
    """
        Given a patient information, this function returns the probability of the patient having diabetes.
        Args:
            info_dict: A dictionary containing the patient information
            models: List of models to use for prediction
                - 'rf': Random Forest
                - 'gb': Gradient Boosting
                - 'dt': Decision Tree
                - 'lr': Logistic Regression
                - 'nn': Neural Network
                - 'svm': Support Vector Machine
    """

    # feature list
    features = np.array([info_dict[feature] for feature in feature_list])

    # loop through all the input models and store predictions
    predictions = []
    for model_name in models:

        # load the model
        model_path = os.path.join(model_folder_path, f"{model_name}_model.pkl")
        model = pickle.load(open(model_path, 'rb'))

        # for logistic regression, the inputs need to go through minmax scaler
        if model_name=='lr':
            scaler_path = os.path.join(model_folder_path, f"{model_name}_scaler.pkl")
            scaler = pickle.load(open(scaler_path, 'rb'))
            scaled_features = scaler.transform(features.reshape(1, -1))
            prediction = model.predict_proba(scaled_features)[0][1]

        # the classes are reversed for neural network
        elif model_name == 'nn':
            prediction = model.predict_proba(features.reshape(1, -1))[0][0]

        else:
            prediction = model.predict_proba(features.reshape(1, -1))[0][1]

        # append the prediction
        predictions.append(prediction)

    # create a dataframe with the predictions and names of models
    df = pd.DataFrame({'Model': [model_list[model_name] for model_name in models], 'Diabetes Likelihood': predictions})

    return df

def compare_patient(compare_feature):
    """
        Given a target feature, this function returns all the points from the dataset for that feature, along with the label.
        Args:
            compare_feature: The feature to compare against the population
                - One of the features from the feature list
    """

    # read dataset
    df = pd.read_csv(dataset_path)

    label_column = "Outcome"

    # get all values for this feature from the dataset
    feature_values = df[compare_feature].values
    target_values = df[label_column].values
    zipped = np.array(list(zip(feature_values, target_values)))

    # return as a list of tuples
    return zipped.tolist()

def run_ui():

    # define columns for the nodes and edges csv upload widgets
    col1, col2 = st.columns([1,1])

    # input section
    with col1:

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
            models = st.multiselect("Select the models to use for prediction", format_func=lambda x: model_list[x], options=model_list.keys())

            submit_button = st.form_submit_button(label='Submit')

    # output section
    with col2:

        # add an expander section with a table of model descriptions
        expander = st.expander("Click here to see descriptions and comments of the models we trained and tested")
        with expander:
            st.table(pd.DataFrame({
                'Model': [model_list[key] for key in model_list],
                'Description': [model_descriptions[key] for key in model_list],
                'Comments': [model_comments[key] for key in model_list]
            }))
        
        
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

                # model inference
                model_output = get_probability(model_dict, models)

                # display in a table
                st.table(model_output)                

                # get feature values and label for the selected feature
                compare_output = compare_patient(compare_feature)

                feature_values = np.array([x[0] for x in compare_output])
                target_values = np.array([x[1] for x in compare_output])

                # plot a scatter plot to compare the patient with the existing patients
                st.markdown(f"<h4 style='text-align: center; color: white;'> Comparison of patient's {compare_feature} with the population </h4>", unsafe_allow_html=True)

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
                    width=750,
                    height=450
                )


                # add a horizontal line to show the patient's value for the selected feature
                rule = alt.Chart(pd.DataFrame({f'{compare_feature}': [model_dict[compare_feature]]})).mark_rule(color='yellow').encode(y=f'{compare_feature}')

                # add legend to show green for negative and red for positive and yellow for the patient's value
                legend = alt.Chart(pd.DataFrame({
                    'label': ['green', 'red', 'yellow'], 
                    'value': ['Negative', 'Positive', f"Patient"]
                    })).mark_point(size=100).encode(
                    y=alt.Y('value', axis=alt.Axis(orient='right', title=None)),
                    color=alt.Color('label', scale=None)
                )
                

                st.altair_chart(chart + rule | legend, use_container_width=True)

                



