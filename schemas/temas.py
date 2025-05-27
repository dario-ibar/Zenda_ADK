
from pydantic import BaseModel
from typing import Optional

class TemaModel(BaseModel):
    id_tema: int
    tema: str
    descripcion_tema: str
    aplica: bool
    grupo_tema: Optional[str]
    prio: Optional[int]
