import csv
import os
import datetime
from flask import Flask, request, jsonify
import pandas as pd
import threading

app = Flask(__name__)

# --- Configuração para o arquivo CSV ---
LOG_FILE = 'soil_data_logs.csv'  # Nome do arquivo mais específico
# Define as colunas do nosso CSV.
CSV_FIELDNAMES = ['rendimento_alvo', 'precipitacao', 'temperatura_max', 'temperatura_min', 'elevacao']

# Cria um Lock para controlar o acesso ao arquivo
file_lock = threading.Lock()
# ----------------------------------------

@app.route('/log/soil_data', methods=['POST'])
def ingest_soil_data(): # Nome da função mais descritivo
    """
    Endpoint para receber dados de solo e salvá-los em um arquivo CSV.
    """
    if not request.is_json:
        return jsonify({"error": "A requisição deve ser do tipo JSON"}), 400

    received_data = request.get_json()

    # --- VALIDAÇÃO CORRIGIDA ---
    # Verifica se todos os campos necessários estão presentes na requisição.
    for field in CSV_FIELDNAMES:
        if field not in received_data:
            return jsonify({"error": f"O campo obrigatório '{field}' não foi encontrado"}), 400
    # ---------------------------

    # O dicionário 'log_entry' já está perfeito como você fez.
    # Estamos apenas usando a variável com o novo nome 'received_data'
    log_entry = {
        'rendimento_alvo': received_data.get('rendimento_alvo'),
        'precipitacao': received_data.get('precipitacao'),
        'temperatura_max': received_data.get('temperatura_max'),
        'temperatura_min': received_data.get('temperatura_min'),
        'elevacao': received_data.get('elevacao')
    }

    # --- Bloco de escrita segura no arquivo (seu código aqui já estava perfeito) ---
    file_lock.acquire()
    try:
        file_exists = os.path.isfile(LOG_FILE)
        with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDNAMES)
            if not file_exists:
                writer.writeheader()
            writer.writerow(log_entry)
    except Exception as e:
        return jsonify({"error": f"Erro ao escrever no arquivo CSV: {str(e)}"}), 500
    finally:
        file_lock.release()
    # -----------------------------------------

    return jsonify({"status": "Dados de solo salvos com sucesso no CSV"}), 201

if __name__ == '__main__':
    app.run(debug=True)

print("ok")