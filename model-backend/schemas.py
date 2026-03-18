from pydantic import BaseModel
from typing import List, Optional

class EstudianteBase(BaseModel):
    nombre: str
    apellidos: str
    matricula: str

class EstudianteCreate(EstudianteBase):
    pass

class Estudiante(EstudianteBase):
    id: int
    class Config:
        from_attributes = True
        
# (Aquí deberías agregar los schemas de Materias, Inscripciones, etc., 
# pero con Estudiante es suficiente para que el servidor arranque sin errores)