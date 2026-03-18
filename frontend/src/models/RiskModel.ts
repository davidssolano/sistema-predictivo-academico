// 1. Aquí le devolvemos su nombre original: RiskModelInterface
export interface RiskModelInterface {
    getStudentRisk(id: number): Promise<{ name: string; riskLevel: string; recommendations: string[] }>;
}

// 2. Y aquí le decimos a la clase que use ese nombre
export class APIRiskModel implements RiskModelInterface {
    async getStudentRisk(id: number) {
        const response = await fetch(`https://api-academica-mvp.onrender.com/analizar/${id}`);
        
        if (!response.ok) {
            throw new Error('Hubo un problema al conectar con el servidor de IA.');
        }

        const data: any = await response.json(); // Le agregamos "any" por si las dudas con TypeScript
        
        return {
            name: data.nombre || `Estudiante #${id}`,
            riskLevel: data.riesgo || 'Desconocido',
            recommendations: data.recomendaciones || ['Sin recomendaciones disponibles.']
        };
    }
}