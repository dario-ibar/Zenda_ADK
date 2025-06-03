from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from uuid import UUID

class SessionContext(BaseModel):
    # Identificadores básicos
    id_cliente: UUID
    id_sesion: UUID
    
    # Estado de sesión
    fase_actual: str = "Inicio_Sesion"  # "Inicio_Sesion", "Desarrollo_Sesion", "Cierre_Sesion"
    modo_asistencia: str = "Integral"   # "Integral", "Rotativo", "Especialidad", "Urgente"
    
    # Dirección estratégica (DT)
    guion_dt: Optional[str] = None
    acuerdo_sesion: Optional[str] = None
    criterios: Dict[str, Any] = {}
    pautas_priorizadas: List[str] = []
    
    # Memoria y contexto
    resumen_memoria_larga: Optional[str] = None
    interacciones_recientes: List[Dict[str, Any]] = []
    
    # Configuración de usuario
    preferencias_usuario: Dict[str, Any] = {}
    
    # Especialidades
    especialidad_principal: Optional[str] = None
    especialidades_secundarias: List[str] = []
    
    # Modo rotativo específico
    ciclo_rotativo_actual: Optional[str] = None
    
    # Think Tool
    think_tool_activado: bool = False
    motivo_tt: Optional[str] = None  # "S" (Sensible), "F" (Falla)
    
    class Config:
        # Permitir campos adicionales para extensibilidad
        extra = "allow"
