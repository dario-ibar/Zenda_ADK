save_context_content = '''from google.adk.function_tool import FunctionTool
from typing import Dict, Any
from datetime import datetime
from schemas import EntidadModel
import uuid

# Simulación de base de datos (TODO: reemplazar por Supabase)
_simulated_entities_db = {}

def save_context_info_function(session_id: str, client_id: str, info_type: str, info_content: str) -> Dict[str, Any]:
    """
    Guarda información muy específica del cliente o muy recurrente (jerga, conceptos)
    como entidad en la base de datos.
    
    Args:
        session_id: ID de la sesión actual
        client_id: ID del cliente asociado
        info_type: Tipo de información ("Jargon", "Concepto", "DatoRelevante")
        info_content: Contenido textual a guardar
        
    Returns:
        Dict[str, Any]: Resultado de la operación con status y entity_id
    """
    print(f"\\n[SAVE_CONTEXT_TOOL]: Guardando contexto para cliente {client_id}")
    print(f"                      Tipo: {info_type}")
    print(f"                      Contenido: '{info_content[:50]}...'")

    new_entity_id = str(uuid.uuid4())
    entity_data = {
        "id_cliente": client_id,
        "tipo_entidad": info_type,
        "nombre_entidad": info_content[:100],
        "datos_entidad": {
            "content": info_content,
            "detected_at": datetime.now().isoformat(),
            "session_id_origen": session_id,
            "auto_detected": True
        },
        "tipo_relacion": "Información",
        "estado": "activo",
        "created_at": datetime.now(),
        "modified_at": datetime.now()
    }
    
    _simulated_entities_db[new_entity_id] = {**entity_data, "id": new_entity_id}
    
    print(f"       -> CONTEXTO GUARDADO: ID {new_entity_id}")
    print(f"          Como entidad tipo '{info_type}'")
    
    return {
        "status": "ok", 
        "entity_id": new_entity_id,
        "message": f"Información guardada como {info_type}"
    }

# Crear FunctionTool ADK
save_context_info_tool = FunctionTool(save_context_info_function)
'''

with open('/home/jupyter/Zenda_ADK/tools/save_context_info_tool.py', 'w') as f:
    f.write(save_context_content)
    
print("✅ save_context_info_tool.py corregido!")