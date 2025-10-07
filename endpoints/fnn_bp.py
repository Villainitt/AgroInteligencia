from flask import Blueprint, request, jsonify, render_template, url_for
import threading
import csv
from tensorflow.keras.models import load_model
import joblib
import pandas as pd
import numpy as np
import os

fnn_bp = Blueprint('fnn', __name__)

MODEL_PATH = 'models/model_fnn.h5'
SCALER_PATH = 'models/preprocessor_fnn.pkl'


model = None
scaler = None

# modelo 
if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
    print("Carregando modelo e scaler...")
    model = load_model(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    print("Modelo e scaler carregados com sucesso!")
else: 
    print(f"AVISO: Arquivo de modelo ('{MODEL_PATH}') ou scaler ('{SCALER_PATH}') não encontrado.")
    print("O endpoint de predição retornará um erro até que os arquivos existam.")

@fnn_bp.route('/predict', methods = ['GET'])
def predict_data():
    return render_template('fnn_template.html')

@fnn_bp.route('/predict/soildata', methods=['POST'])
def predict_soil():
    if model is None or scaler is None:
        return jsonify({'erro': 'Modelo FNN não treinado! Rode train_fnn.py primeiro.'}), 500
    data = request.json
    print("Dados recebidos, começando a predição...")

    try: 
        features = ['precipitacao', 'temperatura_max', 'temperatura_min', 'elevacao']
        df = pd.DataFrame([data], columns=features)
        X = scaler.transform(df)
        pred = model.predict(X, verbose=0) [0] [0]
        classe = 'rendimento_alto' if pred > 0.5 else 'rendimento_baixo'
        return jsonify({'previsao': classe, 'probabilidade': float(pred)})
    except Exception as e:
        print(f"Erro durane a predição: {e}")
        return jsonify({'erro': f'Ocorreu um erro: {e}'}), 400


# log
LOG_FILE = 'soil_data_logs.csv'  
CSV_FIELDNAMES = ['rendimento_alvo', 'precipitacao', 'temperatura_media', 'materia_organica', 'ph_solo']
file_lock = threading.Lock()

@fnn_bp.route('/log/soil_data', methods=['GET','POST'])
def inserir_soil_data(): 
    
    if request.method == 'POST':

        print(f"Dados recebidos do formulário {request.form}")

        received_data = request.form.to_dict()
    
        for field in CSV_FIELDNAMES:
            print(f"Validando campo: '{field}'")
            if field not in received_data:
                print(f"ERRO: Campo '{field}' não foi encontrado nos dados recebidos!\n")
                flash(f"Erro: O campo obrigatório {field} não foi encontrado")
                return redirect(url_for('fnn_bp.inserir_soil_data'))
   
        log_entry = {field: received_data.get(field) for field in CSV_FIELDNAMES}
        file_lock.acquire()

        try:
            file_exists = os.path.isfile(LOG_FILE)
            with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDNAMES)
                if not file_exists:
                    writer.writeheader()
                writer.writerow(log_entry)
        finally:
            file_lock.release()
