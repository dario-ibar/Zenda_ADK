from google.adk.tools import FunctionTool
from typing import Optional, List, Literal
from datetime import datetime
from schemas import BitacoraModel
import json

def bitacora_function(session_id: str, client_id: str, actor: str, tipo: str, texto: str,
                     guia: Optional[List[str]] = None, tt: Optional[Literal["S", "F"]] = None,
                     canal: Optional[Literal["T", "S"]] = None) -> bool:
    """
    Registra un evento en la bitácora de la sesión.
    Esta es una FunctionTool que los agentes usarán para loguear.
    
    Args:
        session_id: ID de la sesión
        client_id: ID del cliente 
        actor: Quién generó el evento (cliente, zenda, dt, qa, sistema)
        tipo: Tipo de entrada (msg, resumen, op, ent, emo, tec, fmem)
        texto: Contenido principal
        guia: Códigos de guía aplicados (opcional)
        tt: Si se usó Think Tool - S/F (opcional)
        canal: Canal de comunicación - T/S (opcional)
        
    Returns:
        bool: True si el registro fue exitoso
    """
    print(f"\n[BITACORA_TOOL]: Sesion={session_id}, Cliente={client_id}")
    print(f"                  Actor={actor}, Tipo={tipo}")
    print(f"                  Texto='{texto[:50]}...'")
    
    # Preparar datos para BitacoraModel
    entry_data = {
        "session_id": session_id,
        "user_id": client_id,
        "created_at": datetime.now(),
        "actor": actor,
        "event_type": tipo,
        "content_text": texto,
        "pautas_codigos": ",".join(guia) if guia else None,
        "status": "ok",
        "tags": ",".join([tt] if tt else []),
        "metadata": {
            "canal": canal,
            "tt": tt,
            "guia": guia
        }
    }
    
    # TODO: Implementar persistencia real a Supabase
    # bitacora_entry = BitacoraModel(**entry_data)
    # supabase.table('bitacora').insert(bitacora_entry.model_dump()).execute()
    
    print(f"       -> BITACORA REGISTRADO: {json.dumps(entry_data, default=str, indent=2)}")
    return True

# Crear FunctionTool ADK
bitacora_tool = FunctionTool(bitacora_function)
