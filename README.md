# AgroInteligencia 🌱

Plataforma integrada de inteligência artificial para o agronegócio, combinando ferramentas visuais de classificação e análise textual com uma API robusta para coleta de dados telemétricos.

## 📋 Funcionalidades

O projeto é dividido em dois módulos principais:

### 🖥️ Módulo Web (Interface de Classificação)
Acesso via navegador para análise em tempo real:
1.  **Saúde das Folhagens (CNN):** Diagnóstico visual de doenças em plantas através do upload de imagens. Classifica em "saudável" ou "doente".
2.  **Classificação de Atividades (RNN):** Análise de notas de campo (texto) para identificar a urgência da atividade. Classifica em "rotina" ou "urgente".
3.  **Classificação de Solo (FNN):** *[Funcionalidade planejada/existente - descrever se já estiver implementada ou manter como placeholder se for o caso]*

### ⚙️ Módulo API (Ingestão de Dados e Logs)
Acesso via sistemas externos (Postman, sensores IoT) ou internamente pela aplicação web:
* **Registro Telemétrico (FNN):** Endpoint para receber dados numéricos de solo (rendimento, precipitação, etc.) e registrá-los em `soil_data_logs.csv`.
* **Log de Imagens (CNN):** Endpoint para salvar imagens classificadas em pastas organizadas (`uploads/saudavel`, `uploads/doente`).
* **Log de Notas (RNN):** Endpoint para registrar novas notas de campo no banco de dados CSV (`data/field_notes_database.csv`).

## 🚀 Como Utilizar

### Pré-requisitos
* [Python 3.8+](https://www.python.org/downloads/) instalado.
* [Git](https://git-scm.com/) (opcional, para clonar o repositório).

### 🔧 Instalação e Configuração

1.  **Clone o repositório:**
    ```bash
    git clone [https://seu-repositorio-aqui.com/agrointeligencia.git](https://seu-repositorio-aqui.com/agrointeligencia.git)
    cd agrointeligencia
    ```

2.  **Crie e ative um ambiente virtual (.venv):**
    * Windows: `python -m venv .venv` depois `.venv\Scripts\activate`
    * Linux/macOS: `python3 -m venv .venv` depois `source .venv/bin/activate`

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Treine os modelos (Necessário na primeira execução):**
    Para que as funcionalidades de IA funcionem, você precisa treinar os modelos primeiro. Execute os scripts de treino:
    ```bash
    python train_cnn.py  # Treina o classificador de imagens
    python train_rnn.py  # Treina o classificador de texto
    python train_fnn.py # Treina o classificador de dados numéricos
    ```
    *Certifique-se de que os dados de treino estejam nas pastas corretas (`data/`, `uploados`) antes de rodar os scripts.*

### ▶️ Executando a Aplicação

1.  Com o ambiente virtual ativo, inicie o servidor Flask:
    ```bash
    python app.py
    ```
2.  Acesse a interface web em `http://127.0.0.1:5000/`.

### 🔍 Acessando as Funcionalidades via API (Exemplos)

* **Classificar Imagem (CNN):**
    * **URL:** `POST http://127.0.0.1:5000/predict/leaf_image`
    * **JSON Body:** `{"image_base64": "sua_string_base64_aqui"}`

* **Classificar Nota (RNN):**
    * **URL:** `POST http://127.0.0.1:5000/predict/note`
    * **JSON Body:** `{"nota": "Infestação severa detectada no setor norte!"}`

* **Registrar Dados de Solo (FNN):**
    * **URL:** `POST http://127.0.0.1:5000/log/soil_data`
    * **JSON Body:** `{"rendimento_alvo": 0.8, "precipitacao": 120, ...}`

## 📂 Estrutura do Projeto
``` /agrointeligencia
├── main.py
├── requirements.txt
├── data/
│   └── field_notes_database.csv
│   └── soil_data_logs.csv
├── models/
│   ├── model_cnn.h5
│   ├── model_cnn.keras
│   ├── model_fnn.h5
│   ├── model_rnn.h5
│   ├── preprocessor_fnn.pkl
│   └── tokenizer_rnn.pkl
├── uploads/
│   ├── saudavel/
│   └── doente/
├── static/
│   ├── assets/
│   ├── anotacoes.js
│   ├── predict.js
│   ├── imagem.js
│   ├── style_cnn.css
│   ├── style_fnn.css
│   ├── style_rnn.css
│   └── style_index.css
├── templates/
│   ├── index.html
│   ├── cnn_template.html
│   ├── fnn_template.html
│   └── rnn_template.html
└── endpoints/
    ├── fnn_bp.py
    ├── cnn_bp.py
    └── rnn_bp.py
```

---
**Nota:** Este projeto foi desenvolvido para fins acadêmicos e de demonstração de aplicação de IA no agronegócio.