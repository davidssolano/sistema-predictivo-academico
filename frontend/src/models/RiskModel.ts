export interface RiskModelInterface {
    // Le decimos a TypeScript que devolveremos las variables exactas que el Presentador quiere
    predictRisk(id: number): Promise<{ 
        estudiante: string; 
        nivel_de_riesgo: string; 
        recomendaciones_agente: string[] 
    }>;
}

export class APIRiskModel implements RiskModelInterface {
    async predictRisk(id: number) {
        const response = await fetch(`https://api-academica-mvp.onrender.com/analizar/${id}`);
        
        if (!response.ok) {
            throw new Error('Hubo un problema al conectar con el servidor de IA.');
        }

        const data: any = await response.json(); 
        
        // Entregamos los datos con los nombres en español que pide tu código
        return {
            estudiante: data.nombre || `Estudiante #${id}`,
            nivel_de_riesgo: data.riesgo || 'Desconocido',
            recomendaciones_agente: data.recomendaciones || ['Sin recomendaciones disponibles.']
        };
    }
}