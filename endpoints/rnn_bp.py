from flask import Blueprint, request, jsonify
import pandas as pd
import numpy as np
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os

rnn_bp = Blueprint('rnn', __name__)

# Carrega modelo e tokenizer salvos (Etapa 3)
if os.path.exists('models/model_rnn.h5') and os.path.exists('models/tokenizer_rnn.pkl'):
    model = load_model('models/model_rnn.h5')
    with open('models/tokenizer_rnn.pkl', 'rb') as f:
        tokenizer = pickle.load(f)
    max_len = 50  # Mesmo do treino
    print("Modelo RNN carregado!")
else:
    print("Erro: Rode train_rnn.py primeiro!")
    model = None
    tokenizer = None

# Endpoint /log/note (já deve ter da Etapa 1, mas adicione se não)
@rnn_bp.route('/log/note', methods=['POST'])
def log_note():
    data = request.json  # {"nota": "texto", "rotulo": "urgente"}
    new_df = pd.DataFrame([data])
    new_df.to_csv('data/field_notes_database.csv', mode='a', header=False, index=False)
    return jsonify({'status': 'nota salva no CSV'})

# Endpoint /predict/note (novo, Etapa 4)
@rnn_bp.route('/predict/note', methods=['POST'])
def predict_note():
    if model is None or tokenizer is None:
        return jsonify({'erro': 'Modelo não treinado! Rode train_rnn.py primeiro.'}), 500
    data = request.json
    texto = data.get('nota', '')  # Ex: "Infestação severa!"
    if not texto:
        return jsonify({'erro': 'Envie "nota": "texto" no JSON'}), 400
    seq = tokenizer.texts_to_sequences([texto])
    X = pad_sequences(seq, maxlen=max_len)
    pred = model.predict(X, verbose=0)[0][0]
    classe = 'urgente' if pred > 0.5 else 'rotina'
    return jsonify({'previsao': classe, 'probabilidade': float(pred)})

# Registre no main.py: app.register_blueprint(rnn_bp, url_prefix='/rnn')