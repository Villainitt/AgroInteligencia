import pandas as pd
import numpy as np
import pickle
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import os

# Caminho correto pro CSV de texto na pasta data/
csv_path = 'data/field_notes_database.csv'
if not os.path.exists(csv_path):
    print(f"Erro: Arquivo '{csv_path}' não encontrado. Confirme se tá na pasta data/!")
    exit()

try:
    df = pd.read_csv(csv_path)
    print("Dataset de texto carregado com sucesso de data/!")
    print("Primeiras linhas:\n", df.head())
    print(f"Shape: {df.shape} (linhas, colunas)")
except Exception as e:
    print(f"Erro ao ler CSV: {e}")
    exit()

# Colunas esperadas: 'nota' (texto) e 'rotulo' ('urgente'/'rotina' ou 0/1)
if 'nota' not in df.columns or 'rotulo' not in df.columns:
    print("Erro: Colunas 'nota' e 'rotulo' não encontradas. Verifique o CSV (ex: nota=texto, rotulo=urgente/rotina).")
    exit()

texts = df['nota'].fillna('').values  # Textos (preenche NaN com vazio)
df['rotulo_num'] = df['rotulo'].map({'rotina': 0, 'urgente': 1}).fillna(0)  # Converte pra binário 0/1
y = df['rotulo_num'].values

print(f"Textos exemplo: {texts[:2]}")
print(f"Targets y: {y[:5]} (0=rotina, 1=urgente)")

# Tokeniza o texto (pré-processamento pra RNN)
max_words = 1000  # Vocabulário máximo
max_len = 50  # Comprimento máximo da sequência
tokenizer = Tokenizer(num_words=max_words, oov_token='<OOV>')  # OOV pra palavras desconhecidas
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)  # <-- LINHA FALTANDO ANTES!
X = pad_sequences(sequences, maxlen=max_len, padding='post')  # Pad pra tamanho fixo

# Salva tokenizer pra usar no /predict
os.makedirs('models', exist_ok=True)  # Cria pasta se não tem
with open('models/tokenizer_rnn.pkl', 'wb') as f:
    pickle.dump(tokenizer, f)

print(f"Sequências X shape: {X.shape}")

# Divide dados
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Treino: {X_train.shape}, Teste: {X_test.shape}")

# Modelo RNN/LSTM
model = Sequential([
    Embedding(max_words, 64, input_length=max_len),  # Embedding pra texto
    LSTM(64, return_sequences=False),  # LSTM layer
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')  # Binário
])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Treina
history = model.fit(X_train, y_train, epochs=20, batch_size=min(8, len(X_train)), validation_data=(X_test, y_test), verbose=1)

# Avalia e salva
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"Treino RNN concluído! Loss: {loss:.2f}, Acurácia no teste: {accuracy:.2f}")

model.save('models/model_rnn.h5')
print("Modelo salvo em models/model_rnn.h5")