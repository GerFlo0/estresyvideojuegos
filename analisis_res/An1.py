import inspect
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# === FUNCIONES ===
def mean_estress_per_game():
    df = cargar_datos()
    promedio_score = df.groupby("game")["score"].mean()
    print(promedio_score)

def emotions_score_correlation(): 
    df = cargar_datos() 
    correlaciones = df[["score", "angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]].corr() 
    print(correlaciones["score"].sort_values(ascending=False))

def emotions_score_correlation_by_game():
    df = cargar_datos()
    cols_emociones = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]
    
    juegos = df["game"].unique()  # obtener todos los juegos presentes
    
    for juego in juegos:
        df_juego = df[df["game"] == juego]
        correlaciones = df_juego[["score"] + cols_emociones].corr()
        print(f"\n=== Correlaciones para {juego} ===")
        print(correlaciones["score"].sort_values(ascending=False))

def time_evolution_of_score_and_emotions_LOL():
    df = cargar_datos()
    GAME="LOL"
    df_lol = df[df["game"] == GAME].copy()
    if df_lol.empty:
        raise SystemExit(f"No se encontraron filas para el juego '{GAME}'.")

    # Agrupar por voluntario (id)
    groups = list(df_lol.groupby("id"))
    if not groups:
        raise SystemExit("No hay sesiones agrupadas por 'id' para LOL.")

    # Elegir sesión de referencia: la que tenga más registros
    ref_id, ref_df = max(groups, key=lambda t: len(t[1]))
    ref_df = ref_df.reset_index(drop=True)

    # Construir eje X de referencia por índice
    ref_len = len(ref_df)
    ref_x = np.arange(ref_len, dtype=float)
    ref_scores_ref = ref_df["score"].to_numpy(dtype=float)

    # Preparar figura
    plt.figure(figsize=(12, 6))
    plt.title(f"Evolución temporal de score (todas las sesiones de {GAME})")
    plt.xlabel("Índice de medición (frame)")
    plt.ylabel("Stress score")

    # Acumular valores interpolados
    interp_matrix = []

    # Procesar las demás sesiones
    for sid, group_df in groups:
        g = group_df.reset_index(drop=True)
        y = g["score"].to_numpy(dtype=float)
        m = len(y)

        if m == 0:
            continue

        # Mapear índices de esta sesión a los de referencia
        mapped_x = np.linspace(ref_x[0], ref_x[-1], m)
        y_on_ref = np.interp(ref_x, mapped_x, y)

        interp_matrix.append(y_on_ref)

        # Ploteo individual (transparente)
        plt.plot(ref_x, y_on_ref, color="tab:blue", alpha=0.25, linewidth=0.8)

    # Convertir a matriz
    interp_matrix = np.vstack(interp_matrix)

    # Calcular promedio y desviación estándar
    mean_profile = np.mean(interp_matrix, axis=0)
    std_profile = np.std(interp_matrix, axis=0)

    # Plotear media y banda de ±1 std
    plt.plot(ref_x, mean_profile, color="red", linewidth=2, label="Media general")
    plt.fill_between(ref_x, mean_profile - std_profile, mean_profile + std_profile, color="red", alpha=0.15, label="±1 std")

    plt.legend()
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.show()

def time_evolution_of_score_and_emotions_MINE():
    df = cargar_datos()
    GAME="Mine"
    df_lol = df[df["game"] == GAME].copy()
    if df_lol.empty:
        raise SystemExit(f"No se encontraron filas para el juego '{GAME}'.")

    # Agrupar por voluntario (id)
    groups = list(df_lol.groupby("id"))
    if not groups:
        raise SystemExit("No hay sesiones agrupadas por 'id' para LOL.")

    # Elegir sesión de referencia: la que tenga más registros
    ref_id, ref_df = max(groups, key=lambda t: len(t[1]))
    ref_df = ref_df.reset_index(drop=True)

    # Construir eje X de referencia por índice
    ref_len = len(ref_df)
    ref_x = np.arange(ref_len, dtype=float)
    ref_scores_ref = ref_df["score"].to_numpy(dtype=float)

    # Preparar figura
    plt.figure(figsize=(12, 6))
    plt.title(f"Evolución temporal de score (todas las sesiones de {GAME})")
    plt.xlabel("Índice de medición (frame)")
    plt.ylabel("Stress score")

    # Acumular valores interpolados
    interp_matrix = []

    # Procesar las demás sesiones
    for sid, group_df in groups:
        g = group_df.reset_index(drop=True)
        y = g["score"].to_numpy(dtype=float)
        m = len(y)

        if m == 0:
            continue

        # Mapear índices de esta sesión a los de referencia
        mapped_x = np.linspace(ref_x[0], ref_x[-1], m)
        y_on_ref = np.interp(ref_x, mapped_x, y)

        interp_matrix.append(y_on_ref)

        # Ploteo individual (transparente)
        plt.plot(ref_x, y_on_ref, color="tab:blue", alpha=0.25, linewidth=0.8)

    # Convertir a matriz
    interp_matrix = np.vstack(interp_matrix)

    # Calcular promedio y desviación estándar
    mean_profile = np.mean(interp_matrix, axis=0)
    std_profile = np.std(interp_matrix, axis=0)

    # Plotear media y banda de ±1 std
    plt.plot(ref_x, mean_profile, color="red", linewidth=2, label="Media general")
    plt.fill_between(ref_x, mean_profile - std_profile, mean_profile + std_profile, color="red", alpha=0.15, label="±1 std")

    plt.legend()
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.show()

def time_evolution_of_score_and_emotions_LOL_2():
    df = cargar_datos()
    GAME = "LOL"
    df_lol = df[df["game"] == GAME].copy()
    if df_lol.empty:
        raise SystemExit(f"No se encontraron filas para el juego '{GAME}'.")

    # Agrupar por voluntario (id)
    groups = list(df_lol.groupby("id"))
    if not groups:
        raise SystemExit("No hay sesiones agrupadas por 'id' para LOL.")

    # Elegir sesión de referencia: la que tenga más registros
    ref_id, ref_df = max(groups, key=lambda t: len(t[1]))
    ref_df = ref_df.reset_index(drop=True)

    # Construir eje X de referencia por índice
    ref_len = len(ref_df)
    ref_x = np.arange(ref_len, dtype=float)
    ref_scores_ref = ref_df["score"].to_numpy(dtype=float)

    # Preparar figura
    plt.figure(figsize=(12, 6))
    plt.title(f"Evolución temporal de score (todas las sesiones de {GAME})")
    plt.xlabel("Índice de medición (frame)")
    plt.ylabel("Stress score")

    # Acumular valores interpolados
    interp_matrix = []

    # Procesar las demás sesiones
    for sid, group_df in groups:
        g = group_df.reset_index(drop=True)
        y = g["score"].to_numpy(dtype=float)
        m = len(y)

        if m == 0:
            continue

        # Mapear índices de esta sesión a los de referencia
        mapped_x = np.linspace(ref_x[0], ref_x[-1], m)
        y_on_ref = np.interp(ref_x, mapped_x, y)

        interp_matrix.append(y_on_ref)

        # Ploteo individual (transparente)
        plt.plot(ref_x, y_on_ref, color="tab:blue", alpha=0.25, linewidth=0.8)

    # Convertir a matriz
    interp_matrix = np.vstack(interp_matrix)

    # Calcular mediana y IQR
    median_profile = np.median(interp_matrix, axis=0)
    q1 = np.percentile(interp_matrix, 25, axis=0)
    q3 = np.percentile(interp_matrix, 75, axis=0)
    iqr = q3 - q1

    # Limitar banda inferior a 0
    lower_bound = np.maximum(median_profile - iqr, 0)
    upper_bound = median_profile + iqr

    # Plotear mediana y banda IQR
    plt.plot(ref_x, median_profile, color="red", linewidth=2, label="Mediana general")
    plt.fill_between(ref_x, lower_bound, upper_bound, color="red", alpha=0.15, label="Mediana ± IQR")

    plt.legend()
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.show()


def time_evolution_of_score_and_emotions_Mine_2():
    df = cargar_datos()
    GAME = "Mine"
    df_lol = df[df["game"] == GAME].copy()
    if df_lol.empty:
        raise SystemExit(f"No se encontraron filas para el juego '{GAME}'.")

    # Agrupar por voluntario (id)
    groups = list(df_lol.groupby("id"))
    if not groups:
        raise SystemExit("No hay sesiones agrupadas por 'id' para LOL.")

    # Elegir sesión de referencia: la que tenga más registros
    ref_id, ref_df = max(groups, key=lambda t: len(t[1]))
    ref_df = ref_df.reset_index(drop=True)

    # Construir eje X de referencia por índice
    ref_len = len(ref_df)
    ref_x = np.arange(ref_len, dtype=float)
    ref_scores_ref = ref_df["score"].to_numpy(dtype=float)

    # Preparar figura
    plt.figure(figsize=(12, 6))
    plt.title(f"Evolución temporal de score (todas las sesiones de {GAME})")
    plt.xlabel("Índice de medición (frame)")
    plt.ylabel("Stress score")

    # Acumular valores interpolados
    interp_matrix = []

    # Procesar las demás sesiones
    for sid, group_df in groups:
        g = group_df.reset_index(drop=True)
        y = g["score"].to_numpy(dtype=float)
        m = len(y)

        if m == 0:
            continue

        # Mapear índices de esta sesión a los de referencia
        mapped_x = np.linspace(ref_x[0], ref_x[-1], m)
        y_on_ref = np.interp(ref_x, mapped_x, y)

        interp_matrix.append(y_on_ref)

        # Ploteo individual (transparente)
        plt.plot(ref_x, y_on_ref, color="tab:blue", alpha=0.25, linewidth=0.8)

    # Convertir a matriz
    interp_matrix = np.vstack(interp_matrix)

    # Calcular mediana y IQR
    median_profile = np.median(interp_matrix, axis=0)
    q1 = np.percentile(interp_matrix, 25, axis=0)
    q3 = np.percentile(interp_matrix, 75, axis=0)
    iqr = q3 - q1

    # Limitar banda inferior a 0
    lower_bound = np.maximum(median_profile - iqr, 0)
    upper_bound = median_profile + iqr

    # Plotear mediana y banda IQR
    plt.plot(ref_x, median_profile, color="red", linewidth=2, label="Mediana general")
    plt.fill_between(ref_x, lower_bound, upper_bound, color="red", alpha=0.15, label="Mediana ± IQR")

    plt.legend()
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.show()


def emotional_profile_vs_stress_per_volunteer():
    df = cargar_datos()
    cols_emociones = ["score", "angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]
    resumen = df.groupby(["id", "game"])[cols_emociones].mean().reset_index()
    pd.set_option("display.float_format", "{:.2f}".format)
    print(resumen.sort_values(by=["id", "game"]))
# Cargar datos desde el CSV
def cargar_datos():
    try:
        df = pd.read_csv("csvs/emotions/csv_unido.csv")
        return df
    except FileNotFoundError:
        print("Error: El archivo 'csvs/emotions/csv_unido.csv' no se encontró.")
        sys.exit(1)
# === SELECTOR DE FUNCIONES DINÁMICO ===
def obtener_funciones_disponibles():
    funciones = {
        nombre: func for nombre, func in globals().items()
        if inspect.isfunction(func)
        and func.__module__ == __name__
        and nombre not in ['obtener_funciones_disponibles', 'selector_de_funciones', 'cargar_datos']
    }
    return funciones

def selector_de_funciones():
    while True:
        funciones = obtener_funciones_disponibles()
        nombres = list(funciones.keys())

        print("\n=== MENÚ DE FUNCIONES DISPONIBLES ===")
        for i, nombre in enumerate(nombres, 1):
            print(f"{i}. {nombre}")
        print(f"{len(nombres)+1}. Salir")

        try:
            opcion = int(input("Selecciona una opción: "))
            if opcion == len(nombres) + 1:
                print("Saliendo del programa.")
                break
            elif 1 <= opcion <= len(nombres):
                print(f"\n--- Ejecutando '{nombres[opcion-1]}' ---")
                funciones[nombres[opcion - 1]]()
            else:
                print("Opción inválida.")
        except ValueError:
            print("Por favor, ingresa un número válido.")

if __name__ == "__main__":
    selector_de_funciones()
