import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import base64
from io import BytesIO
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model

cnn_bp = Blueprint('cnn', __name__)

UPLOAD_FOLDER = 'uploads'
CLASSIFICACOES_PERMITIDAS = {'saudavel', 'doente'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#carrega modelo
if os.path.exists('models/model_cnn.h5'):
    model = load_model('models/model_cnn.h5')
    print("Modelo CNN carregado!")
else:
    model = None
    print("Aviso: Rode train_cnn.py primeiro.")
    
@cnn_bp.route('/log/leaf_image', methods=['POST'])
def classificar_imagens():
    if 'classificacao' not in request.form:
        return jsonify({"error": "O campo 'classificacao' é obrigatório"}), 400
    if 'imagem' not in request.files:
        return jsonify({"error": "Nenhuma imagem foi enviada"}), 400
    
    classificacao_label = request.form['classificacao']
    imagem_file = request.files['imagem']
    
    if classificacao_label not in CLASSIFICACOES_PERMITIDAS:
        return jsonify({"error": f"Classificação '{classificacao_label}' não é permitida"}), 400
    if imagem_file.filename == '':
        return jsonify({"error": "Nenhuma imagem foi selecionada"}), 400
    if imagem_file:
        filename = secure_filename(imagem_file.filename)
        target_directory = os.path.join(UPLOAD_FOLDER, classificacao_label)
        os.makedirs(target_directory, exist_ok=True)
        save_path = os.path.join(target_directory, filename)
        imagem_file.save(save_path)
        
        return jsonify({
            "status": "Sucesso",
            "mensagem": "Imagem salva na pasta correspondente a sua classe",
            "nome_arquivo": filename,
            "classificacao": classificacao_label,
            "salvo_em": save_path
        }), 201
    
    return jsonify({"error": "Ocorreu um erro desconhecido"}), 500

@cnn_bp.route('/predict/leaf_image', methods=['POST'])
def predict_leaf():
    if model is None:
        return jsonify({'erro': 'Modelo CNN não treinado! Rode train_cnn.py primeiro.'}), 500
    data = request.json
    img_b64 = data.get('image_base64', '')  # {"image_base64": "base64string"}
    if not img_b64:  # <-- Fix: era 'img_64', agora 'img_b64'
        return jsonify({'erro': 'Envie "image_base64": "string" no JSON'}), 400
    try:
        img_data = base64.b64decode(img_b64)
        img = Image.open(BytesIO(img_data)).convert('RGB').resize((128, 128))
        X = np.expand_dims(np.array(img) / 255.0, axis=0)
        pred = model.predict(X, verbose=0)[0][0]
        classe = 'saudavel' if pred < 0.5 else 'doente'
        print(f"Previsão CNN: {classe} com prob {pred:.2f}")  # Debug no console Flask
        return jsonify({'previsao': classe, 'probabilidade': float(pred)})
    except Exception as e:
        return jsonify({'erro': f'Erro ao processar imagem: {str(e)}'}), 500