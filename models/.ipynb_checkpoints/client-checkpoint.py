from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime, date
from uuid import UUID
from enum import Enum

# Enum para el género del cliente (F, M, X)
class GenderType(str, Enum):
    """
    Tipos de género permitidos para el cliente: F (Femenino), M (Masculino), X (Otro/No especificado).
    """
    FEMALE = "F"
    MALE = "M"
    OTHER = "X"

class Client(BaseModel):
    """
    Representa un registro de cliente en la tabla 'clientes' de Supabase.
    Almacena información personal, preferencias y referencia al resumen acumulativo del historial.
    """
    id: UUID = Field(..., description="Unique identifier for the client. Primary key.")
    created_at: datetime = Field(..., description="Timestamp when the client record was created (UTC with timezone).")
    name: str = Field(..., description="Full name of the client.")
    email: Optional[str] = Field(None, description="Email address of the client. Used for notifications or account recovery.")
    phone_number: Optional[str] = Field(None, description="Phone number of the client. Used for contact.")
    birthdate: Optional[date] = Field(None, description="Client's date of birth.")
    gender: Optional[GenderType] = Field(None, description="Client's gender: 'F' for Female, 'M' for Male, 'X' for Other/Not Specified.")
    preferences: Optional[Dict[str, Any]] = Field(None, description="JSONB field storing client preferences (e.g., communication style, notification settings).")
    language: Optional[str] = Field(None, description="Preferred language of communication for the client.")
    current_goal: Optional[str] = Field(None, description="The primary goal the client is currently working on with Zenda.")
    last_session_summary_id: Optional[UUID] = Field(None, description="Foreign key to the last **acumulated** session summary related to this client, for quick access to the most recent context.")
    context_cache_id: Optional[UUID] = Field(None, description="ID of the associated context cache entry in Vertex AI.")