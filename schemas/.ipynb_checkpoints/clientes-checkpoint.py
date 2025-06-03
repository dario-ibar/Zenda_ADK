
from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from uuid import UUID
from datetime import date, datetime

class ClienteModel(BaseModel):
    id_cliente: UUID
    alias: str
    pais: Optional[str]
    genero: Literal['M', 'F', 'X']
    fecha_nacimiento: date
    email: Optional[EmailStr]
    whatsapp: Optional[str]
    mail_trastorno: Optional[str]
    canal: Optional[str]
    cod_mktg: Optional[str]
    fecha_alta: datetime
    estado: Optional[str]
    preferencias: Optional[dict]
    codigo_personal: Optional[str]
    ash: UUID
    modo_test: bool
