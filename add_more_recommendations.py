# Script para agregar más recomendaciones predefinidas

ADDITIONAL_RECOMMENDATIONS = {
    ("perro", "Cirugía"): """
🎒 **Preparación y qué traer:**
• Ayuno completo 12 horas antes
• Cartilla de vacunación actualizada
• Resultados de análisis pre-quirúrgicos
• Collar isabelino (si no lo proporciona la clínica)

🐾 **Cuidados previos con la mascota:**
• Baño 2-3 días antes de la cirugía
• Ejercicio ligero días previos
• Evita estrés y cambios de rutina
• Retira agua 2 horas antes

⚠️ **Señales de alerta a observar:**
• Fiebre o temperatura elevada
• Vómitos o diarrea
• Heridas o infecciones en la piel
• Problemas respiratorios

💡 **Consejos para reducir estrés:**
• Mantén ambiente tranquilo en casa
• Evita visitas o ruidos fuertes
• Prepara área de recuperación post-cirugía
• Ten mantas limpias disponibles

📝 **Información importante para el veterinario:**
• Reacciones previas a anestesia
• Medicamentos actuales
• Alergias conocidas
• Historial quirúrgico anterior
    """,
    
    ("gato", "Cirugía"): """
🎒 **Preparación y qué traer:**
• Ayuno 12 horas (agua hasta 2h antes)
• Transportín limpio y seguro
• Manta familiar para recuperación
• Cartilla de vacunación completa

🐾 **Cuidados previos con la mascota:**
• Mantén en casa 24-48 horas antes
• Limpia caja de arena completamente
• Observa comportamiento y apetito
• Evita estrés adicional

⚠️ **Señales de alerta a observar:**
• Pérdida total de apetito
• Letargo extremo
• Problemas respiratorios
• Fiebre o temblores

💡 **Consejos para reducir estrés:**
• Usa feromonas calmantes
• Prepara habitación tranquila para recuperación
• Ten caja de arena extra limpia
• Mantén temperatura ambiente estable

📝 **Información importante para el veterinario:**
• Reacciones a medicamentos previos
• Comportamiento bajo estrés
• Preferencias alimenticias
• Contacto con otros gatos
    """,
    
    ("perro", "Emergencia"): """
🎒 **Preparación y qué traer:**
• Correa resistente y collar
• Historial médico disponible
• Lista de síntomas observados
• Método de pago para emergencias

🐾 **Cuidados previos con la mascota:**
• Mantén calma para no transmitir estrés
• No administres medicamentos humanos
• Observa y anota síntomas específicos
• Mantén hidratado si puede beber

⚠️ **Señales de alerta críticas:**
• Dificultad respiratoria severa
• Convulsiones o pérdida de conciencia
• Sangrado abundante
• Vómitos con sangre

💡 **Consejos para la emergencia:**
• Llama antes de llegar si es posible
• Transporta con cuidado y seguridad
• Ten a mano número de emergencias
• Mantén vías respiratorias despejadas

📝 **Información crítica para el veterinario:**
• Hora exacta de inicio de síntomas
• Posible causa (envenenamiento, accidente)
• Medicamentos recientes
• Cambios súbitos en comportamiento
    """,
    
    ("conejo", "Vacunación"): """
🎒 **Preparación y qué traer:**
• Transportín con base antideslizante
• Cartilla de vacunación anterior
• Heno fresco para el viaje
• Historial de reacciones alérgicas

🐾 **Cuidados previos con la mascota:**
• Mantén dieta normal hasta la cita
• Observa producción de heces 24h antes
• Evita cambios en el ambiente
• Asegúrate de que esté hidratado

⚠️ **Señales de alerta a observar:**
• Disminución en apetito
• Heces anormales o ausentes
• Letargo o inactividad
• Respiración acelerada

💡 **Consejos para reducir estrés:**
• Transportín con material familiar
• Viaje corto y suave
• Evita ruidos fuertes
• Mantén temperatura estable

📝 **Información importante para el veterinario:**
• Dieta específica y horarios
• Contacto con otros conejos
• Vida interior vs exterior
• Reacciones a vacunas previas
    """,
}

def update_recommendations_database():
    """Función para actualizar la base de datos de recomendaciones"""
    # Esta función se puede usar para agregar más recomendaciones
    return ADDITIONAL_RECOMMENDATIONS

if __name__ == "__main__":
    print("Recomendaciones adicionales disponibles:")
    for key, recommendation in ADDITIONAL_RECOMMENDATIONS.items():
        print(f"\n{key[0].title()} - {key[1]}:")
        print(recommendation[:100] + "...")
