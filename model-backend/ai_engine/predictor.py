import pickle
import os
import numpy as np

class AcademicRiskPredictor:
    def __init__(self):
        # Cargamos el modelo entrenado
        model_path = os.path.join(os.path.dirname(__file__), 'decision_tree_model.pkl')
        try:
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
        except FileNotFoundError:
            self.model = None
            print("Advertencia: Modelo no encontrado. Ejecuta train_model.py primero.")

    def predict(self, data: dict) -> str:
        if not self.model:
            return "Modelo no inicializado"

        # Orden de variables: [promedio, asistencia, tareas_no_entregadas, historial]
        features = np.array([[
            data['promedio'], 
            data['asistencia'], 
            data['tareas_no_entregadas'], 
            data['historial']
        ]])
        
        prediction = self.model.predict(features)[0]
        
        risk_map = {0: "Sin riesgo", 1: "Riesgo medio", 2: "Alto riesgo"}
        return risk_map.get(prediction, "Desconocido")