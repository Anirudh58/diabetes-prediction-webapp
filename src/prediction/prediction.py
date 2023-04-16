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

    # get data
    data = request.get_json(force=True)

    features = [data['pregnancies'], data['glucose'], data['bloodPressure'], data['skinThickness'],
                data['insulin'], data['BMI'], data["diabetesPedigreeFunction"],
                data['age']]
    final_features = [np.array(features)]

    model_weight = pickle.load(open("./../../models/anirudh_03152023/rf_model.pkl", 'rb'))
    prediction = model_weight.predict_proba(final_features)
    
    return jsonify(prediction.tolist())

if __name__ == "__main__":
    app.run(debug=True)

