from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models

def create_estudiante(db: Session, nombre: str, apellidos: str, matricula: str):
    db_estudiante = models.Estudiante(nombre=nombre, apellidos=apellidos, matricula=matricula)
    db.add(db_estudiante)
    db.commit()
    db.refresh(db_estudiante)
    return db_estudiante

def get_estudiante(db: Session, estudiante_id: int):
    return db.query(models.Estudiante).filter(models.Estudiante.id == estudiante_id).first()

# RF2 - RF6: Funciones para registrar datos operativos
def registrar_inscripcion(db: Session, estudiante_id: int, materia_id: int):
    db_inscripcion = models.Inscripcion(estudiante_id=estudiante_id, materia_id=materia_id, periodo="2024-1")
    db.add(db_inscripcion)
    db.commit()
    return db_inscripcion

def registrar_calificacion(db: Session, inscripcion_id: int, nota: float):
    db_cal = models.Calificacion(inscripcion_id=inscripcion_id, nota=nota, tipo_evaluacion="Parcial")
    db.add(db_cal)
    db.commit()

def registrar_asistencia(db: Session, inscripcion_id: int, presente: bool):
    import datetime
    db_asis = models.Asistencia(inscripcion_id=inscripcion_id, fecha=datetime.date.today(), presente=presente)
    db.add(db_asis)
    db.commit()

def registrar_tarea(db: Session, inscripcion_id: int, entregada: bool):
    import datetime
    db_tarea = models.Tareas(inscripcion_id=inscripcion_id, descripcion="Tarea regular", entregada=entregada, fecha_limite=datetime.date.today())
    db.add(db_tarea)
    db.commit()

# EL CÁLCULO REAL DE MÉTRICAS PARA LA I.A.
def get_student_metrics(db: Session, estudiante_id: int):
    inscripciones = db.query(models.Inscripcion).filter(models.Inscripcion.estudiante_id == estudiante_id).all()
    if not inscripciones:
        return {"promedio": 0.0, "asistencia": 100.0, "tareas_no_entregadas": 0, "historial": 7.0}

    inscripcion_ids = [i.id for i in inscripciones]

    # 1. Promedio real de calificaciones
    promedio = db.query(func.avg(models.Calificacion.nota)).filter(models.Calificacion.inscripcion_id.in_(inscripcion_ids)).scalar() or 0.0

    # 2. Porcentaje de asistencia real
    total_clases = db.query(models.Asistencia).filter(models.Asistencia.inscripcion_id.in_(inscripcion_ids)).count()
    asistencias = db.query(models.Asistencia).filter(models.Asistencia.inscripcion_id.in_(inscripcion_ids), models.Asistencia.presente == True).count()
    asistencia_pct = (asistencias / total_clases * 100) if total_clases > 0 else 100.0

    # 3. Tareas no entregadas reales
    tareas_no_entregadas = db.query(models.Tareas).filter(models.Tareas.inscripcion_id.in_(inscripcion_ids), models.Tareas.entregada == False).count()

    return {
        "promedio": float(round(promedio, 2)),
        "asistencia": float(round(asistencia_pct, 2)),
        "tareas_no_entregadas": tareas_no_entregadas,
        "historial": 7.0 # Simulado para este MVP por simplicidad
    }