from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Estudiante(Base):
    __tablename__ = "estudiantes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    apellidos = Column(String)
    matricula = Column(String, unique=True, index=True)
    
    # Relación: Un estudiante tiene muchas inscripciones
    inscripciones = relationship("Inscripcion", back_populates="estudiante")

class Materia(Base):
    __tablename__ = "materias"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    codigo = Column(String, unique=True)
    
    # Relación: Una materia tiene muchas inscripciones
    inscripciones = relationship("Inscripcion", back_populates="materia")

class Inscripcion(Base):
    __tablename__ = "inscripciones"
    
    id = Column(Integer, primary_key=True, index=True)
    estudiante_id = Column(Integer, ForeignKey("estudiantes.id"))
    materia_id = Column(Integer, ForeignKey("materias.id"))

    # Relaciones hacia arriba
    estudiante = relationship("Estudiante", back_populates="inscripciones")
    materia = relationship("Materia", back_populates="inscripciones")
    
    # Relaciones hacia abajo (El historial)
    calificaciones = relationship("Calificacion", back_populates="inscripcion")
    asistencias = relationship("Asistencia", back_populates="inscripcion")
    tareas = relationship("Tarea", back_populates="inscripcion")
    participaciones = relationship("Participacion", back_populates="inscripcion") # ¡Aquí está el RF6!

class Calificacion(Base):
    __tablename__ = "calificaciones"
    id = Column(Integer, primary_key=True, index=True)
    inscripcion_id = Column(Integer, ForeignKey("inscripciones.id"))
    valor = Column(Float) # Ejemplo: 8.5
    inscripcion = relationship("Inscripcion", back_populates="calificaciones")

class Asistencia(Base):
    __tablename__ = "asistencias"
    id = Column(Integer, primary_key=True, index=True)
    inscripcion_id = Column(Integer, ForeignKey("inscripciones.id"))
    valor = Column(Integer) # 1 = Presente, 0 = Ausente
    inscripcion = relationship("Inscripcion", back_populates="asistencias")

class Tarea(Base):
    __tablename__ = "tareas"
    id = Column(Integer, primary_key=True, index=True)
    inscripcion_id = Column(Integer, ForeignKey("inscripciones.id"))
    valor = Column(Integer) # 1 = Entregada, 0 = No entregada
    inscripcion = relationship("Inscripcion", back_populates="tareas")

class Participacion(Base):
    __tablename__ = "participaciones"
    id = Column(Integer, primary_key=True, index=True)
    inscripcion_id = Column(Integer, ForeignKey("inscripciones.id"))
    valor = Column(Integer) # 1 = Participó, 0 = No participó
    inscripcion = relationship("Inscripcion", back_populates="participaciones")