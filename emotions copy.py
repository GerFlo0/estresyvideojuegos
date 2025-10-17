import os
import cv2
import pandas as pd
from deepface import DeepFace
from tqdm import tqdm

root_input_folder = "frames/por_analizar"
output_folder = "csvs"
fps = 1

os.makedirs(output_folder, exist_ok=True)

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
        timestamp_sec = round(i / fps, 2)

        try:
            img = cv2.imread(img_path)
            analysis = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)

            emotion_data = analysis[0]['emotion']
            dominant = analysis[0]['dominant_emotion']

            row = {
                "archivo": filename,
                "timestamp_segundos": timestamp_sec,
                "emocion_dominante": dominant
            }
            row.update(emotion_data)

        except Exception as e:
            print(f"[ERROR] {filename}: {e}")
            # Genera una fila "dummy" con -1 y error
            row = {
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
            }

        results.append(row)

    # Guardar CSV por subcarpeta
    output_path = os.path.join(output_folder, csv_filename)
    df = pd.DataFrame(results)

    # Si el CSV tiene columnas vacías (porque nunca hubo resultados correctos), las rellena en orden
    columnas = ["archivo", "timestamp_segundos", "emocion_dominante",
                "angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]
    for col in columnas:
        if col not in df.columns:
            df[col] = "error" if col == "emocion_dominante" else -1
    df = df[columnas]

    df.to_csv(output_path, index=False)
    print(f"CSV guardado: {output_path}")
