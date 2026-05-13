import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder

print("--- INICIANDO FASE DE ENTRENAMIENTO DE IA ---")

# 1. Cargar los datasets
df_train = pd.read_csv('dataset_entrenamiento_LIMPIO.csv')
df_test = pd.read_csv('dataset_prueba_ciega.csv') # El que el modelo nunca ha visto

# 2. Pre-procesamiento: Convertir texto a números (El modelo solo entiende matemáticas)
le_participacion = LabelEncoder()
# Entrenamos el codificador con todas las opciones posibles ('Alta', 'Media', 'Baja')
df_train['Nivel_Participacion'] = le_participacion.fit_transform(df_train['Nivel_Participacion'])
df_test['Nivel_Participacion'] = le_participacion.transform(df_test['Nivel_Participacion'])

# Separar las variables (X) del resultado a predecir (y)
X_train = df_train.drop('Nivel_Riesgo', axis=1)
y_train = df_train['Nivel_Riesgo']

X_test = df_test.drop('Nivel_Riesgo', axis=1)
y_test = df_test['Nivel_Riesgo']

# 3. Modelar los datos: Crear y Entrenar el Árbol de Decisión
print("-> Entrenando el Árbol de Decisión con 50,000 registros...")
modelo_arbol = DecisionTreeClassifier(max_depth=5, random_state=42)
modelo_arbol.fit(X_train, y_train)

# 4. Probar y Verificar: Hacer predicciones con los 50,000 datos nuevos
print("-> Poniendo a prueba el modelo con 50,000 registros ciegos...")
predicciones = modelo_arbol.predict(X_test)

# 5. Conocimiento: Evaluar qué tan bien lo hizo
precision = accuracy_score(y_test, predicciones)
print(f"\n✅ ¡Prueba superada! Precisión del modelo: {precision * 100:.2f}%\n")
print("--- Reporte Detallado ---")
print(classification_report(y_test, predicciones))

# ==========================================
# GENERACIÓN DE GRÁFICAS PARA EL DOCUMENTO
# ==========================================
print("-> Generando gráficas de rendimiento...")

# Gráfica 1: Matriz de Confusión (Muestra en qué acertó y en qué se equivocó)
plt.figure(figsize=(8, 6))
cm = confusion_matrix(y_test, predicciones, labels=modelo_arbol.classes_)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=modelo_arbol.classes_, yticklabels=modelo_arbol.classes_)
plt.title('Matriz de Confusión: Predicciones vs Realidad')
plt.xlabel('Predicción de la IA')
plt.ylabel('Riesgo Real')
plt.savefig('grafica_matriz_confusion.png') # Guarda la imagen
plt.close()

# Gráfica 2: Importancia de las Variables (Qué mira más el profesor/IA para decidir)
plt.figure(figsize=(8, 6))
importancias = modelo_arbol.feature_importances_
sns.barplot(x=importancias, y=X_train.columns, palette='viridis', hue=X_train.columns, legend=False)
plt.title('¿Qué variables influyen más en el Nivel de Riesgo?')
plt.xlabel('Nivel de Importancia')
plt.ylabel('Variable Académica')
plt.savefig('grafica_importancia_variables.png') # Guarda la imagen
plt.close()

print("✅ Gráficas guardadas como 'grafica_matriz_confusion.png' y 'grafica_importancia_variables.png'")