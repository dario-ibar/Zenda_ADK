
from pydantic import BaseModel
from typing import Optional, Literal
from uuid import UUID
from datetime import datetime

class BitacoraModel(BaseModel):
    id: int
    session_id: UUID
    user_id: UUID
    invocation_id: Optional[str]
    event_id: Optional[str]
    created_at: datetime
    actor: Literal['user', 'zenda', 'dt', 'qa', 'system']
    event_type: Literal['input', 'respuesta', 'pauta_aplicada', 'alerta', 'interrupcion']
    content_text: Optional[str]
    content_raw: Optional[dict]
    pautas_codigos: Optional[str]
    status: Literal['ok', 'error', 'sin_respuesta', 'incompleto', 'tool_fail', 'ignored']
    tags: Optional[str]
    metadata: Optional[dict]
