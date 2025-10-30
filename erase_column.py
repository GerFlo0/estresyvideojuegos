import pandas as pd

# === CONFIGURACIÓN ===
ruta_csv = "csvs/emotions/csv_unido.csv"         # Ruta del archivo original
columna_a_eliminar = "timestamp_segundos"   # Nombre de la columna que quieres eliminar

# === PROCESAMIENTO ===
df = pd.read_csv(ruta_csv)                  # Leer CSV
df = df.drop(columns=[columna_a_eliminar])  # Eliminar columna
df.to_csv(ruta_csv, index=False)         # Guardar sin índice

print(f"Columna '{columna_a_eliminar}' eliminada")
