import { RiskView } from './views/RiskView';

function App() {
  return (
    <div>
      {/* Botón de navegación hacia el panel del backend */}
      <div style={{ textAlign: 'center', margin: '20px 0' }}>
        <a 
          href="https://api-academica-mvp.onrender.com/docs" 
          target="_blank" 
          rel="noopener noreferrer"
          style={{ 
            padding: '10px 20px', 
            backgroundColor: '#007bff', 
            color: 'white', 
            textDecoration: 'none', 
            borderRadius: '5px', 
            fontWeight: 'bold',
            fontFamily: 'sans-serif'
          }}
        >
          ⚙️ Ir al Panel de Registro de Datos
        </a>
      </div>

      {/* Tu vista principal (MVP) */}
      <RiskView />
    </div>
  );
}

export default App;