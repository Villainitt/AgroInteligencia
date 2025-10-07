import os
from PIL import Image, ImageDraw
import random

def generate_leaf_image(width=128, height=128, class_name='saudavel'):
    img = Image.new('RGB', (width, height), color='lightgreen')  # Fundo verde claro
    draw = ImageDraw.Draw(img)
    
    # Desenha folha básica (oval verde)
    leaf_color = 'darkgreen' if class_name == 'saudavel' else 'green'
    draw.ellipse([20, 20, 100, 100], fill=leaf_color, outline='black', width=2)
    
    if class_name == 'doente':
        # Simula manchas/doenças (círculos marrons/amarelos aleatórios)
        for _ in range(random.randint(3, 6)):  # 3-6 manchas
            x, y = random.randint(30, 90), random.randint(30, 90)
            color = random.choice(['brown', 'yellow', 'black'])
            size = random.randint(5, 15)
            draw.ellipse([x-size//2, y-size//2, x+size//2, y+size//2], fill=color)
    
    # Salva como JPG com timestamp
    filename = f"{class_name}_{random.randint(1, 1000)}.jpg"
    path = os.path.join('uploads', class_name, filename)
    img.save(path)
    return path

# Gera 25 por classe (total 50 > 40 do PDF)
os.makedirs('uploads/saudavel', exist_ok=True)
os.makedirs('uploads/doente', exist_ok=True)

for i in range(25):
    generate_leaf_image(class_name='saudavel')
    generate_leaf_image(class_name='doente')

print("Pastas uploads/ populadas com 25 imagens por classe (total 50)! Verifique as pastas.")