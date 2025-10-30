import pandas as pd
import os

# Carpeta donde están los CSVs originales
ruta_csvs = "csvs"  # Cámbiala si es necesario

# Lista de archivos .csv en esa carpeta
archivos = [f for f in os.listdir(ruta_csvs) if f.endswith(".csv")]

# Lista para almacenar DataFrames
dfs = []

# Proceso con barra de progreso
for archivo in archivos:
    ruta = os.path.join(ruta_csvs, archivo)
    df = pd.read_csv(ruta)

    if "archivo" in df.columns:
        def extraer_id_y_juego(nombre):
            base = str(nombre).split("_")[0]
            return base[:-1], base[-1]  # id = todo menos última letra, juego = última letra

        ids, juegos = zip(*df["archivo"].map(extraer_id_y_juego))

        df.insert(0, "juego", juegos)
        df.insert(0, "id", ids)

        dfs.append(df)
    else:
        print(f"[ERROR] El archivo '{archivo}' no contiene la columna 'archivo'. Saltando.")

# Unir todos los DataFrames
df_final = pd.concat(dfs, ignore_index=True)

# Guardar el CSV unificado
df_final.to_csv("csvs/csv_unificado.csv", index=False)
print("CSV unificado guardado como 'csv_unificado.csv'")
