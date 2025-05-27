
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class SesionModel(BaseModel):
    id_sesion: UUID
    id_cliente: UUID
    fecha_inicio: datetime
    fecha_fin: Optional[datetime]
    modo_asistencia: Optional[str]
    modo_comunicacion: Optional[str]
    finalizo_ok: Optional[bool]
    uso_tt: Optional[str]
    tokens_total: Optional[int]
    tkn_in: Optional[int]
    tkn_out: Optional[int]
    tokens_por_minuto: Optional[float]
    observaciones: Optional[str]
    comentario_usuario: Optional[str]
    usd_costo: Optional[float]
    usd_costo_min: Optional[float]
    usd_fact: Optional[float]
    duracion_minutos: Optional[float]
    historical_summary: Optional[str]
    csat: Optional[float]
    tipo_falla_mem: Optional[List[str]]
    fallas_memoria: Optional[int]
    adherencia: Optional[float]
    efectividad: Optional[float]
    q: Optional[float]
    qresumen: Optional[float]
    qa_labels: Optional[List[str]]
    comentario_qa: Optional[str]
    llm_qa_usado: Optional[str]
