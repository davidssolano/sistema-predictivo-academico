from sqlalchemy.orm import Session
import models, schemas

def get_estudiantes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Estudiante).offset(skip).limit(limit).all()

def create_estudiante(db: Session, estudiante: schemas.EstudianteCreate):
    db_estudiante = models.Estudiante(**estudiante.model_dump())
    db.add(db_estudiante)
    db.commit()
    db.refresh(db_estudiante)
    return db_estudiante