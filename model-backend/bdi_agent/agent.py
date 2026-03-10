class AcademicBDIAgent:
    def __init__(self, student_data: dict, risk_level: str):
        # Beliefs (Creencias sobre el estado actual del mundo/estudiante)
        self.beliefs = {
            "metrics": student_data,
            "risk": risk_level
        }
        # Desires (Objetivo del sistema)
        self.desires = "Garantizar la retención escolar y éxito académico."

    def execute_intentions(self) -> list:
        # Intentions (Planes de acción generados a partir de las creencias)
        intentions = []
        metrics = self.beliefs["metrics"]
        risk = self.beliefs["risk"]

        if risk == "Alto riesgo":
            intentions.append("🚨 ALERTA ROJA: Notificar inmediatamente a coordinación académica.")
            intentions.append("📅 Programar sesión de tutoría obligatoria urgente.")
        elif risk == "Riesgo medio":
            intentions.append("⚠️ Enviar notificación preventiva al profesor titular y al estudiante.")
        
        if metrics["asistencia"] < 80:
            intentions.append("👥 Sugerir intervención de Trabajo Social por ausentismo.")
            
        if metrics["tareas_no_entregadas"] >= 4:
            intentions.append("📚 Asignar taller de regularización y hábitos de estudio.")

        if not intentions:
            intentions.append("✅ Estudiante con buen desempeño. Mantener seguimiento estándar.")

        return intentions