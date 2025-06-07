from pydantic import BaseModel
from datetime import datetime

class TemaEspecialidadModel(BaseModel):
    id: int
    fk_tema: int
    fk_especialidad: int
    prio_tema_rela: int
    created_at: datetime