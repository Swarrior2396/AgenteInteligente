import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración del bot
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Configuración de la base de datos (para futuras expansiones)
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///pethealth.db')

# Configuración de horarios
BUSINESS_HOURS = {
    'start': '09:00',
    'end': '17:00',
    'lunch_start': '12:00',
    'lunch_end': '14:00'
}

# Días de la semana (0=Lunes, 6=Domingo)
BUSINESS_DAYS = [0, 1, 2, 3, 4]  # Lunes a Viernes
