import os
import shutil
from pathlib import Path

# Seu path exato do download
dataset_path = Path(r'C:\Users\gicas\.cache\kagglehub\datasets\abdallahalidev\plantvillage-dataset\versions\3')

# Lista estrutura pra debug
print('Estrutura do PlantVillage:')
for p in dataset_path.glob('*'):
    print(p)
plantvillage_folder = dataset_path / 'plantvillage dataset'
print('\nContents of plantvillage dataset:', os.listdir(plantvillage_folder))
color_path = plantvillage_folder / 'color'
print('\nSubpastas em color/ (primeiras 10):', os.listdir(color_path)[:10])

# Integra 20 saudáveis (de pastas *___healthy)
uploads_saudavel = Path('uploads/saudavel')
uploads_doente = Path('uploads/doente')
uploads_saudavel.mkdir(parents=True, exist_ok=True)
uploads_doente.mkdir(parents=True, exist_ok=True)

saudavel_paths = []
healthy_folders = [f for f in os.listdir(color_path) if 'healthy' in f.lower()]
print(f'\nPastas healthy encontradas: {len(healthy_folders)} (primeiras 5): {healthy_folders[:5]}')
for folder_name in healthy_folders[:4]:  # 4 culturas pra variedade
    folder = color_path / folder_name
    imgs = list(folder.glob('*.jpg'))
    saudavel_paths.extend(imgs[:5])  # 5 por pasta pra 20 total
    print(f'  - {folder_name}: {len(imgs)} imgs, copiando 5')

for i, img_path in enumerate(saudavel_paths[:20]):
    dest = uploads_saudavel / f'folha_saudavel_{i+1}.jpg'
    shutil.copy2(img_path, dest)

# 20 doentes (de pastas *___* sem healthy)
doente_paths = []
diseased_folders = [f for f in os.listdir(color_path) if 'healthy' not in f.lower()]
print(f'\nPastas diseased encontradas: {len(diseased_folders)} (primeiras 5): {diseased_folders[:5]}')
for folder_name in diseased_folders[:4]:  # 4 doenças
    folder = color_path / folder_name
    imgs = list(folder.glob('*.jpg'))
    doente_paths.extend(imgs[:5])
    print(f'  - {folder_name}: {len(imgs)} imgs, copiando 5')

for i, img_path in enumerate(doente_paths[:20]):
    dest = uploads_doente / f'folha_doente_{i+1}.jpg'
    shutil.copy2(img_path, dest)

print(f'\nIntegrado: {len(list(uploads_saudavel.glob("*.jpg")))} saudáveis, {len(list(uploads_doente.glob("*.jpg")))} doentes em uploads/.')
print('Verifique: dir uploads\\saudavel')
print('Agora rode python train_scripts/train_cnn.py!')