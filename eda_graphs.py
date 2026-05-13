import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("--- INICIANDO ANÁLISIS GRÁFICO (EDA) ---")

# 1. Cargar el dataset limpio
df = pd.read_csv('dataset_entrenamiento_LIMPIO.csv')

# Configurar el estilo visual de las gráficas
sns.set_theme(style="whitegrid")

# ---------------------------------------------------------
# GRÁFICA 1: Distribución del Nivel de Riesgo (¿Cómo está la población?)
# ---------------------------------------------------------
print("Generando Gráfica 1: Distribución de Riesgo...")
plt.figure(figsize=(8, 6))
sns.countplot(data=df, x='Nivel_Riesgo', palette='Set2', order=['Alto riesgo', 'Medio riesgo', 'Sin riesgo'])
plt.title('Distribución de Estudiantes por Nivel de Riesgo', fontsize=14)
plt.xlabel('Categoría de Riesgo')
plt.ylabel('Cantidad de Estudiantes')
plt.savefig('eda_1_distribucion_riesgo.png')
plt.close()

# ---------------------------------------------------------
# GRÁFICA 2: Histograma de Promedio de Notas (Campana de Gauss)
# ---------------------------------------------------------
print("Generando Gráfica 2: Histograma de Notas...")
plt.figure(figsize=(8, 6))
sns.histplot(df['Promedio_Notas'], bins=20, kde=True, color='blue')
plt.title('Distribución del Promedio de Notas en la Población', fontsize=14)
plt.xlabel('Promedio de Notas (0.0 a 10.0)')
plt.ylabel('Frecuencia')
plt.savefig('eda_2_histograma_notas.png')
plt.close()

# ---------------------------------------------------------
# GRÁFICA 3: Relación entre Notas y Asistencia (Gráfico de Dispersión)
# ---------------------------------------------------------
print("Generando Gráfica 3: Notas vs Asistencia...")
plt.figure(figsize=(8, 6))
# Tomamos una muestra de 1000 estudiantes para que la gráfica no se sature de puntos
muestra = df.sample(1000, random_state=42) 
sns.scatterplot(data=muestra, x='Asistencia_Pct', y='Promedio_Notas', hue='Nivel_Riesgo', palette='Set1', alpha=0.7)
plt.title('Relación: Promedio de Notas vs Porcentaje de Asistencia', fontsize=14)
plt.xlabel('Porcentaje de Asistencia (%)')
plt.ylabel('Promedio de Notas')
plt.legend(title='Nivel de Riesgo')
plt.savefig('eda_3_dispersion.png')
plt.close()

print("✅ Análisis finalizado. 3 gráficas exportadas exitosamente (.png).")