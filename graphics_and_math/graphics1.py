import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar datos
df = pd.read_csv("csvs/csv_unificado.csv")

# Estilo visual
sns.set(style="whitegrid")
palette = sns.color_palette("Set2")
emociones = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]

# 1. Conteo total de emociones dominantes
plt.figure(figsize=(8, 5))
ax = sns.countplot(data=df, x="emocion_dominante", order=df["emocion_dominante"].value_counts().index, palette=palette)
plt.title("Conteo total de emociones dominantes")
plt.xlabel("Emoción")
plt.ylabel("Cantidad de imágenes")
for p in ax.patches:
    height = p.get_height()
    ax.annotate(f"{height}", (p.get_x() + p.get_width() / 2, height), ha='center', va='bottom')
plt.tight_layout()
plt.show()

# 2. Porcentaje relativo de cada emoción (gráfico de pastel)
conteo = df["emocion_dominante"].value_counts()
plt.figure(figsize=(6, 6))
plt.pie(conteo, labels=conteo.index, autopct='%1.1f%%', colors=palette)
plt.title("Distribución porcentual de emociones dominantes")
plt.tight_layout()
plt.show()

# 3. Conteo de emociones por juego
plt.figure(figsize=(10, 6))
ax = sns.countplot(data=df, x="emocion_dominante", hue="juego", palette="Set1")
plt.title("Conteo de emociones dominantes por juego")
plt.xlabel("Emoción")
plt.ylabel("Cantidad")
plt.legend(title="Juego")
for container in ax.containers:
    ax.bar_label(container, label_type="edge", fontsize=8)
plt.tight_layout()
plt.show()

# 4. Conteo de emociones por sujeto
conteo_sujeto = df.groupby(["id", "emocion_dominante"]).size().unstack().fillna(0)
plt.figure(figsize=(12, 6))
conteo_sujeto.plot(kind="bar", stacked=True, colormap="Set3")
plt.title("Emociones dominantes por sujeto")
plt.xlabel("Sujeto")
plt.ylabel("Cantidad de imágenes")
plt.legend(title="Emoción", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# 5. Promedio de cada emoción (probabilidad) en todo el dataset
promedios = df[emociones].mean().sort_values(ascending=False)
plt.figure(figsize=(8, 5))
ax = sns.barplot(x=promedios.values, y=promedios.index, palette="Blues_r")
plt.title("Promedio de probabilidad por emoción (todas las imágenes)")
plt.xlabel("Promedio")
for i, v in enumerate(promedios.values):
    ax.text(v + 0.002, i, f"{v:.2f}", va="center")
plt.tight_layout()
plt.show()

# 6. Comparación de emociones promedio por juego
promedios_juego = df.groupby("juego")[emociones].mean()
ax = promedios_juego.T.plot(kind='bar', figsize=(10, 6), colormap='Set3')
plt.title("Promedio de emociones por juego")
plt.xlabel("Emoción")
plt.ylabel("Probabilidad promedio")
plt.legend(title="Juego")
for container in ax.containers:
    ax.bar_label(container, fmt="%.2f", fontsize=7)
plt.tight_layout()
plt.show()

# 7. Evolución emocional a lo largo del tiempo (línea temporal)
df_sub = df[(df["id"] == "U10") & (df["juego"] == "L")]
plt.figure(figsize=(12, 6))
for emo in emociones:
    plt.plot(df_sub["timestamp_segundos"], df_sub[emo], label=emo)
plt.title("Evolución de emociones - Sujeto U10 (Juego L)")
plt.xlabel("Tiempo (s)")
plt.ylabel("Probabilidad")
plt.legend()
plt.tight_layout()
plt.show()

# 8. Gráfico de calor de emociones promedio por sujeto
promedios_sujeto = df.groupby("id")[emociones].mean()
plt.figure(figsize=(12, 6))
sns.heatmap(promedios_sujeto, annot=True, cmap="YlGnBu", fmt=".2f")
plt.title("Promedio de emociones por sujeto")
plt.xlabel("Emoción")
plt.ylabel("Sujeto")
plt.tight_layout()
plt.show()

# 9. Conteo de emociones dominantes por sujeto (stacked bar con total)
conteo_dom = df.groupby(["id", "emocion_dominante"]).size().unstack(fill_value=0)
ax = conteo_dom.plot(kind="bar", stacked=True, figsize=(12, 6), colormap="tab20c")
plt.title("Conteo de emociones dominantes por sujeto")
plt.xlabel("Sujeto")
plt.ylabel("Cantidad")
plt.legend(title="Emoción", bbox_to_anchor=(1.05, 1), loc='upper left')
for idx, total in enumerate(conteo_dom.sum(axis=1)):
    ax.text(idx, total + 5, str(int(total)), ha='center')
plt.tight_layout()
plt.show()
