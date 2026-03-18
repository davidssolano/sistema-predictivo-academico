export interface RiskModelInterface {
    // Le devolvemos el nombre que el Presentador espera: predictRisk
    predictRisk(id: number): Promise<{ name: string; riskLevel: string; recommendations: string[] }>;
}

export class APIRiskModel implements RiskModelInterface {
    // También cambiamos el nombre aquí
    async predictRisk(id: number) {
        const response = await fetch(`https://api-academica-mvp.onrender.com/analizar/${id}`);
        
        if (!response.ok) {
            throw new Error('Hubo un problema al conectar con el servidor de IA.');
        }

        const data: any = await response.json(); 
        
        return {
            name: data.nombre || `Estudiante #${id}`,
            riskLevel: data.riesgo || 'Desconocido',
            recommendations: data.recomendaciones || ['Sin recomendaciones disponibles.']
        };
    }
}