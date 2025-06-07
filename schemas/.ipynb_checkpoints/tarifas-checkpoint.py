
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TarifaModel(BaseModel):
    id: int
    modelo_llm: str
    origen: str
    unidad: str
    costo_usd_unitario: float
    precio_usd_unitario: float
    fecha_desde: datetime
    fecha_hasta: Optional[datetime]
    created_at: datetime
