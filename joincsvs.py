import pandas as pd
import os
from tqdm import tqdm

# Carpeta donde están los CSVs originales
ruta_csvs = "csvs"

# Lista de archivos .csv en esa carpeta
archivos = [f for f in os.listdir(ruta_csvs) if f.endswith(".csv")]

# Lista para guardar cada DataFrame
dfs = []

for archivo in tqdm(archivos, desc="Uniendo archivos CSV"):
    ruta = os.path.join(ruta_csvs, archivo)
    df = pd.read_csv(ruta)

    # Extraer ID desde la columna "archivo"
    if "archivo" in df.columns:
        df.insert(0, "id", df["archivo"].apply(lambda x: x.split("_")[0]))
        dfs.append(df)
    else:
        print(f"No se encontró la columna 'archivo' en {archivo}. Saltando...")

# Unir todos los DataFrames
df_final = pd.concat(dfs, ignore_index=True)

# Guardar el CSV unificado
df_final.to_csv("csvs/CSVs_unidos.csv", index=False)
print("CSV unificado guardado como 'CSVs_unidos.csv'")
