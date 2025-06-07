entidades_content = '''from google.adk.tools import FunctionTool
from typing import Dict, Any, Optional
from datetime import datetime
from schemas import EntidadModel
import uuid

# Simulación de base de datos en memoria (TODO: reemplazar por Supabase)
_simulated_entities_db = {}

def entidades_function(session_id: str, id_cliente: str, action: str, 
                      entity_data: Optional[Dict[str, Any]] = None,
                      entity_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Gestiona entidades (personas, organizaciones, jerga, conceptos) en la base de datos.
    
    Args:
        session_id: ID de la sesión actual
        id_cliente: ID del cliente asociado
        action: Acción a realizar ("guardar", "actualizar", "leer", "eliminar")
        entity_data: Datos de la entidad para guardar/actualizar (opcional)
        entity_id: ID de la entidad para leer/actualizar/eliminar (opcional)
        
    Returns:
        Dict[str, Any]: Resultado de la operación con status y datos
    """
    print(f"\\n[ENTIDADES_TOOL]: Acción '{action}' para cliente {id_cliente}")
    
    if action == "guardar":
        if not entity_data:
            return {"status": "error", "message": "Datos de entidad requeridos para guardar."}
        
        new_entity_id = str(uuid.uuid4())
        
        entity_entry = {
            "id_cliente": id_cliente,
            "tipo_entidad": entity_data.get("tipo_entidad", "Concepto"),
            "nombre_entidad": entity_data.get("nombre_entidad", ""),
            "datos_entidad": entity_data.get("datos_entidad", {}),
            "tipo_relacion": entity_data.get("tipo_relacion"),
            "estado": "activo",
            "created_at": datetime.now(),
            "modified_at": datetime.now()
        }
        
        _simulated_entities_db[new_entity_id] = {**entity_entry, "id": new_entity_id}
        
        print(f"       -> ENTIDAD GUARDADA: ID {new_entity_id}")
        print(f"          Tipo: {entity_data.get('tipo_entidad')}")
        
        return {"status": "ok", "entity_id": new_entity_id, "entity": _simulated_entities_db[new_entity_id]}
    
    elif action == "leer":
        if not entity_id:
            return {"status": "error", "message": "ID de entidad requerido para leer."}
        
        entity = _simulated_entities_db.get(entity_id)
        if entity:
            print(f"       -> ENTIDAD LEÍDA: {entity.get('nombre_entidad')}")
            return {"status": "ok", "entity": entity}
        else:
            return {"status": "not_found", "message": "Entidad no encontrada."}
    
    elif action == "actualizar":
        if not entity_id or not entity_data:
            return {"status": "error", "message": "ID y datos requeridos para actualizar."}
        
        if entity_id in _simulated_entities_db:
            _simulated_entities_db[entity_id].update(entity_data)
            _simulated_entities_db[entity_id]["modified_at"] = datetime.now()
            return {"status": "ok", "entity": _simulated_entities_db[entity_id]}
        else:
            return {"status": "not_found", "message": "Entidad no encontrada."}
    
    elif action == "eliminar":
        if not entity_id:
            return {"status": "error", "message": "ID de entidad requerido para eliminar."}
        
        if entity_id in _simulated_entities_db:
            del _simulated_entities_db[entity_id]
            print(f"       -> ENTIDAD ELIMINADA: {entity_id}")
            return {"status": "ok"}
        else:
            return {"status": "not_found", "message": "Entidad no encontrada."}
    
    else:
        return {"status": "error", "message": f"Acción no válida: {action}"}

# Crear FunctionTool ADK
entidades_tool = FunctionTool(entidades_function)
'''

with open('/home/jupyter/Zenda_ADK/tools/entidades_tool.py', 'w') as f:
    f.write(entidades_content)
    
print("✅ entidades_tool.py corregido!")