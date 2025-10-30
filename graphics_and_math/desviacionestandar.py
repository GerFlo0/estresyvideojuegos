import pandas as pd
import numpy as np

df = pd.read_csv("csvs\\csv_unificado.csv")

emotion_map = {
    'angry': 0,
    'disgust': 1,
    'fear': 2,
    'happy': 3,
    'sad': 4,
    'surprise': 5,
    'neutral': 6
}
df['emocion_numerica'] = df['emocion_dominante'].map(emotion_map)

# Verificar si hay valores no mapeados
if df['emocion_numerica'].isnull().any():
    print("Advertencia: hay emociones no reconocidas. Revisa los valores únicos:")
    print(df['emocion_dominante'].unique())

# Calcular desviación estándar por participante y juego
desviaciones = df.groupby(['id', 'juego'])['emocion_numerica'].std().reset_index()
desviaciones.rename(columns={'emocion_numerica': 'std_emocion'}, inplace=True)

# Calcular promedio de desviaciones por juego
promedios = desviaciones.groupby('juego')['std_emocion'].agg(['mean', 'std', 'count']).reset_index()

# Mostrar resultados
print("Desviación estándar promedio por juego:")
print(promedios)

# Guardar resultados en archivos CSV
promedios.to_csv("csvs\\resumen_desviaciones_por_juego.csv", index=False)
desviaciones.to_csv("desviaciones_por_participante.csv", index=False)
