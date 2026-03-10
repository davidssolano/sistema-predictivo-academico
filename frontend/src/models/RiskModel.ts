export interface PredictionResult {
    estudiante: string;
    nivel_de_riesgo: string;
    recomendaciones_agente: string[];
}

export interface RiskModelInterface {
    predictRisk(studentId: number): Promise<PredictionResult>;
}

export class APIRiskModel implements RiskModelInterface {
    async predictRisk(studentId: number): Promise<PredictionResult> {
        // Vite usa import.meta.env para leer variables de entorno en React
        // Si no existe la variable (producción), asume que está en local
        const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
        
        const response = await fetch(`${API_BASE_URL}/prediccion/${studentId}`);
        if (!response.ok) {
            throw new Error("Error al obtener la predicción del servidor");
        }
        return response.json();
    }
}