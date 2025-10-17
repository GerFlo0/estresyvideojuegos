import os
import pandas as pd

# Carpeta donde están los CSV
input_folder = "csvs/emotions/individual/residents_w_score"   # Cambia esto si usas otra carpeta
output_file = "csvs/emotions/csv_unido.csv"

# Lista para almacenar todos los DataFrames
dataframes = []

# Recorrer todos los archivos en la carpeta
for filename in os.listdir(input_folder):
    if filename.lower().endswith(".csv"):
        file_path = os.path.join(input_folder, filename)
        df = pd.read_csv(file_path)
        dataframes.append(df)
        print(f"Archivo agregado: {filename}")

# Unir todos los DataFrames
df_final = pd.concat(dataframes, ignore_index=True)

# Guardar archivo final
df_final.to_csv(output_file, index=False)
print(f"Total de filas combinadas: {len(df_final)}")
