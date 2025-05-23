# tools/bitacora_tool.py
from typing import List, Optional, Literal
from datetime import datetime
import json

# --- Placeholder para el modelo Pydantic BitacoraEntry (se reemplazará por el real) ---
# Asumimos que BitacoraEntry será una clase que podemos convertir a dict
class BitacoraEntry:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    def to_dict(self):
        # Asegurar conversión de tipos para el log (ej. datetime a str)
        data = {}
        for k,v in self.__dict__.items():
            if isinstance(v, datetime):
                data[k] = v.isoformat()
            else:
                data[k] = v
        return data

def bitacora_tool(session_id: str, client_id: str, actor: str, tipo: str, texto: str,
                  guia: Optional[List[str]] = None, tt: Optional[Literal["S", "F"]] = None,
                  canal: Optional[Literal["T", "S"]] = None) -> bool:
    """
    Registra un evento en la bitácora de la sesión.
    Esta es una FunctionTool que los agentes usarán para loguear.
    """
    print(f"\n[TOOL]: bitacora_tool invocada - Sesion: {session_id}, Cliente: {client_id}")
    entry_data = {
        "id_cliente": client_id,
        "id_sesion": session_id,
        "timestamp": datetime.now(),
        "actor": actor,
        "tipo": tipo,
        "texto": texto,
        "guia": guia,
        "tt": tt,
        "canal": canal
    }
    # Validar con Pydantic si el modelo BitacoraEntry real estuviera aquí
    # entry = BitacoraEntry(**entry_data) 

    print(f"       -> BITACORA REGISTRO: {json.dumps(entry_data, indent=2)}")
    # TODO: Implementar la lógica REAL de persistencia a Supabase (Paso 7)
    return True
