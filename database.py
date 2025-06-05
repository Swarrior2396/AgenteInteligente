import json
import os
from typing import List, Dict, Optional
from models import Appointment, Doctor

class SimpleDatabase:
    """Base de datos simple usando archivos JSON"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.appointments_file = os.path.join(data_dir, "appointments.json")
        self.doctors_file = os.path.join(data_dir, "doctors.json")
        
        # Crear directorio si no existe
        os.makedirs(data_dir, exist_ok=True)
        
        # Inicializar archivos si no existen
        self._initialize_files()
    
    def _initialize_files(self):
        """Inicializa los archivos de datos"""
        if not os.path.exists(self.doctors_file):
            initial_doctors = [
                {
                    "id": 1,
                    "name": "Dr. María González",
                    "specialty": "Medicina General",
                    "available": True
                },
                {
                    "id": 2,
                    "name": "Dr. Carlos Rodríguez", 
                    "specialty": "Cirugía",
                    "available": True
                },
                {
                    "id": 3,
                    "name": "Dr. Ana Martínez",
                    "specialty": "Nutricionista",
                    "available": True
                },
                {
                    "id": 4,
                    "name": "Dr. Luis Fernández",
                    "specialty": "Cardiología", 
                    "available": True
                }
            ]
            self._save_json(self.doctors_file, initial_doctors)
        
        if not os.path.exists(self.appointments_file):
            self._save_json(self.appointments_file, [])
    
    def _load_json(self, file_path: str) -> List[Dict]:
        """Carga datos desde archivo JSON"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_json(self, file_path: str, data: List[Dict]):
        """Guarda datos en archivo JSON"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_doctors(self) -> List[Dict]:
        """Obtiene todos los doctores"""
        return self._load_json(self.doctors_file)
    
    def get_available_doctors(self) -> List[Dict]:
        """Obtiene doctores disponibles"""
        doctors = self.get_doctors()
        return [d for d in doctors if d.get('available', True)]
    
    def get_appointments(self) -> List[Dict]:
        """Obtiene todas las citas"""
        return self._load_json(self.appointments_file)
    
    def get_user_appointments(self, chat_id: int) -> List[Dict]:
        """Obtiene citas de un usuario específico"""
        appointments = self.get_appointments()
        return [apt for apt in appointments if apt.get('chat_id') == chat_id]
    
    def save_appointment(self, appointment: Dict) -> bool:
        """Guarda una nueva cita"""
        try:
            appointments = self.get_appointments()
            appointments.append(appointment)
            self._save_json(self.appointments_file, appointments)
            return True
        except Exception as e:
            print(f"Error saving appointment: {e}")
            return False
    
    def get_doctor_by_id(self, doctor_id: int) -> Optional[Dict]:
        """Obtiene un doctor por ID"""
        doctors = self.get_doctors()
        return next((d for d in doctors if d['id'] == doctor_id), None)

# Instancia global de la base de datos
db = SimpleDatabase()
