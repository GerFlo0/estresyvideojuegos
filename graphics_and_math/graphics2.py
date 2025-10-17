import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("csvs/csv_unificado.csv")
emociones = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]

sns.set(style="whitegrid")
palette = sns.color_palette("Set2")

#1. Cantidad total de imágenes por juego
plt.figure(figsize=(6, 4))
ax = sns.countplot(data=df, x="juego", palette="pastel")
plt.title("Cantidad total de imágenes por juego")
for container in ax.containers:
    ax.bar_label(container)
plt.tight_layout()
plt.show()

#2. Distribución de emociones dominantes por juego
plt.figure(figsize=(10, 6))
ax = sns.countplot(data=df, x="emocion_dominante", hue="juego", palette="Set1")
plt.title("Distribución de emociones dominantes por juego")
plt.xlabel("Emoción dominante")
plt.ylabel("Cantidad")
for container in ax.containers:
    ax.bar_label(container, fontsize=8)
plt.legend(title="Juego")
plt.tight_layout()
plt.show()

#3. Promedio de cada emoción (probabilidad) por juego
promedios_juego = df.groupby("juego")[emociones].mean().T  # transpuesto para mejor visualización

plt.figure(figsize=(10, 6))
ax = promedios_juego.plot(kind="bar", figsize=(10, 6), colormap="Set2")
plt.title("Promedio de emociones por juego")
plt.ylabel("Probabilidad promedio")
plt.xlabel("Emoción")
plt.legend(title="Juego")
for container in ax.containers:
    ax.bar_label(container, fmt="%.2f")
plt.tight_layout()
plt.show()

#4. Gráfico de calor (heatmap) de emociones promedio por juego
plt.figure(figsize=(8, 4))
sns.heatmap(promedios_juego, annot=True, cmap="YlGnBu", fmt=".2f")
plt.title("Heatmap de emociones promedio por juego")
plt.ylabel("Emoción")
plt.xlabel("Juego")
plt.tight_layout()
plt.show()

#5. Evolución temporal promedio de emociones por juego 
df["tiempo_grupo"] = (df["timestamp_segundos"] // 5) * 5

df_tiempo = df.groupby(["juego", "tiempo_grupo"])[emociones].mean().reset_index()

plt.figure(figsize=(12, 6))
for juego in df["juego"].unique():
    sub = df_tiempo[df_tiempo["juego"] == juego]
    plt.plot(sub["tiempo_grupo"], sub["happy"], label=f"Juego {juego}")

plt.title("Evolución temporal de felicidad por juego (promedio cada 5s)")
plt.xlabel("Tiempo (segundos)")
plt.ylabel("Probabilidad de 'happy'")
plt.legend()
plt.tight_layout()
plt.show()
