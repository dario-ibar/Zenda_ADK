
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class TokenModel(BaseModel):
    id_token: UUID
    id_cliente: UUID
    id_origen: str
    tokens: int
    fecha: datetime
