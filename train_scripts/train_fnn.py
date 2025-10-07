import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import os

# Caminho correto pro CSV na pasta data/
csv_path = 'data/soil_data_logs.csv'
if not os.path.exists(csv_path):
    print(f"Erro: Arquivo '{csv_path}' não encontrado. Confirme se tá na pasta data/!")
    exit()

try:
    df = pd.read_csv(csv_path)
    print("Dataset carregado com sucesso de data/!")
    print("Primeiras linhas:\n", df.head())
    print(f"Shape: {df.shape} (linhas, colunas)")
except Exception as e:
    print(f"Erro ao ler CSV: {e}")
    exit()

# Features e target (colunas do seu CSV)
feature_cols = ['precipitacao', 'temperatura_max', 'temperatura_min', 'elevacao']
if not all(col in df.columns for col in feature_cols + ['rendimento_alvo']):
    print("Erro: Colunas esperadas não encontradas. Verifique o CSV.")
    exit()

X = df[feature_cols].values
y = df['rendimento_alvo'].values

print(f"Features X shape: {X.shape}, Target y: {y}")

# Pré-processa (escala features)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
os.makedirs('models', exist_ok=True)
joblib.dump(scaler, 'models/preprocessor_fnn.pkl')  # Salva em models/ (crie se não tem)

# Divide dados
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
print(f"Treino: {X_train.shape}, Teste: {X_test.shape}")

# Modelo FNN
model = Sequential([
    Dense(64, activation='relu', input_shape=(X.shape[1],)),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
])
model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])

# Treina
history = model.fit(X_train, y_train, epochs=50, batch_size=min(8, len(X_train)), validation_data=(X_test, y_test), verbose=1)

# Avalia e salva
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"Treino FNN concluído! Loss: {loss:.2f}, Acurácia no teste: {accuracy:.2f}")

model.save('models/model_fnn.h5')
print("Modelo salvo em models/model_fnn.h5")