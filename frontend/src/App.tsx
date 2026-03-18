import { useState } from 'react';
import './App.css';
import { RiskView } from './views/RiskView';

function App() {
  // Estado para controlar qué pantalla se muestra (Simulando un enrutador básico)
  const [activeTab, setActiveTab] = useState<'analisis' | 'registro'>('analisis');

  return (
    <div className="dashboard-container">
      {/* MENÚ LATERAL */}
      <aside className="sidebar">
        <div className="sidebar-title">
          🎓 Sistema Predictivo BDI
        </div>
        <button 
          className={`nav-button ${activeTab === 'analisis' ? 'active' : ''}`}
          onClick={() => setActiveTab('analisis')}
        >
          📊 Análisis de Riesgo
        </button>
        <button 
          className={`nav-button ${activeTab === 'registro' ? 'active' : ''}`}
          onClick={() => setActiveTab('registro')}
        >
          📝 Registro de Datos
        </button>
      </aside>

      {/* CONTENIDO PRINCIPAL */}
      <main className="main-content">
        {activeTab === 'analisis' && (
          <div className="card">
            <h2 className="card-title">Panel de Predicción IA</h2>
            <p style={{ color: '#6b7280', marginBottom: '20px' }}>
              Ingrese el ID del estudiante para activar el Agente BDI y calcular el riesgo académico.
            </p>
            {/* Aquí mandamos a llamar tu Vista de Análisis que ya tienes */}
            <RiskView />
          </div>
        )}

        {activeTab === 'registro' && (
          <div className="card">
            <h2 className="card-title">Ingreso de Nueva Información</h2>
            <p style={{ color: '#6b7280', marginBottom: '20px' }}>
              Formulario para registrar calificaciones, asistencias y tareas (Módulo de Presentador en construcción).
            </p>
            
            {/* Esqueleto del formulario (Vista) */}
            <div className="form-group">
              <label>ID de Inscripción</label>
              <input type="number" className="form-input" placeholder="Ej: 5" />
            </div>
            
            <div className="form-group">
              <label>Tipo de Registro</label>
              <select className="form-input">
                <option>Calificación</option>
                <option>Asistencia</option>
                <option>Tarea</option>
              </select>
            </div>

            <div className="form-group">
              <label>Valor</label>
              <input type="number" step="0.1" className="form-input" placeholder="Ej: 8.5" />
            </div>

            <button className="btn-primary">Guardar Registro en la Base de Datos</button>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;