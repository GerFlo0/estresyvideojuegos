import cv2
import os
from pathlib import Path
from tqdm import tqdm

input_folder = 'videos\\por_analizar'
output_video_folder = 'videos\\webcam'
output_frames_folder = 'frames\\por_analizar'

# Definición de las coordenadas del recorte
x1, y1 = 0, 0
x2, y2 = 260, 220

frame_interval_seconds = 3

def procesar_video(video_path: Path):
    print(f"Procesando: {video_path.name}")

    video_name = video_path.stem
    frames_output_dir = Path(output_frames_folder) / video_name
    frames_output_dir.mkdir(parents=True, exist_ok=True)
    Path(output_video_folder).mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(str(video_path))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps

    width, height = x2 - x1, y2 - y1
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_video_path = Path(output_video_folder) / f"{video_name}_webcam.mp4"
    out = cv2.VideoWriter(str(out_video_path), fourcc, fps, (width, height))

    frame_idx = 0
    next_capture_frame = int(fps * frame_interval_seconds)

    # Barra de progreso
    with tqdm(total=frame_count, desc=video_name, unit="frame") as pbar:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            webcam_frame = frame[y1:y2, x1:x2]

            if frame_idx >= next_capture_frame:
                timestamp = int(frame_idx / fps)
                frame_file = frames_output_dir / f"{video_name}_frame_{timestamp:04d}.jpg"
                cv2.imwrite(str(frame_file), webcam_frame)
                next_capture_frame += int(fps * frame_interval_seconds)

            out.write(webcam_frame)

            frame_idx += 1
            pbar.update(1)

    cap.release()
    out.release()
    print(f"Video recortado guardado en: {out_video_path.name}")

input_dir = Path(input_folder)
for video_file in input_dir.glob("*.mp4"):
    procesar_video(video_file)

print("Todos los videos han sido procesados.")
