import os
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import logging

# Cargar variables de entorno
from dotenv import load_dotenv
load_dotenv()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Verificar variables de entorno
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TELEGRAM_BOT_TOKEN:
    logger.error("❌ TELEGRAM_BOT_TOKEN no está configurado en el archivo .env")
    exit(1)

@dataclass
class Doctor:
    id: int
    name: str
    specialty: str
    available: bool = True

@dataclass
class AppointmentData:
    owner_name: Optional[str] = None
    pet_name: Optional[str] = None
    pet_type: Optional[str] = None
    appointment_type: Optional[str] = None
    selected_doctor: Optional[str] = None
    selected_doctor_id: Optional[int] = None
    selected_date: Optional[str] = None
    selected_time: Optional[str] = None

@dataclass
class ConversationState:
    step: str = "greeting"
    data: AppointmentData = None
    
    def __post_init__(self):
        if self.data is None:
            self.data = AppointmentData()

# Base de datos simulada
doctors = [
    Doctor(1, "Dr. María González", "Medicina General"),
    Doctor(2, "Dr. Carlos Rodríguez", "Cirugía"),
    Doctor(3, "Dr. Ana Martínez", "Dermatología"),
    Doctor(4, "Dr. Luis Fernández", "Cardiología"),
    Doctor(5, "Dr. Patricia Morales", "Oftalmología"),
    Doctor(6, "Dr. Roberto Silva", "Traumatología"),
]

# Tipos de citas disponibles
appointment_types = [
    {"id": "consulta_general", "name": "Consulta General", "description": "Revisión médica general"},
    {"id": "vacunacion", "name": "Vacunación", "description": "Aplicación de vacunas"},
    {"id": "cirugia", "name": "Cirugía", "description": "Procedimientos quirúrgicos"},
    {"id": "emergencia", "name": "Emergencia", "description": "Atención de urgencia"},
    {"id": "control", "name": "Control Post-operatorio", "description": "Seguimiento después de cirugía"},
    {"id": "dermatologia", "name": "Dermatología", "description": "Problemas de piel y pelo"},
    {"id": "oftalmologia", "name": "Oftalmología", "description": "Problemas oculares"},
    {"id": "traumatologia", "name": "Traumatología", "description": "Lesiones y fracturas"},
]

appointments = []
conversation_states: Dict[int, ConversationState] = {}

# Recomendaciones predefinidas por tipo de mascota y cita
RECOMMENDATIONS_DATABASE = {
    ("perro", "Consulta General"): """
🎒 **Preparación y qué traer:**
• Cartilla de vacunación actualizada
• Correa y collar seguros
• Lista de medicamentos actuales
• Muestra de heces reciente (si es posible)

🐾 **Cuidados previos con la mascota:**
• Mantén su rutina normal de alimentación
• Ejercicio ligero antes de la cita
• Baño 2-3 días antes (no el mismo día)

⚠️ **Señales de alerta a observar:**
• Cambios en apetito o comportamiento
• Vómitos o diarrea
• Letargo inusual
• Dificultad para respirar

💡 **Consejos para reducir estrés:**
• Llega 10 minutos antes de la cita
• Mantén calma y confianza
• Trae su juguete favorito
• Usa refuerzo positivo con premios

📝 **Información importante para el veterinario:**
• Cambios recientes en comportamiento
• Historial de enfermedades previas
• Reacciones a medicamentos
• Hábitos alimenticios y de ejercicio
    """,
    
    ("perro", "Vacunación"): """
🎒 **Preparación y qué traer:**
• Cartilla de vacunación anterior
• Correa resistente y collar con identificación
• Premios pequeños para recompensar
• Historial de reacciones alérgicas (si las hay)

🐾 **Cuidados previos con la mascota:**
• Asegúrate de que esté completamente sano
• No bañes 24 horas antes
• Alimentación normal hasta 2 horas antes
• Evita ejercicio intenso el día anterior

⚠️ **Señales de alerta a observar:**
• Fiebre o temperatura elevada
• Vómitos o diarrea recientes
• Letargo o debilidad
• Reacciones alérgicas previas a vacunas

💡 **Consejos para reducir estrés:**
• Socialización previa con otros perros
• Mantén rutina normal antes de la cita
• Usa transportín si es un cachorro
• Evita lugares con muchos animales antes

📝 **Información importante para el veterinario:**
• Fecha de última vacunación
• Reacciones adversas anteriores
• Medicamentos actuales
• Exposición a otros animales enfermos
    """,
    
    ("gato", "Consulta General"): """
🎒 **Preparación y qué traer:**
• Transportín seguro y cómodo
• Cartilla de vacunación
• Manta familiar para reducir estrés
• Muestra de orina si es posible

🐾 **Cuidados previos con la mascota:**
• Mantén en casa 24 horas antes
• No cambies su dieta
• Limpia la caja de arena
• Observa comportamiento y apetito

⚠️ **Señales de alerta a observar:**
• Cambios en uso de caja de arena
• Pérdida de apetito
• Esconderse más de lo normal
• Vocalización excesiva

💡 **Consejos para reducir estrés:**
• Usa feromonas calmantes en transportín
• Cubre el transportín con manta
• Evita ruidos fuertes durante traslado
• Mantén temperatura estable

📝 **Información importante para el veterinario:**
• Hábitos de caja de arena
• Comportamiento social con otros gatos
• Preferencias alimenticias
• Lugares favoritos para esconderse
    """,
    
    ("gato", "Vacunación"): """
🎒 **Preparación y qué traer:**
• Transportín con ventilación adecuada
• Cartilla de vacunación completa
• Toalla o manta familiar
• Lista de medicamentos actuales

🐾 **Cuidados previos con la mascota:**
• Mantén en ayunas 12 horas antes si es necesario
• Observa comportamiento 48 horas previas
• Evita estrés adicional en casa
• Mantén rutina de juego normal

⚠️ **Señales de alerta a observar:**
• Fiebre o letargo
• Pérdida de apetito
• Vómitos o diarrea
• Comportamiento agresivo inusual

💡 **Consejos para reducir estrés:**
• Acostumbra al transportín días antes
• Usa spray de feromonas
• Mantén viaje corto y suave
• Habla con voz calmada

📝 **Información importante para el veterinario:**
• Reacciones a vacunas anteriores
• Contacto con gatos callejeros
• Vida interior vs exterior
• Cambios recientes en comportamiento
    """,
    
    ("conejo", "Consulta General"): """
🎒 **Preparación y qué traer:**
• Transportín con base sólida
• Heno fresco y pellets
• Historial médico completo
• Muestra de heces recientes

🐾 **Cuidados previos con la mascota:**
• Mantén dieta constante
• Observa producción de cecótrofos
• Revisa dientes y uñas
• Pesa regularmente

⚠️ **Señales de alerta a observar:**
• Disminución en producción de heces
• Pérdida de apetito
• Letargo o inactividad
• Problemas dentales

💡 **Consejos para reducir estrés:**
• Transportín con material familiar
• Evita cambios bruscos de temperatura
• Mantén ambiente tranquilo
• No manipules excesivamente

📝 **Información importante para el veterinario:**
• Dieta específica y cantidad
• Hábitos de ejercicio
• Interacción con otros conejos
• Historial reproductivo
    """,
}

def get_available_dates() -> List[Dict]:
    """Obtiene las próximas 3 fechas de días hábiles"""
    dates = []
    today = datetime.now()
    business_days = 0
    current_date = today
    
    while business_days < 3:
        current_date += timedelta(days=1)
        if current_date.weekday() < 5:
            dates.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'display_date': current_date.strftime('%A, %d de %B de %Y'),
                'slots': ['09:00', '10:00', '11:00', '14:00', '15:00', '16:00']
            })
            business_days += 1
    
    return dates

def get_appointment_recommendations(pet_type: str, appointment_type: str) -> str:
    """Obtiene recomendaciones predefinidas basadas en tipo de mascota y cita"""
    
    # Buscar recomendación específica
    key = (pet_type.lower(), appointment_type)
    if key in RECOMMENDATIONS_DATABASE:
        return RECOMMENDATIONS_DATABASE[key]
    
    # Buscar por tipo de mascota general
    general_keys = [k for k in RECOMMENDATIONS_DATABASE.keys() if k[0] == pet_type.lower()]
    if general_keys:
        return RECOMMENDATIONS_DATABASE[general_keys[0]]
    
    # Recomendación genérica
    return f"""
🎒 **Preparación general para {pet_type}:**
• Trae cartilla de vacunación
• Transportín o correa segura
• Lista de medicamentos actuales
• Historial médico disponible

🐾 **Cuidados previos:**
• Mantén rutina normal de alimentación
• Observa comportamiento 24h antes
• Evita estrés adicional
• Asegúrate de que esté hidratado

⚠️ **Señales de alerta:**
• Cambios en apetito
• Letargo inusual
• Vómitos o diarrea
• Comportamiento anormal

💡 **Consejos generales:**
• Llega puntual a la cita
• Mantén calma durante la visita
• Prepara preguntas para el veterinario
• Trae método de pago

📝 **Información importante:**
• Síntomas actuales
• Medicamentos en uso
• Cambios recientes
• Preguntas específicas
    """

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /start"""
    chat_id = update.effective_chat.id
    conversation_states[chat_id] = ConversationState()
    
    welcome_message = """
🏥 ¡Bienvenido a PetHealth! 

Soy tu asistente virtual y estoy aquí para ayudarte a agendar una cita para tu mascota.

Te proporcionaré recomendaciones personalizadas basadas en el tipo de cita y tu mascota.

Para comenzar, por favor dime tu nombre completo.
    """
    
    await update.message.reply_text(welcome_message)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Maneja los mensajes de texto"""
    chat_id = update.effective_chat.id
    user_message = update.message.text
    
    if chat_id not in conversation_states:
        conversation_states[chat_id] = ConversationState()
    
    state = conversation_states[chat_id]
    
    if state.step == "greeting":
        state.data.owner_name = user_message
        state.step = "ask_pet_name"
        response = f"Mucho gusto, {user_message}! 🙂\n\n¿Cómo se llama tu mascota?"
        
    elif state.step == "ask_pet_name":
        state.data.pet_name = user_message
        state.step = "ask_pet_type"
        response = f"¡Qué lindo nombre! ¿Qué tipo de mascota es {user_message}?\n\n(Por ejemplo: perro, gato, conejo, etc.)"
        
    elif state.step == "ask_pet_type":
        state.data.pet_type = user_message
        state.step = "ask_appointment_type"
        response = f"Perfecto! {state.data.pet_name} es un {user_message} muy especial. 🐾\n\n¿Qué tipo de cita necesitas?"
        
        # Mostrar tipos de citas
        keyboard = []
        for apt_type in appointment_types:
            keyboard.append([InlineKeyboardButton(
                f"{apt_type['name']}", 
                callback_data=f"apt_type_{apt_type['id']}"
            )])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(response, reply_markup=reply_markup)
        return
        
    else:
        response = "Por favor, usa los botones para continuar con el proceso de agendamiento."
    
    await update.message.reply_text(response)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Maneja los callbacks de los botones"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat_id
    callback_data = query.data
    
    if chat_id not in conversation_states:
        await query.edit_message_text("Error: Sesión expirada. Usa /start para comenzar de nuevo.")
        return
    
    state = conversation_states[chat_id]
    
    if callback_data.startswith("apt_type_"):
        appointment_type_id = callback_data.split("_", 2)[2]
        appointment_type_info = next((apt for apt in appointment_types if apt['id'] == appointment_type_id), None)
        
        if appointment_type_info:
            state.data.appointment_type = appointment_type_info['name']
            state.step = "show_recommendations"
            
            # Generar recomendaciones predefinidas
            recommendations = get_appointment_recommendations(
                state.data.pet_type, 
                appointment_type_info['name']
            )
            
            response = f"""
✅ **Tipo de cita seleccionada:** {appointment_type_info['name']}

📋 **Recomendaciones personalizadas para {state.data.pet_name}:**

{recommendations}

---

¿Estás listo para continuar con la selección del doctor?
            """
            
            # Botón para continuar
            keyboard = [[InlineKeyboardButton("Continuar con doctores", callback_data="continue_doctors")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(response, reply_markup=reply_markup)
    
    elif callback_data == "continue_doctors":
        state.step = "show_doctors"
        
        response = "Ahora selecciona uno de nuestros doctores disponibles:"
        
        # Mostrar doctores
        keyboard = []
        for doctor in doctors:
            if doctor.available:
                keyboard.append([InlineKeyboardButton(
                    f"{doctor.name} - {doctor.specialty}", 
                    callback_data=f"doctor_{doctor.id}"
                )])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(response, reply_markup=reply_markup)
    
    elif callback_data.startswith("doctor_"):
        doctor_id = int(callback_data.split("_")[1])
        doctor = next((d for d in doctors if d.id == doctor_id), None)
        
        if doctor:
            state.data.selected_doctor = doctor.name
            state.data.selected_doctor_id = doctor_id
            state.step = "show_dates"
            
            response = f"Has seleccionado a {doctor.name} ({doctor.specialty}) 👨‍⚕️\n\nAhora elige una fecha disponible:"
            
            dates = get_available_dates()
            keyboard = []
            for date_info in dates:
                keyboard.append([InlineKeyboardButton(
                    date_info['display_date'], 
                    callback_data=f"date_{date_info['date']}"
                )])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(response, reply_markup=reply_markup)
    
    elif callback_data.startswith("date_"):
        selected_date = callback_data.split("_")[1]
        dates = get_available_dates()
        date_info = next((d for d in dates if d['date'] == selected_date), None)
        
        if date_info:
            state.data.selected_date = selected_date
            state.step = "show_times"
            
            response = f"Fecha seleccionada: {date_info['display_date']} 📅\n\nElige un horario disponible:"
            
            keyboard = []
            for time_slot in date_info['slots']:
                keyboard.append([InlineKeyboardButton(
                    time_slot, 
                    callback_data=f"time_{time_slot}"
                )])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(response, reply_markup=reply_markup)
    
    elif callback_data.startswith("time_"):
        selected_time = callback_data.split("_")[1]
        state.data.selected_time = selected_time
        
        # Crear cita
        appointment = {
            'id': len(appointments) + 1,
            'owner_name': state.data.owner_name,
            'pet_name': state.data.pet_name,
            'pet_type': state.data.pet_type,
            'appointment_type': state.data.appointment_type,
            'doctor_id': state.data.selected_doctor_id,
            'doctor_name': state.data.selected_doctor,
            'date': state.data.selected_date,
            'time': selected_time,
            'created_at': datetime.now().isoformat(),
            'chat_id': chat_id
        }
        
        appointments.append(appointment)
        
        # Limpiar estado
        del conversation_states[chat_id]
        
        # Mensaje de confirmación
        confirmation_message = f"""
🎉 ¡Cita confirmada exitosamente!

📋 **Detalles de la cita:**
👤 Dueño: {appointment['owner_name']}
🐾 Mascota: {appointment['pet_name']} ({appointment['pet_type']})
📝 Tipo de cita: {appointment['appointment_type']}
👨‍⚕️ Doctor: {appointment['doctor_name']}
📅 Fecha: {datetime.strptime(appointment['date'], '%Y-%m-%d').strftime('%A, %d de %B de %Y')}
🕐 Hora: {appointment['time']}
🆔 ID Cita: #{appointment['id']}

💡 **Recordatorio:** Revisa las recomendaciones que te proporcionamos para prepararte mejor para la cita.

Te esperamos en PetHealth. ¡Gracias por confiar en nosotros! 🏥

Para agendar otra cita, usa /start
        """
        
        await query.edit_message_text(confirmation_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /help"""
    help_text = """
🏥 **PetHealth Bot - Ayuda**

**Comandos disponibles:**
/start - Iniciar proceso de agendamiento
/help - Mostrar esta ayuda
/citas - Ver tus citas programadas
/tipos - Ver tipos de citas disponibles

**¿Cómo funciona?**
1. Usa /start para comenzar
2. Proporciona tu nombre
3. Nombre de tu mascota
4. Tipo de mascota
5. Selecciona tipo de cita
6. Recibe recomendaciones personalizadas
7. Selecciona doctor
8. Elige fecha y hora
9. ¡Listo! Recibirás confirmación

**Características:**
✨ Recomendaciones personalizadas
✨ Consejos específicos por tipo de mascota y cita
✨ Preparación previa a la consulta
✨ Funciona sin conexión a internet adicional

**Soporte:**
Si tienes problemas, contacta a nuestro equipo de soporte.
    """
    
    await update.message.reply_text(help_text)

async def appointment_types_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /tipos - Mostrar tipos de citas disponibles"""
    message = "📋 **Tipos de citas disponibles:**\n\n"
    
    for apt_type in appointment_types:
        message += f"🔸 **{apt_type['name']}**\n   {apt_type['description']}\n\n"
    
    message += "Para agendar una cita, usa /start"
    
    await update.message.reply_text(message)

async def my_appointments(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /citas - Mostrar citas del usuario"""
    chat_id = update.effective_chat.id
    user_appointments = [apt for apt in appointments if apt['chat_id'] == chat_id]
    
    if not user_appointments:
        await update.message.reply_text("No tienes citas programadas. Usa /start para agendar una.")
        return
    
    message = "📅 **Tus citas programadas:**\n\n"
    
    for apt in user_appointments:
        date_formatted = datetime.strptime(apt['date'], '%Y-%m-%d').strftime('%d/%m/%Y')
        message += f"""
🆔 Cita #{apt['id']}
🐾 {apt['pet_name']} ({apt['pet_type']})
📝 Tipo: {apt.get('appointment_type', 'No especificado')}
👨‍⚕️ {apt['doctor_name']}
📅 {date_formatted} a las {apt['time']}
---
        """
    
    await update.message.reply_text(message)

def main() -> None:
    """Función principal"""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN no está configurado")
        return
    
    # Crear aplicación
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Agregar handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("citas", my_appointments))
    application.add_handler(CommandHandler("tipos", appointment_types_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(handle_callback))
    
    # Ejecutar bot
    logger.info("🏥 Bot PetHealth iniciado (Versión Offline)...")
    logger.info("✅ Funcionando con recomendaciones predefinidas")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
