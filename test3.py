import pandas as pd
import os

# Carpeta donde están los archivos originales
carpeta_entrada = "origen"
carpeta_salida = "fin"
os.makedirs(carpeta_salida, exist_ok=True)

# Procesar todos los archivos en la carpeta
for archivo in os.listdir(carpeta_entrada):
    if archivo.endswith(".xlsx"):
        ruta = os.path.join(carpeta_entrada, archivo)
        
        # Leer el archivo Excel
        df = pd.read_excel(ruta)

        # Aseguramos que existen las columnas necesarias
        if "id" not in df.columns or "game" not in df.columns:
            print(f"El archivo {archivo} no tiene columnas 'id' y 'game'. Saltando...")
            continue

        # Agrupar por voluntario y juego
        for (voluntario, juego), datos in df.groupby(["id", "game"]):
            # Crear nombre de archivo: ejemplo "P-V1_Mine.xlsx"
            nombre_archivo = f"{voluntario}{juego}.xlsx".replace(" ", "")
            ruta_salida = os.path.join(carpeta_salida, nombre_archivo)

            # Guardar los datos completos (todas las columnas)
            datos.to_excel(ruta_salida, index=False)
            print(f"Archivo creado: {ruta_salida}")