import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import json
import warnings

warnings.filterwarnings("ignore")

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    """
        Given patient information, predict the probability of the patient having diabetes, by invoking the model API.
        Args:
            info_dict: dictionary containing the patient information
    """

    # get data
    data = request.get_json(force=True)

    feature_list = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
                    'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']

    features = [data[feature] for feature in feature_list]
    final_features = [np.array(features)]

    # load and predict
    model_weight = pickle.load(open("./../../models/anirudh_03152023/rf_model.pkl", 'rb'))
    prediction = model_weight.predict_proba(final_features)

    return jsonify(prediction.tolist())

@app.route('/compare', methods=['POST'])
def compare():
    """
        Compare the patient with the existing patients in the database.
        ArgS:
            info_dict: dictionary containing the target feature 
    """

    # get data
    data = request.get_json(force=True)
    compare_feature = data['feature']
    label_column = "Outcome"

    # read dataset
    df = pd.read_csv("./../../data/diabetes.csv")

    # get all values for this feature from the dataset
    feature_values = df[compare_feature].values
    target_values = df[label_column].values
    zipped = np.array(list(zip(feature_values, target_values)))

    # return as a list of tuples
    return jsonify(zipped.tolist())


if __name__ == "__main__":
    app.run(debug=True)

