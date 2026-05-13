import pandas as pd
import numpy as np

def limpiar_datos(archivo_entrada, archivo_salida):
    print(f"--- Iniciando Fase 1: Depuración de {archivo_entrada} ---")
    
    # 1. Cargar los datos (Recolección)
    df = pd.read_csv(archivo_entrada)
    total_inicial = len(df)

    # 2. Manejo de Datos Nulos (Limpieza de vacíos)
    # En lugar de borrar todo, rellenamos los nulos con la mediana para no perder volumen de datos
    print("-> Identificando y corrigiendo valores nulos...")
    df['Promedio_Notas'] = df['Promedio_Notas'].fillna(df['Promedio_Notas'].median())
    df['Tareas_Entregadas_Pct'] = df['Tareas_Entregadas_Pct'].fillna(df['Tareas_Entregadas_Pct'].median())

    # 3. Tratamiento de Outliers (Ruido extremo)
    # Si la nota es > 10 (como ese 150 que pusimos), la bajamos a 10.0
    # Si la asistencia es < 0, la subimos a 0.0
    print("-> Corrigiendo Outliers (valores fuera de rango lógico)...")
    df['Promedio_Notas'] = df['Promedio_Notas'].clip(0.0, 10.0)
    df['Asistencia_Pct'] = df['Asistencia_Pct'].clip(0.0, 100.0)

    # 4. Estandarización de Categorías (Limpieza de texto)
    # Cambiamos cualquier cosa rara (como 'Desconocido_X99') por la categoría más común: 'Media'
    categorias_validas = ['Alta', 'Media', 'Baja']
    df['Nivel_Participacion'] = df['Nivel_Participacion'].apply(
        lambda x: x if x in categorias_validas else 'Media'
    )

    # 5. Verificación Final (Análisis de calidad)
    print("\n--- Resumen de Calidad de Datos ---")
    print(f"Registros procesados: {len(df)}")
    print(f"Valores nulos restantes:\n{df.isnull().sum()}")
    
    # Exportar el dataset impecable
    df.to_csv(archivo_salida, index=False)
    print(f"\n✅ Fase terminada. Archivo depurado guardado como: '{archivo_salida}'")

# Ejecutar el proceso
limpiar_datos('dataset_entrenamiento.csv', 'dataset_entrenamiento_LIMPIO.csv')