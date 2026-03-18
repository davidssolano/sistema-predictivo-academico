import random
from database import SessionLocal, engine
import models

# Aseguramos que las tablas existan
models.Base.metadata.create_all(bind=engine)
db = SessionLocal()

def inyectar_notas():
    estudiantes = db.query(models.Estudiante).all()
    if not estudiantes:
        print("❌ No hay estudiantes en la base de datos.")
        return

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
    
    print(f"✅ Materias listas. Generando notas para {len(estudiantes)} estudiantes...")

    # 2. Inscribir y Calificar a cada estudiante
    for est in estudiantes:
        tiene_inscripciones = db.query(models.Inscripcion).filter(models.Inscripcion.estudiante_id == est.id).first()
        if tiene_inscripciones:
            continue

        perfil = est.id % 3 

        for mat in materias_db:
            inscripcion = models.Inscripcion(estudiante_id=est.id, materia_id=mat.id)
            db.add(inscripcion)
            db.commit()
            db.refresh(inscripcion)

            if perfil == 0:
                nota = random.uniform(4.0, 5.9) # Perfil bajo rendimiento
            elif perfil == 1:
                nota = random.uniform(8.0, 10.0) # Perfil sobresaliente
            else:
                nota = random.uniform(6.0, 7.9) # Perfil regular

            calificacion = models.Calificacion(inscripcion_id=inscripcion.id, valor=round(nota, 1))
            db.add(calificacion)
    
    db.commit()
    print("🎉 ¡Notas generadas e inyectadas con éxito en Supabase!")

if __name__ == "__main__":
    inyectar_notas()