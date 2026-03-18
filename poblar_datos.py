import requests
import random
import time

BASE_URL = "https://api-academica-mvp.onrender.com"

nombres = ["Ana", "Luis", "Carlos", "Marta", "Jorge", "Lucía", "Pedro", "Elena", "Diego", "Valentina", "Andrés", "Camila", "Mateo", "Valeria", "Sebastián", "Mariana"]
apellidos = ["García", "Martínez", "López", "González", "Pérez", "Rodríguez", "Sánchez", "Ramírez", "Cruz", "Gómez", "Flores", "Morales", "Ortiz", "Gutiérrez", "Ruiz"]

print("🚀 Iniciando inyección masiva de 50 estudiantes en Supabase...")

# Asegurar que existe al menos una materia
res_materia = requests.post(f"{BASE_URL}/materias/", json={"nombre": "Física Fundamental", "codigo": "FIS-101"})
materia_id = res_materia.json().get("id", 1) if res_materia.status_code == 200 else 1

ids_generados = []

for i in range(50):
    nombre = random.choice(nombres)
    apellido = random.choice(apellidos)
    matricula = f"MAT-{random.randint(1000, 9999)}"

    # 1. Crear Estudiante y capturar su ID REAL de la base de datos
    res_est = requests.post(f"{BASE_URL}/estudiantes/", json={"nombre": nombre, "apellidos": apellido, "matricula": matricula})
    
    if res_est.status_code != 200:
        continue
        
    estudiante_id = res_est.json().get("id")
    ids_generados.append(estudiante_id)
    
    # 2. Inscribir al estudiante
    res_insc = requests.post(f"{BASE_URL}/inscripciones/", json={"estudiante_id": estudiante_id, "materia_id": materia_id})
    inscripcion_id = res_insc.json().get("id")

    # 3. Asignarle un "destino" aleatorio para probar la IA
    perfil = random.choice(["Alto", "Medio", "Sin Riesgo", "Sin Riesgo"])
    
    # 4. Inyectar 5 registros de historial por cada estudiante
    for _ in range(5):
        if perfil == "Sin Riesgo":
            nota = round(random.uniform(8.0, 10.0), 1)
            asistencia = 1
            tarea = 1
        elif perfil == "Medio":
            nota = round(random.uniform(6.0, 7.9), 1)
            asistencia = random.choice([0, 1, 1])
            tarea = random.choice([0, 1])
        else: # Riesgo Alto
            nota = round(random.uniform(2.0, 5.9), 1)
            asistencia = random.choice([0, 0, 1])
            tarea = 0
            
        requests.post(f"{BASE_URL}/calificaciones/", json={"inscripcion_id": inscripcion_id, "valor": nota})
        requests.post(f"{BASE_URL}/asistencias/", json={"inscripcion_id": inscripcion_id, "valor": asistencia})
        requests.post(f"{BASE_URL}/tareas/", json={"inscripcion_id": inscripcion_id, "valor": tarea})

    # Imprimir en la consola exactamente qué ID le tocó
    print(f"[{i+1}/50] Registrado: {nombre} {apellido} | ID Real: {estudiante_id} | Simulando perfil: {perfil}")
    time.sleep(0.2) # Pausa breve para cuidar la memoria del servidor

print(f"\n✅ ¡Inyección masiva completada con éxito!")
print(f"👉 IDs disponibles para consultar en tu aplicación web: {ids_generados}")