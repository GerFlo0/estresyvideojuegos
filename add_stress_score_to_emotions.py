import pandas as pd
from pathlib import Path

# === CONFIGURACIÓN ===
carpeta_a = Path("csvs/emotions/individual/residents")  # Carpeta con los CSV base
carpeta_b = Path("csvs/measurements/individual_measurements")  # Carpeta con los CSV que contienen la columna a agregar
columna_b = "score"  # Nombre de la columna en B que quieres agregar
nombre_columna_en_a = "score"  # Nombre que tendrá en el CSV combinado
columna_referencia = "emocion_dominante"  # Columna delante de la cual se insertará
carpeta_salida = Path("csvs/emotions/individual/residents_w_score")  # Carpeta de salida
carpeta_salida.mkdir(parents=True, exist_ok=True)

# === PROCESAMIENTO ===
for archivo_a in carpeta_a.glob("*.csv"):
    nombre_archivo = archivo_a.name
    archivo_b = carpeta_b / nombre_archivo

    if not archivo_b.exists():
        print(f"⚠️ No se encontró el archivo correspondiente en B: {nombre_archivo}")
        continue

    # Leer ambos CSV
    df_a = pd.read_csv(archivo_a)
    df_b = pd.read_csv(archivo_b)

    # Verificar longitud
    if len(df_a) != len(df_b):
        min_filas = min(len(df_a), len(df_b))
        df_a = df_a.iloc[:min_filas].copy()
        df_b = df_b.iloc[:min_filas].copy()

    # Insertar columnas en el orden especificado
    col_index = df_a.columns.get_loc(columna_referencia)

    # Insertar "score" primero (inmediatamente antes de la referencia)
    df_a.insert(col_index, "score", df_b["score"].values)

    # Insertar "id" y "game" antes de "score"
    df_a.insert(col_index, "id", df_b["id"].values)
    df_a.insert(col_index, "game", df_b["game"].values)

    # Guardar resultado
    salida = carpeta_salida / nombre_archivo
    df_a.to_csv(salida, index=False)
    print(f"✅ {nombre_archivo} combinado con columnas 'game', 'id' y 'score'")