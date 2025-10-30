import pandas as pd

# === CONFIGURACIÓN ===
archivo_entrada = "csvs/emotions/csv_unido.csv"          # Ruta del archivo CSV original
archivo_salida = "csvs/emotions/csv_weka.csv"  # Ruta del archivo CSV modificado
columna_a_eliminar = "archivo"   # Nombre de la columna que quieres eliminar

# Diccionarios de reemplazo para columnas de texto
diccionario_game = {
    "LOL": 0,
    "Mine": 1
}

diccionario_emocion_dominante = {
    "angry": 0,
    "disgust": 1,
    "fear": 2,
    "happy": 3,
    "sad": 4,
    "surprise": 5,
    "neutral": 6
}

# Nombres de las columnas que quieres transformar
columna1 = "game"
columna2 = "emocion_dominante"

# === PROCESAMIENTO ===
# Cargar el CSV
df = pd.read_csv(archivo_entrada)

# Eliminar la columna no deseada
if columna_a_eliminar in df.columns:
    df.drop(columns=[columna_a_eliminar], inplace=True)

# Reemplazar valores de texto por números
#df[columna1] = df[columna1].map(diccionario_game).fillna(-1)
#df[columna2] = df[columna2].map(diccionario_emocion_dominante).fillna(-1)

# Guardar el nuevo CSV
df.to_csv(archivo_salida, index=False)
print(f"Archivo modificado guardado como: {archivo_salida}")
