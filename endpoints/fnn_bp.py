import csv
import os
from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
import threading

fnn_bp = Blueprint('fnn_bp', __name__)

LOG_FILE = 'soil_data_logs.csv'  
CSV_FIELDNAMES = ['rendimento_alvo', 'precipitacao', 'temperatura_max', 'temperatura_min', 'elevacao']
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
    
        flash('Dados enviados com sucesso!')
        return redirect(url_for('fnn_bp.inserir_soil_data'))

    return render_template('fnn_template.html')