from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime

@dataclass
class Doctor:
    id: int
    name: str
    specialty: str
    available: bool = True
    schedule: Optional[List[str]] = None

@dataclass
class Appointment:
    id: int
    owner_name: str
    pet_name: str
    pet_type: str
    doctor_id: int
    doctor_name: str
    date: str
    time: str
    created_at: str
    chat_id: int
    status: str = "confirmed"

@dataclass
class AppointmentData:
    owner_name: Optional[str] = None
    pet_name: Optional[str] = None
    pet_type: Optional[str] = None
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
