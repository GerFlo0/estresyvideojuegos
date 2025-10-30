from pathlib import Path
import pandas as pd
import numpy as np
measurements_file = 'csvs\\individual_measurements'
df = pd.read_csv(Path(measurements_file) / "U-V19-M.csv") #se carga el csv correspondiente al video
frame_interval_seconds = df['segs_sig_med'].to_numpy() #se extrae el arreglo de intervalos en segundos

print(frame_interval_seconds)
print(type(frame_interval_seconds[2]))