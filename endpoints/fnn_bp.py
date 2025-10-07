from flask import Blueprint, request, jsonify
from tensorflow.keras.models import load_model
import joblib
import pandas as pd
import numpy as np
import os

fnn_bp = Blueprint('fnn', __name__)

#carrega modelo e scaler
if os.path.exists('models/model_fnn.h5') and os.path.exists('models/preprocessor_fnn.pkl'):
    model = load_model('models/model_fnn.h5')
    scaler = joblib.load('models/preprocessor_fnn.pkl')
    print("Modelo FNN carregado!")
else:
    model = None
    scaler = None
    print("Aviso: Rode train_fnn.py primeiro.")
    
@fnn_bp.route('/log/soil_data', methods=['POST'])
def log_soil():
    data = request.json
    new_df = pd.DataFrame([data])
    new_df.to_csv('data/soil_data_logs.csv', mode='a', header=False, index=False)
    return jsonify({'status': 'dados solo salvos no CSV'})

@fnn_bp.route('/predict/soil_data', methods=['POST'])
def predict_soil():
    if model is None or scaler is None:
        return jsonify({'erro': 'Modelo FNN não treinado! Rode train_fnn.py primeiro.'}), 500
    data = request.json
    df = pd.DataFrame([data])
    X = scaler.transform(df[['precipitacao', 'temperatura_max', 'temperatura_min', 'elevacao']])
    pred = model.predict(X, verbose=0) [0] [0]
    classe = 'rendimento_alto' if pred > 0.5 else 'rendimento_baixo'
    return jsonify({'previsao': classe, 'probabilidade': float(pred)})