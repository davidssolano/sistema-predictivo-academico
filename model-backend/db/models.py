from sqlalchemy import Column, Integer, String, Date, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
import datetime

Base = declarative_base()

class Estudiante(Base):
    __tablename__ = 'estudiante'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    matricula = Column(String(20), unique=True, index=True, nullable=False)
    fecha_registro = Column(DateTime, default=datetime.datetime.utcnow)
    
    inscripciones = relationship("Inscripcion", back_populates="estudiante")
    historial = relationship("HistorialAcademico", back_populates="estudiante")

class Materia(Base):
    __tablename__ = 'materia'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    creditos = Column(Integer, nullable=False)
    
    inscripciones = relationship("Inscripcion", back_populates="materia")

class Inscripcion(Base):
    __tablename__ = 'inscripcion'
    id = Column(Integer, primary_key=True, index=True)
    estudiante_id = Column(Integer, ForeignKey('estudiante.id', ondelete="CASCADE"))
    materia_id = Column(Integer, ForeignKey('materia.id', ondelete="CASCADE"))
    periodo = Column(String(20), nullable=False)
    
    estudiante = relationship("Estudiante", back_populates="inscripciones")
    materia = relationship("Materia", back_populates="inscripciones")
    calificaciones = relationship("Calificacion", back_populates="inscripcion")

class Calificacion(Base):
    __tablename__ = 'calificacion'
    id = Column(Integer, primary_key=True, index=True)
    inscripcion_id = Column(Integer, ForeignKey('inscripcion.id', ondelete="CASCADE"))
    nota = Column(Float, nullable=False)
    tipo_evaluacion = Column(String(50), nullable=False)
    
    inscripcion = relationship("Inscripcion", back_populates="calificaciones")

class HistorialAcademico(Base):
    __tablename__ = 'historial_academico'
    id = Column(Integer, primary_key=True, index=True)
    estudiante_id = Column(Integer, ForeignKey('estudiante.id', ondelete="CASCADE"))
    promedio_historico = Column(Float)
    materias_reprobadas = Column(Integer, default=0)
    
    estudiante = relationship("Estudiante", back_populates="historial")

class Asistencia(Base):
    __tablename__ = 'asistencia'
    id = Column(Integer, primary_key=True, index=True)
    inscripcion_id = Column(Integer, ForeignKey('inscripcion.id', ondelete="CASCADE"))
    fecha = Column(Date, nullable=False)
    presente = Column(Boolean, nullable=False)

class Tareas(Base):
    __tablename__ = 'tareas'
    id = Column(Integer, primary_key=True, index=True)
    inscripcion_id = Column(Integer, ForeignKey('inscripcion.id', ondelete="CASCADE"))
    descripcion = Column(String(200), nullable=False)
    entregada = Column(Boolean, nullable=False)
    fecha_limite = Column(Date, nullable=False)