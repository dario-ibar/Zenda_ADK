
from pydantic import BaseModel

class EspecialidadModel(BaseModel):
    id_especialidad: int
    cod_esp: str
    especialidad: str
    disciplina: str
    rama: str
    enfoque: str
    prioridad: int
