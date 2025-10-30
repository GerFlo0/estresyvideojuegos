import cv2
from pathlib import Path
import pandas as pd
import numpy as np
from tqdm import tqdm

input_folder = 'videos/por_analizar'
output_frames_folder = 'frames/por_analizar'
measurements_file = 'csvs/measurements/individual_measurements'

x1, y1 = 0, 0
x2, y2 = 270, 200

# Diccionario de tiempos muertos (en segundos)
tiempos_muertos = {
    "P-5-L": 60.0,
    "P-5-M": 11.0,
    "P-6-L": 45.0,
    "P-6-M": 30.0,
    "U-2-L": 35.0,
    "U-2-M": 12.0,
    "U-5-L": 47.0,
    "U-5-M": 53.0,
    "U-6-L": 160.0,
    "U-6-M": 5.0,
    "U-7-L": 90.0,
    "U-7-M": 31.0,
    "U-8-L": 66.0,
    "U-8-M": 43.0,
    "U-10-L": 64.0,
    "U-10-M": 16.0,
    "U-11-L": 60.0,
    "U-11-M": 334.0,
    "U-13-L": 70.0,
    "U-13-M": 15.0,
    "U-16-L": 52.0,
    "U-16-M": 27.0,
    "U-17-L": 90.0,
    "U-17-M": 19.0,
    "U-20-L": 50.0,
    "U-20-M": 4.0
    # agrega los demás videos aquí
}

def procesar_video(video_path: Path):
    print(f"Procesando: {video_path.name}")
    
    video_name = video_path.stem
    df = pd.read_csv(Path(measurements_file) / f"{video_name}.csv")
    frame_intervals = df['segs_sig_med'].to_numpy()

    frames_output_dir = Path(output_frames_folder) / video_name
    frames_output_dir.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(str(video_path))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Si el video está en el diccionario, saltamos ese tiempo inicial
    tiempo_actual = tiempos_muertos.get(video_name, 0.0)
    intervalo_idx = 0
    image_counter = 1

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duracion_video = total_frames / fps

    with tqdm(total=len(frame_intervals), desc=f"Frames {video_name}", unit="frame") as pbar:
        while intervalo_idx < len(frame_intervals):
            if frame_intervals[intervalo_idx] == -1:
                break

            # Si el tiempo solicitado supera la duración del video, se detiene
            if tiempo_actual > duracion_video:
                print(f"Tiempo {tiempo_actual:.2f}s fuera del rango de {video_name}, deteniendo.")
                break

            frame_a_capturar = int(tiempo_actual * fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_a_capturar)
            ret, frame = cap.read()
            if not ret:
                break

            webcam_frame = frame[y1:y2, x1:x2]

            frame_file = frames_output_dir / f"{video_name}_{image_counter:03d}.jpg"
            cv2.imwrite(str(frame_file), webcam_frame)

            # Avanza tiempo y contador
            tiempo_actual += frame_intervals[intervalo_idx]
            intervalo_idx += 1
            image_counter += 1
            pbar.update(1)

    cap.release()
    print(f"Frames extraídos para {video_name}.")

input_dir = Path(input_folder)
for video_file in input_dir.glob("*.mp4"):
    procesar_video(video_file)

print("Todos los videos han sido procesados.")
