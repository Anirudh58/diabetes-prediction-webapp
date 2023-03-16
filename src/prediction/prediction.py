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
    input_json = request.get_json(force=True)
    features = [input_json['pregnancies'], input_json['glucose'], input_json['bloodPressure'], input_json['skinThickness'],
                input_json['insulin'], input_json['BMI'], input_json["diabetesPedigreeFunction"],
                input_json['age']]
    final_features = [np.array(features)]

    model_weight = pickle.load(open("./../../models/anirudh_03152023/rfc_model.pkl", 'rb'))
    prediction = model_weight.predict_proba(final_features)
    output = prediction[0][1]

    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)

