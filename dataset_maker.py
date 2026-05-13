import pandas as pd
import numpy as np
import time

def generar_dataset(cantidad, inyectar_ruido=False):
    print(f"Generando {cantidad} registros...")
    
    # 1. Generación de variables con distribución lógica (campana de Gauss)
    # Asistencia promedio de 80%, con variación.
    asistencia = np.random.normal(80, 15, cantidad).clip(0, 100)
    
    # El promedio depende fuertemente de la asistencia + un factor aleatorio
    promedio = (asistencia / 100) * 10 + np.random.normal(0, 1.5, cantidad)
    promedio = promedio.clip(0, 10.0)
    
    # Las tareas entregadas también se correlacionan con la asistencia
    tareas = np.random.normal(asistencia, 10, cantidad).clip(0, 100)
    
    # Participación y faltas (distribuciones aleatorias)
    participacion = np.random.choice(['Alta', 'Media', 'Baja'], cantidad, p=[0.3, 0.5, 0.2])
    faltas = np.random.poisson(0.5, cantidad) # La mayoría tendrá 0 o 1 falta

    # 2. Cálculo de la Variable Objetivo (Reglas de Riesgo Académico)
    riesgo = []
    for i in range(cantidad):
        if promedio[i] < 6.0 or asistencia[i] < 70:
            riesgo.append('Alto riesgo')
        elif promedio[i] < 8.0:
            riesgo.append('Medio riesgo')
        else:
            riesgo.append('Sin riesgo')

    # Crear el DataFrame de Pandas
    df = pd.DataFrame({
        'Promedio_Notas': np.round(promedio, 1),
        'Asistencia_Pct': np.round(asistencia, 1),
        'Tareas_Entregadas_Pct': np.round(tareas, 1),
        'Nivel_Participacion': participacion,
        'Faltas_Disciplinarias': faltas,
        'Nivel_Riesgo': riesgo
    })

    # 3. Inyección de Ruido (Solo para la fase de limpieza en el entrenamiento)
    if inyectar_ruido:
        print("Inyectando 20% de anomalías, datos sucios y outliers...")
        num_errores = int(cantidad * 0.2) # El 20% exacto
        
        # Seleccionar filas al azar para arruinarlas
        indices_ruido = np.random.choice(cantidad, num_errores, replace=False)
        
        for idx in indices_ruido:
            tipo_error = np.random.choice(['nulo_nota', 'nulo_tareas', 'outlier_positivo', 'outlier_negativo', 'error_texto'])
            
            if tipo_error == 'nulo_nota':
                df.loc[idx, 'Promedio_Notas'] = np.nan # Dato vacío
            elif tipo_error == 'nulo_tareas':
                df.loc[idx, 'Tareas_Entregadas_Pct'] = np.nan # Dato vacío
            elif tipo_error == 'outlier_positivo':
                df.loc[idx, 'Promedio_Notas'] = 150.0 # ¡Imposible! (Outlier)
            elif tipo_error == 'outlier_negativo':
                df.loc[idx, 'Asistencia_Pct'] = -25.0 # ¡Imposible! (Outlier)
            elif tipo_error == 'error_texto':
                df.loc[idx, 'Nivel_Participacion'] = 'Desconocido_X99' # Basura
                
    return df

# ==========================================
# EJECUCIÓN DEL SCRIPT
# ==========================================
start_time = time.time()

# 1. Dataset para entrenar (SUCIO - Para probar tu limpieza de datos)
print("--- CREANDO DATASET DE ENTRENAMIENTO ---")
df_train = generar_dataset(50000, inyectar_ruido=True)
df_train.to_csv('dataset_entrenamiento.csv', index=False)

# 2. Dataset para validación ciega (LIMPIO - Para ver si la IA aprendió)
print("\n--- CREANDO DATASET DE PRUEBA CIEGA ---")
df_test = generar_dataset(50000, inyectar_ruido=False)
df_test.to_csv('dataset_prueba_ciega.csv', index=False)

print(f"\n✅ ¡Éxito! 100,000 registros generados en {round(time.time() - start_time, 2)} segundos.")
print("Archivos exportados: 'dataset_entrenamiento.csv' y 'dataset_prueba_ciega.csv'")