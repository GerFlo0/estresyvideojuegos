import pandas as pd
from pathlib import Path

input_csv = "csvs\measurements\mediciones_sin_fecha.csv"   # ruta del csv de entrada
output_folder = "csvs\measurements\individual_measurements"     # carpeta donde se guardarán los sub-archivos

# Leer el CSV original
df = pd.read_csv(input_csv)

sub_df = []  # acumulador de filas para el sub-CSV actual
for idx, row in df.iterrows():
    sub_df.append(row)  # agregamos la fila actual siempre

    if row["segs_sig_med"] == -1:
        # Obtener nombre de archivo con id y primera letra de game
        id_val = row["id"]
        game_val = str(row["game"])  # asegurarnos que sea string
        first_letter_game = game_val[0]

        output_path = Path(output_folder) / f"{id_val}-{first_letter_game}.csv"
        pd.DataFrame(sub_df).to_csv(output_path, index=False)
        print(f"Sub-CSV guardado: {output_path.name}")
        sub_df = []  # reiniciar acumulador para el siguiente bloque

print("Proceso completado.")
