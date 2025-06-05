from datetime import datetime, timedelta
from typing import List, Dict
import locale

# Configurar locale para español (opcional)
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except:
    pass

def get_available_dates(days_ahead: int = 3) -> List[Dict]:
    """
    Obtiene las próximas fechas de días hábiles disponibles
    
    Args:
        days_ahead: Número de días hábiles a obtener
    
    Returns:
        Lista de diccionarios con información de fechas
    """
    dates = []
    today = datetime.now()
    business_days = 0
    current_date = today
    
    while business_days < days_ahead:
        current_date += timedelta(days=1)
        # Excluir sábados (5) y domingos (6)
        if current_date.weekday() < 5:
            dates.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'display_date': format_date_spanish(current_date),
                'weekday': current_date.strftime('%A'),
                'slots': get_available_time_slots()
            })
            business_days += 1
    
    return dates

def format_date_spanish(date: datetime) -> str:
    """Formatea una fecha en español"""
    days = {
        'Monday': 'Lunes',
        'Tuesday': 'Martes', 
        'Wednesday': 'Miércoles',
        'Thursday': 'Jueves',
        'Friday': 'Viernes',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    }
    
    months = {
        'January': 'Enero', 'February': 'Febrero', 'March': 'Marzo',
        'April': 'Abril', 'May': 'Mayo', 'June': 'Junio',
        'July': 'Julio', 'August': 'Agosto', 'September': 'Septiembre',
        'October': 'Octubre', 'November': 'Noviembre', 'December': 'Diciembre'
    }
    
    day_name = days.get(date.strftime('%A'), date.strftime('%A'))
    month_name = months.get(date.strftime('%B'), date.strftime('%B'))
    
    return f"{day_name}, {date.day} de {month_name} de {date.year}"

def get_available_time_slots() -> List[str]:
    """Obtiene los horarios disponibles"""
    morning_slots = ['09:00', '09:30', '10:00', '10:30', '11:00', '11:30']
    afternoon_slots = ['14:00', '14:30', '15:00', '15:30', '16:00', '16:30']
    
    return morning_slots + afternoon_slots

def validate_pet_type(pet_type: str) -> bool:
    """Valida si el tipo de mascota es válido"""
    valid_types = [
        'perro', 'gato', 'conejo', 'hamster', 'cobayo', 'hurón',
        'ave', 'pájaro', 'pez', 'reptil', 'tortuga', 'iguana'
    ]
    
    return pet_type.lower() in valid_types

def generate_appointment_id() -> str:
    """Genera un ID único para la cita"""
    return f"PH{datetime.now().strftime('%Y%m%d%H%M%S')}"
