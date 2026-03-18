import sys
import os

# Agrega la carpeta actual al radar de Python para que encuentre models.py, crud.py, etc.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

# Importaciones internas de tu proyecto
import models
import crud
import schemas
from database import engine, get_db

# (Si tienes tu agente en un archivo separado, impórtalo aquí)
# from ai_engine.bdi_agent import AcademicBDIAgent

# Crea las tablas en la base de datos al arrancar (si no existen)
models.Base.metadata.create_all(bind=engine)

# ==========================================
# 1. CONFIGURACIÓN LIMPIA DE LA API (MODELO MVP)
# ==========================================
app = FastAPI(
    title="Sistema Predictivo Académico - Modelo API",
    description="API interna del sistema. Acceso exclusivo para el Presentador (Frontend en Vercel).",
    version="1.0.0"
)

# ==========================================
# 2. SEGURIDAD CORS (VITAL PARA CONECTAR VERCEL CON RENDER)
# ==========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En un entorno corporativo estricto, aquí iría solo la URL de tu Vercel
    allow_credentials=True,
    allow_methods=["*"],  # Permite GET, POST, PUT, DELETE
    allow_headers=["*"],
)

# ==========================================
# 3. ENDPOINT DE ESTADO (RAÍZ)
# ==========================================
@app.get("/")
def read_root():
    return {"message": "API del Sistema Predictivo Académico funcionando perfectamente bajo arquitectura MVP."}

# ==========================================
# 4. RUTAS CRUD (ESTUDIANTES, MATERIAS, NOTAS, ETC.)
# ==========================================
# ⚠️ IMPORTANTE: Aquí debes dejar los endpoints que ya habías programado. 
# Te pongo el de estudiantes como ejemplo:

@app.get("/estudiantes/", response_model=list[schemas.Estudiante])
def read_estudiantes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_estudiantes(db, skip=skip, limit=limit)

@app.post("/estudiantes/", response_model=schemas.Estudiante)
def create_estudiante(estudiante: schemas.EstudianteCreate, db: Session = Depends(get_db)):
    return crud.create_estudiante(db=db, estudiante=estudiante)

# -> PEGA AQUÍ TUS @app.post DE INSCRIPCIONES, CALIFICACIONES, ASISTENCIAS Y TAREAS <-


# ==========================================
# 5. ENDPOINT DE IA Y AGENTE BDI (EL CEREBRO)
# ==========================================
# (Asegúrate de que el nombre de la función coincida con cómo la habías programado)
@app.get("/analizar/{estudiante_id}")
def analizar_riesgo_estudiante(estudiante_id: int, db: Session = Depends(get_db)):
    # Aquí es donde llamas a tu Agente BDI y a Scikit-Learn
    # Ejemplo:
    # agente = AcademicBDIAgent(db)
    # resultado = agente.analizar_y_recomendar(estudiante_id)
    # return resultado
    pass # Reemplaza este pass con la lógica real de tu endpoint de análisis