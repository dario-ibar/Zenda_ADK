
from pydantic import BaseModel
from typing import Optional, Literal
from uuid import UUID
from datetime import datetime

class QaModel(BaseModel):
    id: int
    session_id: UUID
    evento_id: int
    codigo_pauta: str
    tipo_evaluacion: Literal['ad', 'ef']
    evaluacion: Literal[1, -1]
    impacto: int
    detalle: Optional[str]
    llm: Optional[str]
    metadata: Optional[dict]
    created_at: datetime
