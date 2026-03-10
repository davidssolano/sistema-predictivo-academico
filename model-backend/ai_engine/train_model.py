import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle
import os

print("Generando dataset sintético de estudiantes...")

# Generar 1000 registros simulados
np.random.seed(42)
n_samples = 1000

# Variables (Features)
promedios = np.random.uniform(4.0, 10.0, n_samples)
asistencia = np.random.uniform(40, 100, n_samples)
tareas_no_entregadas = np.random.randint(0, 15, n_samples)
historial = np.random.uniform(5.0, 10.0, n_samples)

# Lógica determinista para crear la etiqueta (Target: 0=Sin riesgo, 1=Medio, 2=Alto)
riesgo = []
for i in range(n_samples):
    if promedios[i] < 6.0 or asistencia[i] < 60 or tareas_no_entregadas[i] > 8:
        riesgo.append(2) # Alto riesgo
    elif 6.0 <= promedios[i] < 7.5 or 60 <= asistencia[i] < 80 or 4 <= tareas_no_entregadas[i] <= 8:
        riesgo.append(1) # Riesgo medio
    else:
        riesgo.append(0) # Sin riesgo

# Crear DataFrame
df = pd.DataFrame({
    'promedio': promedios,
    'asistencia': asistencia,
    'tareas_no_entregadas': tareas_no_entregadas,
    'historial': historial,
    'riesgo': riesgo
})

X = df[['promedio', 'asistencia', 'tareas_no_entregadas', 'historial']]
y = df['riesgo']

# Dividir en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Entrenando Árbol de Decisión...")
clf = DecisionTreeClassifier(max_depth=5, random_state=42)
clf.fit(X_train, y_train)

# Evaluar
y_pred = clf.predict(X_test)
print(f"Precisión del modelo (Accuracy): {accuracy_score(y_test, y_pred) * 100:.2f}%")
print("\nReporte de Clasificación:")
print(classification_report(y_test, y_pred, target_names=["Sin Riesgo", "Medio", "Alto"]))

# Guardar el modelo entrenado
model_path = os.path.join(os.path.dirname(__file__), 'decision_tree_model.pkl')
with open(model_path, 'wb') as f:
    pickle.dump(clf, f)

print(f"Modelo guardado exitosamente en: {model_path}")