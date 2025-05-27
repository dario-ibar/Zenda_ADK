
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class EntidadModel(BaseModel):
    id: int
    id_cliente: UUID
    tipo_entidad: str
    nombre_entidad: str
    datos_entidad: Optional[dict]
    tipo_relacion: Optional[str]
    estado: Optional[str]
    created_at: datetime
    modified_at: Optional[datetime]
