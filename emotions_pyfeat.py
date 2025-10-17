import os
import cv2
import pandas as pd
from tqdm import tqdm
from feat import Detector  # Py-Feat

# 📁 Carpetas
root_input_folder = "frames/por_analizar"
output_folder = "csvs_pyfeat"
fps = 1  # 1 frame por segundo (ajusta si es distinto)

os.makedirs(output_folder, exist_ok=True)

# Inicializar el detector (modelo por defecto)
# Emociones: angry, disgust, fear, happy, sad, surprise, neutral
detector = Detector(
    face_model="retinaface",
    landmark_model="mobilefacenet",
    au_model="jaanet",
    emotion_model="resmasknet"
)

# Recorrer subcarpetas
for subfolder in os.listdir(root_input_folder):
    input_folder = os.path.join(root_input_folder, subfolder)
    if not os.path.isdir(input_folder):
        continue

    csv_filename = f"{subfolder}_pyfeat.csv"
    image_files = sorted([f for f in os.listdir(input_folder) if f.lower().endswith('.jpg')])
    results = []

    print(f"\nAnalizando carpeta: {subfolder} ({len(image_files)} imágenes)")

    for i, filename in tqdm(enumerate(image_files), total=len(image_files), desc=subfolder):
        img_path = os.path.join(input_folder, filename)

        try:
            img = cv2.imread(img_path)
            if img is None:
                raise ValueError("No se pudo leer la imagen")

            # Detectar emociones
            prediction = detector.detect_image(img)

            # Si hay detección
            if len(prediction) > 0:
                emotions = prediction.emotions.iloc[0].to_dict()
                dominant_emotion = max(emotions, key=emotions.get)
                timestamp_sec = round(i / fps, 2)

                row = {
                    "archivo": filename,
                    "timestamp_segundos": timestamp_sec,
                    "emocion_dominante": dominant_emotion
                }
                row.update(emotions)
                results.append(row)
            else:
                timestamp_sec = round(i / fps, 2)
                results.append({
                    "archivo": filename,
                    "timestamp_segundos": timestamp_sec,
                    "emocion_dominante": "error",
                    "angry": -1,
                    "disgust": -1,
                    "fear": -1,
                    "happy": -1,
                    "sad": -1,
                    "surprise": -1,
                    "neutral": -1
                })

        except Exception as e:
            print(f"[ERROR] {filename}: {e}")
            timestamp_sec = round(i / fps, 2)
            results.append({
                "archivo": filename,
                "timestamp_segundos": timestamp_sec,
                "emocion_dominante": "error",
                "angry": -1,
                "disgust": -1,
                "fear": -1,
                "happy": -1,
                "sad": -1,
                "surprise": -1,
                "neutral": -1
            })

    # Guardar CSV por subcarpeta
    output_path = os.path.join(output_folder, csv_filename)
    df = pd.DataFrame(results)
    df.to_csv(output_path, index=False)

    print(f"✅ CSV guardado: {output_path}")
