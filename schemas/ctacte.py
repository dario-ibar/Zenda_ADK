
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class CtacteModel(BaseModel):
    id: int
    id_cliente: UUID
    timestamp: datetime
    tipo: str
    moneda: str
    monto: float
    tokens: int
    cpte_nro: Optional[str]
    origen: Optional[str]
    detalle: Optional[str]
    saldo_post: Optional[float]
