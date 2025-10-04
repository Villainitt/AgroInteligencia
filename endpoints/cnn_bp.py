import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

cnn_bp = Blueprint('cnn_bp', __name__)

UPLOAD_FOLDER = 'imagens'
CLASSIFICACOES_PERMITIDAS = {'saudavel', 'doente'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@cnn_bp.route('/log/leaf_image', methods=['POST'])
def classificar_imagens():
    if 'classificacao' not in request.form:
        return jsonify({"error": "O campo 'classificacao' é obrigatório" }), 400
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
        os.makedirs(target_directory, exist_ok= True)
        save_path = os.path.join(target_directory, filename)
        imagem_file.save(save_path)

        return jsonify ({
            "status": "Sucesso",
            "mensagem": "Imagem salva na pasta correspondente a sua classe",
            "nome_arquivo": filename,
            "classificacao": classificacao_label,
            "salvo_em": save_path
        }), 201
    
    return jsonify ({"error": "Ocorreu um erro desconhecido"}), 500