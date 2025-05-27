
from pydantic import BaseModel
from datetime import datetime

class PautaModel(BaseModel):
    codigo: str
    categ: str
    relev: int
    pauta: str
    cuando: str
    etapa: str
    keywords: str
    semantica: str
    accion: str
    para: str
    como: str
    marcadores: str
    created_at: datetime
