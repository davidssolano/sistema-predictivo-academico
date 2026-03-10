from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List

# Importamos nuestros módulos internos
from db import models, crud
from ai_engine.predictor import AcademicRiskPredictor
from bdi_agent.agent import AcademicBDIAgent

# --- CONFIGURACIÓN DE BASE DE DATOS ---
# Usamos SQLite local para facilitar el desarrollo inicial
import os

# --- CONFIGURACIÓN DE BASE DE DATOS (Preparado para Producción) ---
# Si existe la variable DATABASE_URL en el servidor (PostgreSQL), la usa. 
# Si no, usa SQLite por defecto para desarrollo local.
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./academic_test.db")

# Ajuste necesario porque las URLs de Postgres en algunos hostings empiezan con postgres:// en lugar de postgresql://
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Si usamos SQLite (local), necesitamos "check_same_thread". Para Postgres (nube) no.
if "sqlite" in SQLALCHEMY_DATABASE_URL:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Crea todas las tablas en la base de datos (Estudiante, Materia, Calificacion, etc.)
models.Base.metadata.create_all(bind=engine)

# --- INICIALIZACIÓN DE LA APLICACIÓN ---
app = FastAPI(title="Sistema Predictivo Académico - API")

# Habilitar CORS para que el Frontend (puerto 5173) pueda comunicarse con el Backend (puerto 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargamos el motor de Inteligencia Artificial (Minería de Datos)
predictor = AcademicRiskPredictor()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- MODELOS DE DATOS (Pydantic) ---
class EstudianteCreate(BaseModel):
    nombre: str
    apellidos: str
    matricula: str

class InscripcionCreate(BaseModel):
    estudiante_id: int
    materia_id: int

class MetricaCreate(BaseModel):
    inscripcion_id: int
    valor: float # Nota o 1/0 para booleanos

# --- ENDPOINTS / RUTAS DE LA API ---

@app.get("/")
def read_root():
    return {"message": "API del Sistema Predictivo Académico funcionando"}

# RF1 - Registrar Estudiantes
@app.post("/estudiantes/")
def registrar_estudiante(estudiante: EstudianteCreate, db: Session = Depends(get_db)):
    return crud.create_estudiante(db=db, nombre=estudiante.nombre, apellidos=estudiante.apellidos, matricula=estudiante.matricula)

# RF3 - Registrar Inscripciones (y Materias automáticamente si no existen)
@app.post("/inscripciones/")
def inscribir_materia(datos: InscripcionCreate, db: Session = Depends(get_db)):
    materia = db.query(models.Materia).filter(models.Materia.id == datos.materia_id).first()
    if not materia:
        materia = models.Materia(id=datos.materia_id, nombre="Materia de Prueba", creditos=5)
        db.add(materia)
        db.commit()
    return crud.registrar_inscripcion(db, datos.estudiante_id, datos.materia_id)

# RF4 - Registrar Calificaciones
@app.post("/calificaciones/")
def agregar_calificacion(datos: MetricaCreate, db: Session = Depends(get_db)):
    crud.registrar_calificacion(db, datos.inscripcion_id, datos.valor)
    return {"status": "Calificación registrada"}

# RF5 - Registrar Asistencia (valor 1 = Presente, 0 = Ausente)
@app.post("/asistencias/")
def agregar_asistencia(datos: MetricaCreate, db: Session = Depends(get_db)):
    presente = True if datos.valor == 1 else False
    crud.registrar_asistencia(db, datos.inscripcion_id, presente)
    return {"status": "Asistencia registrada"}

# RF6 - Registrar Tareas (valor 1 = Entregada, 0 = No entregada)
@app.post("/tareas/")
def agregar_tarea(datos: MetricaCreate, db: Session = Depends(get_db)):
    entregada = True if datos.valor == 1 else False
    crud.registrar_tarea(db, datos.inscripcion_id, entregada)
    return {"status": "Tarea registrada"}

# RF7, RF8, RF9 - Ejecutar Predicción, Clasificar Riesgo y Generar Recomendaciones
@app.get("/prediccion/{estudiante_id}")
def analizar_riesgo(estudiante_id: int, db: Session = Depends(get_db)):
    # 1. Buscar estudiante
    estudiante = crud.get_estudiante(db, estudiante_id)
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado en la base de datos")
    
    # 2. Obtener Métricas Reales desde la DB (Lógica en crud.py)
    metrics = crud.get_student_metrics(db, estudiante_id)
    
    # 3. Minería de Datos: Ejecutar Modelo Predictivo (Scikit-Learn)
    risk_level = predictor.predict(metrics)
    
    # 4. Agente BDI: Generar Recomendaciones Inteligentes
    agent = AcademicBDIAgent(metrics, risk_level)
    recommendations = agent.execute_intentions()
    
    return {
        "estudiante": f"{estudiante.nombre} {estudiante.apellidos}",
        "metricas_actuales": metrics,
        "nivel_de_riesgo": risk_level,
        "recomendaciones_agente": recommendations
    }