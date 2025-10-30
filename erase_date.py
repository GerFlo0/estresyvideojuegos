import pandas as pd

archivo = "mediciones excel.xlsx"
hoja = "csv_unido"
columna = "start_time"

df = pd.read_excel(archivo, sheet_name=hoja)

df[columna] = pd.to_datetime(df[columna], errors="coerce")

df[columna] = df[columna].dt.time

df.to_excel("tus_datos_sin_fecha.xlsx", index=False)

print("Columna procesada y guardada en 'tus_datos_sin_fecha.xlsx'")
