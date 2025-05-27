
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MarketingModel(BaseModel):
    cod_mktg: str
    canal_tipo: str
    mktg_info: Optional[str]
    comision: Optional[float]
    moneda: Optional[str]
    min_liq: Optional[float]
    fecha_desde: Optional[datetime]
    fecha_hasta: Optional[datetime]
    created_at: datetime
