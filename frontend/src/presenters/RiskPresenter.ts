import { RiskModelInterface } from '../models/RiskModel';

// La interfaz que la Vista DEBE implementar
export interface IRiskView {
    showLoading(): void;
    hideLoading(): void;
    displayRiskResult(studentName: string, riskLevel: string, recommendations: string[]): void;
    showError(message: string): void;
}

export class RiskPresenter {
    private view: IRiskView;
    private model: RiskModelInterface;

    constructor(view: IRiskView, model: RiskModelInterface) {
        this.view = view;
        this.model = model;
    }

    // Método que la vista llama cuando el usuario hace clic en el botón
    async analyzeStudentRisk(studentId: number) {
        this.view.showLoading();
        try {
            const result = await this.model.predictRisk(studentId);
            this.view.displayRiskResult(
                result.estudiante, 
                result.nivel_de_riesgo, 
                result.recomendaciones_agente
            );
        } catch (error) {
            this.view.showError("Hubo un problema al conectar con el servidor de IA.");
        } finally {
            this.view.hideLoading();
        }
    }
}