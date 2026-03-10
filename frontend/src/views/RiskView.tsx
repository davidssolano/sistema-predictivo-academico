import React, { useState } from 'react';
import { RiskPresenter, IRiskView } from '../presenters/RiskPresenter';
import { APIRiskModel } from '../models/RiskModel';

export const RiskView: React.FC = () => {
    // Estados de React solo para renderizar
    const [studentId, setStudentId] = useState<number>(1);
    const [studentName, setStudentName] = useState<string>('');
    const [risk, setRisk] = useState<string>('');
    const [recs, setRecs] = useState<string[]>([]);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string>('');

    // Implementación de la interfaz IRiskView exigida por el Presentador
    const viewImplementation: IRiskView = {
        showLoading: () => { setLoading(true); setError(''); },
        hideLoading: () => setLoading(false),
        displayRiskResult: (name, riskLevel, recommendations) => {
            setStudentName(name);
            setRisk(riskLevel);
            setRecs(recommendations);
        },
        showError: (msg) => setError(msg)
    };

    // Instanciamos el Presentador pasándole esta vista y el modelo API
    const presenter = new RiskPresenter(viewImplementation, new APIRiskModel());

    return (
        <div style={{ fontFamily: 'Arial', maxWidth: '600px', margin: '40px auto', padding: '20px', border: '1px solid #ccc', borderRadius: '8px' }}>
            <h2>Sistema Predictivo de Riesgo Académico</h2>
            <p>Arquitectura MVP - Agente BDI - IA</p>
            
            <div style={{ marginBottom: '20px' }}>
                <label>ID del Estudiante: </label>
                <input 
                    type="number" 
                    value={studentId} 
                    onChange={(e) => setStudentId(Number(e.target.value))}
                    style={{ padding: '5px', marginRight: '10px' }}
                />
                {/* La vista NO hace fetch, solo avisa al presentador */}
                <button 
                    onClick={() => presenter.analyzeStudentRisk(studentId)}
                    style={{ padding: '6px 15px', backgroundColor: '#007BFF', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
                >
                    Analizar Desempeño
                </button>
            </div>

            {loading && <p>🧠 La Inteligencia Artificial está analizando...</p>}
            {error && <p style={{ color: 'red' }}>{error}</p>}

            {risk && !loading && (
                <div style={{ marginTop: '20px', padding: '15px', backgroundColor: risk === 'Alto riesgo' ? '#ffebee' : '#e8f5e9', borderRadius: '8px' }}>
                    <h3>Resultados para: {studentName}</h3>
                    <h4 style={{ color: risk === 'Alto riesgo' ? 'red' : 'green' }}>
                        Clasificación: {risk}
                    </h4>
                    
                    <h5>🤖 Recomendaciones del Agente BDI:</h5>
                    <ul>
                        {recs.map((r, i) => <li key={i} style={{ marginBottom: '8px' }}>{r}</li>)}
                    </ul>
                </div>
            )}
        </div>
    );
};