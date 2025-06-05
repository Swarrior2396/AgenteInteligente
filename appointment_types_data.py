# Datos detallados de tipos de citas y especialidades

APPOINTMENT_TYPES = [
    {
        "id": "consulta_general",
        "name": "Consulta General",
        "description": "Revisión médica general y chequeo de salud",
        "duration": 30,
        "preparation_time": 15,
        "specialties": ["Medicina General"],
        "common_pets": ["perro", "gato", "conejo", "hamster"]
    },
    {
        "id": "vacunacion",
        "name": "Vacunación",
        "description": "Aplicación de vacunas preventivas",
        "duration": 20,
        "preparation_time": 10,
        "specialties": ["Medicina General"],
        "common_pets": ["perro", "gato", "conejo", "hurón"]
    },
    {
        "id": "cirugia_menor",
        "name": "Cirugía Menor",
        "description": "Procedimientos quirúrgicos ambulatorios",
        "duration": 60,
        "preparation_time": 30,
        "specialties": ["Cirugía"],
        "common_pets": ["perro", "gato"]
    },
    {
        "id": "cirugia_mayor",
        "name": "Cirugía Mayor",
        "description": "Procedimientos quirúrgicos complejos",
        "duration": 120,
        "preparation_time": 60,
        "specialties": ["Cirugía"],
        "common_pets": ["perro", "gato"]
    },
    {
        "id": "emergencia",
        "name": "Emergencia",
        "description": "Atención de urgencia médica",
        "duration": 45,
        "preparation_time": 0,
        "specialties": ["Medicina General", "Cirugía"],
        "common_pets": ["perro", "gato", "conejo", "ave"]
    },
    {
        "id": "control_postoperatorio",
        "name": "Control Post-operatorio",
        "description": "Seguimiento después de cirugía",
        "duration": 25,
        "preparation_time": 10,
        "specialties": ["Cirugía", "Medicina General"],
        "common_pets": ["perro", "gato"]
    },
    {
        "id": "dermatologia",
        "name": "Dermatología",
        "description": "Problemas de piel, pelo y alergias",
        "duration": 40,
        "preparation_time": 20,
        "specialties": ["Dermatología"],
        "common_pets": ["perro", "gato", "conejo"]
    },
    {
        "id": "oftalmologia",
        "name": "Oftalmología",
        "description": "Problemas oculares y de visión",
        "duration": 35,
        "preparation_time": 15,
        "specialties": ["Oftalmología"],
        "common_pets": ["perro", "gato", "conejo"]
    },
    {
        "id": "traumatologia",
        "name": "Traumatología",
        "description": "Lesiones, fracturas y problemas óseos",
        "duration": 50,
        "preparation_time": 25,
        "specialties": ["Traumatología"],
        "common_pets": ["perro", "gato"]
    },
    {
        "id": "cardiologia",
        "name": "Cardiología",
        "description": "Problemas cardíacos y circulatorios",
        "duration": 45,
        "preparation_time": 20,
        "specialties": ["Cardiología"],
        "common_pets": ["perro", "gato"]
    },
    {
        "id": "exoticos",
        "name": "Medicina de Exóticos",
        "description": "Atención para mascotas exóticas",
        "duration": 40,
        "preparation_time": 25,
        "specialties": ["Medicina General"],
        "common_pets": ["ave", "reptil", "hurón", "conejo", "hamster"]
    }
]

PET_SPECIFIC_RECOMMENDATIONS = {
    "perro": {
        "general_tips": [
            "Mantén a tu perro con correa durante la visita",
            "Trae su juguete favorito para reducir ansiedad",
            "Evita alimentarlo 2 horas antes si es cirugía"
        ],
        "behavioral_notes": "Los perros pueden mostrar ansiedad en entornos nuevos"
    },
    "gato": {
        "general_tips": [
            "Usa un transportín seguro y cómodo",
            "Cubre el transportín con una manta para reducir estrés",
            "Evita alimentarlo 12 horas antes si es cirugía"
        ],
        "behavioral_notes": "Los gatos se estresan fácilmente, mantén un ambiente tranquilo"
    },
    "conejo": {
        "general_tips": [
            "Usa un transportín con ventilación adecuada",
            "Trae heno fresco para mantenerlo calmado",
            "Evita cambios bruscos de temperatura"
        ],
        "behavioral_notes": "Los conejos son muy sensibles al estrés y cambios"
    },
    "ave": {
        "general_tips": [
            "Usa una jaula de transporte apropiada",
            "Mantén temperatura estable durante el traslado",
            "Evita ruidos fuertes y movimientos bruscos"
        ],
        "behavioral_notes": "Las aves son muy sensibles a cambios ambientales"
    }
}

def get_appointment_type_by_id(appointment_id: str):
    """Obtiene información detallada de un tipo de cita"""
    return next((apt for apt in APPOINTMENT_TYPES if apt['id'] == appointment_id), None)

def get_recommended_doctors_for_appointment(appointment_type: str, doctors_list: list):
    """Filtra doctores recomendados para un tipo de cita específico"""
    apt_info = get_appointment_type_by_id(appointment_type)
    if not apt_info:
        return doctors_list
    
    recommended_specialties = apt_info.get('specialties', [])
    
    # Filtrar doctores por especialidad
    recommended_doctors = []
    for doctor in doctors_list:
        if doctor.specialty in recommended_specialties:
            recommended_doctors.append(doctor)
    
    # Si no hay doctores específicos, devolver todos los disponibles
    return recommended_doctors if recommended_doctors else doctors_list
