import os
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing.image import img_to_array, ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split

def load_data():
    X, y = [], []
    classes = [('saudavel', 0), ('doente', 1)]
    img_size = (128, 128)
    for class_name, idx in classes:
        path = f'uploads/{class_name}'
        if not os.path.exists(path):
            print(f"Erro: Pasta {path} não encontrada! Adicione fotos reais.")
            return np.array([]), np.array(y)
        for fname in os.listdir(path):
            if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
                img_path = os.path.join(path, fname)
                img = Image.open(img_path).convert('RGB').resize(img_size)
                X.append(img_to_array(img) / 255.0)
                y.append(idx)
    return np.array(X), np.array(y)

X, y = load_data()
if len(X) == 0:
    print("Sem imagens! Popule uploads/saudavel e uploads/doente com 20+ JPGs cada.")
    exit()

print(f"Dataset carregado: {len(X)} imagens, classes balanceadas? {np.bincount(y)}")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Treino: {X_train.shape}, Teste: {X_test.shape}")

# Augmentation pra mais dados (simula variações reais de fotos)
datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    zoom_range=0.2,
    fill_mode='nearest'
)
datagen.fit(X_train)

# Modelo CNN melhorado (camada extra + Dropout)
model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(128, 128, 3)),
    MaxPooling2D(2,2),
    Conv2D(64, (3,3), activation='relu'),  # Extra pra features
    MaxPooling2D(2,2),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Flatten(),
    Dense(64, activation='relu'),
    Dropout(0.5),  # Evita overfit
    Dense(1, activation='sigmoid')
])
model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])

# Early stopping (para se não melhorar)
early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

# Treina com augmentation
history = model.fit(
    datagen.flow(X_train, y_train, batch_size=4),
    steps_per_epoch=len(X_train) // 4,
    epochs=30,
    validation_data=(X_test, y_test),
    callbacks=[early_stop],
    verbose=1
)

# Print history pra ver progresso
print("History de accuracy:")
for epoch in range(len(history.history['accuracy'])):
    print(f"Epoch {epoch+1}: Train Acc {history.history['accuracy'][epoch]:.2f}, Val Acc {history.history['val_accuracy'][epoch]:.2f}")

# Avalia e salva
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"Treino CNN concluído! Loss: {loss:.2f}, Acurácia no teste: {accuracy:.2f}")

os.makedirs('models', exist_ok=True)
model.save('models/model_cnn.h5')
print("Modelo salvo em models/model_cnn.h5")