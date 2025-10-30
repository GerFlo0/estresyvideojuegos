import os
import cv2
import pandas as pd
from deepface import DeepFace
from tqdm import tqdm

# 📁 Rutas
root_input_folder = "frames\\por_analizar"
output_folder = "csvs\\mejorado"
fps = 1

os.makedirs(output_folder, exist_ok=True)

# 🧼 Función de preprocesamiento de imagen
def preprocess_image(path):
    img = cv2.imread(path)
    if img is None:
        return None
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_eq = cv2.equalizeHist(gray)  # mejora contraste
    img_final = cv2.cvtColor(img_eq, cv2.COLOR_GRAY2BGR)
    return img_final

# Recorrer todas las subcarpetas
for subfolder in os.listdir(root_input_folder):
    input_folder = os.path.join(root_input_folder, subfolder)
    if not os.path.isdir(input_folder):
        continue  # Ignorar archivos que no son carpetas

    csv_filename = f"{subfolder}.csv"
    image_files = sorted([f for f in os.listdir(input_folder) if f.lower().endswith('.jpg')])
    results = []

    print(f"\nAnalizando carpeta: {subfolder} ({len(image_files)} imágenes)")

    for i, filename in tqdm(enumerate(image_files), total=len(image_files), desc=f"{subfolder}"):
        img_path = os.path.join(input_folder, filename)

        try:
            # 🧼 Preprocesamiento de imagen
            img = preprocess_image(img_path)
            if img is None:
                print(f"[ADVERTENCIA] Imagen no válida: {filename}")
                continue

            # 🧠 Análisis de emociones con mejor detector
            analysis = DeepFace.analyze(
                img_path=img,
                actions=['emotion'],
                enforce_detection=False,
                detector_backend='retinaface'  # ✅ mejora en detección
            )

            emotion_data = analysis[0]['emotion']
            dominant = analysis[0]['dominant_emotion']
            timestamp_sec = round(i / fps, 2)

            row = {
                "archivo": filename,
                "timestamp_segundos": timestamp_sec,
                "emocion_dominante": dominant
            }
            row.update(emotion_data)
            results.append(row)

        except Exception as e:
            print(f"[ERROR] {filename}: {e}")

    # Guardar CSV por subcarpeta
    output_path = os.path.join(output_folder, csv_filename)
    df = pd.DataFrame(results)
    df.to_csv(output_path, index=False)

    print(f"✅ CSV guardado: {output_path}")
