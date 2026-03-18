import sys
import os

# Agrega la carpeta actual al radar de Python para que encuentre models.py, database.py, etc.
# Esto previene el "ModuleNotFoundError" en Render.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

# Importaciones de tu propia arquitectura
import models
import schemas
from database import engine, get_db

# Crea las tablas en la base de datos si no existen
models.Base.metadata.create_all(bind=engine)

# Inicializa la aplicación
app = FastAPI(
    title="Sistema Predictivo Académico - Modelo API",
    description="API interna del sistema. Acceso exclusivo para el Presentador (Frontend en Vercel).",
    version="1.0.0"
)

# Configuración de CORS (Permite que Vercel se comunique con Render sin bloqueos de seguridad)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# RUTAS (ENDPOINTS) DEL MVP
# ==========================================

@app.get("/")
def read_root():
    return {"mensaje": "API del Sistema Predictivo BDI funcionando correctamente"}

@app.get("/estudiantes/", response_model=list[schemas.Estudiante])
def read_estudiantes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Devuelve la lista de estudiantes
    estudiantes = db.query(models.Estudiante).offset(skip).limit(limit).all()
    return estudiantes

@app.post("/estudiantes/", response_model=schemas.Estudiante)
def create_estudiante(estudiante: schemas.EstudianteCreate, db: Session = Depends(get_db)):
    # Verifica si la matrícula ya existe antes de crearlo
    db_estudiante = db.query(models.Estudiante).filter(models.Estudiante.matricula == estudiante.matricula).first()
    if db_estudiante:
        raise HTTPException(status_code=400, detail="La matrícula ya está registrada")
    
    nuevo_estudiante = models.Estudiante(
        nombre=estudiante.nombre,
        apellidos=estudiante.apellidos,
        matricula=estudiante.matricula
    )
    db.add(nuevo_estudiante)
    db.commit()
    db.refresh(nuevo_estudiante)
    return nuevo_estudiante

@app.get("/analizar/{estudiante_id}")
def analizar_riesgo_estudiante(estudiante_id: int, db: Session = Depends(get_db)):
    # 1. Buscamos al estudiante real en la base de datos
    estudiante = db.query(models.Estudiante).filter(models.Estudiante.id == estudiante_id).first()
    
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado.")

    # =================================================================
    # LÓGICA DE IA (DINÁMICA BASADA EN DATOS REALES)
    # Extrae las notas de la DB y calcula el riesgo de forma inteligente
    # =================================================================
    
    # Recopilamos todas las calificaciones del estudiante a través de sus inscripciones
    todas_las_calificaciones = []
    for inscripcion in estudiante.inscripciones:
        todas_las_calificaciones.extend([c.valor for c in inscripcion.calificaciones])
    
    # Calculamos el promedio real matemático
    if todas_las_calificaciones:
        promedio_real = sum(todas_las_calificaciones) / len(todas_las_calificaciones)
    else:
        promedio_real = 0 # Si no tiene notas cargadas
        
    nombre_est = estudiante.nombre

    # Árbol de decisión del Agente BDI
    if promedio_real == 0:
        riesgo = "Desconocido"
        comentarios = [
            f"El estudiante {nombre_est} aún no tiene calificaciones registradas en el sistema.", 
            "Sugerencia: Solicitar a los docentes la actualización de notas."
        ]
    elif promedio_real < 6.0:
        riesgo = "Alto riesgo"
        comentarios = [
            f"Urgente: {nombre_est} presenta alerta crítica de reprobación (Promedio: {promedio_real:.1f}).", 
            "Acción requerida: Agendar tutoría de nivelación de inmediato.", 
            "Acción requerida: Contactar a la familia o acudiente."
        ]
    elif promedio_real < 8.0:
        riesgo = "Medio riesgo"
        comentarios = [
            f"Alerta moderada: El rendimiento de {nombre_est} (Promedio: {promedio_real:.1f}) muestra inestabilidad.", 
            "Evaluar el nivel de participación y entrega de tareas recientes.", 
            "Sugerencia: Recomendar al estudiante unirse a un grupo de estudio."
        ]
    else:
        riesgo = "Sin riesgo detectado"
        comentarios = [
            f"Excelente desempeño: {nombre_est} mantiene un promedio sobresaliente ({promedio_real:.1f}).", 
            "Considerar asignar retos adicionales para mantener su motivación alta.", 
            "Felicitar por el cumplimiento de sus objetivos académicos."
        ]

    # 3. Devolvemos el JSON con las llaves exactas que espera Vercel
    return {
        "nombre": f"{estudiante.nombre} {estudiante.apellidos}",
        "riesgo": riesgo,
        "recomendaciones": comentarios
    }

@app.get("/generar-notas-prueba/")
def generar_notas_prueba(db: Session = Depends(get_db)):
    import random
    estudiantes = db.query(models.Estudiante).all()
    
    if not estudiantes:
        return {"error": "No hay estudiantes en la base de datos."}

    # 1. Crear Materias
    nombres_materias = ["Matemáticas", "Física", "Programación"]
    materias_db = []
    for nombre in nombres_materias:
        mat = db.query(models.Materia).filter(models.Materia.nombre == nombre).first()
        if not mat:
            mat = models.Materia(nombre=nombre, codigo=f"{nombre[:3].upper()}101")
            db.add(mat)
            db.commit()
            db.refresh(mat)
        materias_db.append(mat)

    # 2. Inscribir y Calificar
    estudiantes_modificados = 0
    for est in estudiantes:
        tiene_inscripciones = db.query(models.Inscripcion).filter(models.Inscripcion.estudiante_id == est.id).first()
        if tiene_inscripciones:
            continue # Si ya tiene notas, lo saltamos

        perfil = est.id % 3 
        estudiantes_modificados += 1

        for mat in materias_db:
            inscripcion = models.Inscripcion(estudiante_id=est.id, materia_id=mat.id)
            db.add(inscripcion)
            db.commit()
            db.refresh(inscripcion)

            if perfil == 0:
                nota = random.uniform(4.0, 5.9) # Perfil bajo
            elif perfil == 1:
                nota = random.uniform(8.0, 10.0) # Perfil alto
            else:
                nota = random.uniform(6.0, 7.9) # Perfil medio

            calificacion = models.Calificacion(inscripcion_id=inscripcion.id, valor=round(nota, 1))
            db.add(calificacion)
            
    db.commit()
    return {"mensaje": f"¡Éxito! Se generaron materias y notas aleatorias para {estudiantes_modificados} estudiantes."}