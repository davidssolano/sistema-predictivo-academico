export interface IRiskModel {
    getStudentRisk(id: number): Promise<{ name: string; riskLevel: string; recommendations: string[] }>;
}

export class APIRiskModel implements IRiskModel {
    async getStudentRisk(id: number) {
        // AQUÍ ESTABA EL ERROR: Cambiamos /prediccion/ por /analizar/
        const response = await fetch(`https://api-academica-mvp.onrender.com/analizar/${id}`);
        
        if (!response.ok) {
            throw new Error('Hubo un problema al conectar con el servidor de IA.');
        }

        const data = await response.json();
        
        // Mapeamos los datos que llegan de Python a lo que espera React
        return {
            name: data.nombre || `Estudiante #${id}`, // Si Python no manda nombre, ponemos el ID
            riskLevel: data.riesgo || 'Desconocido',
            recommendations: data.recomendaciones || ['Sin recomendaciones disponibles.']
        };
    }
}