# tools/entidades_tool.py
from typing import Dict, Any, List, Optional, Literal
import json
from datetime import datetime

# --- Placeholder para el modelo Pydantic Entidad (se reemplazará por el real) ---
# Asumimos que Entidad será una clase que podemos convertir a dict
class Entidad:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    def to_dict(self):
        # Simulación de conversión para el log
        data = {}
        for k, v in self.__dict__.items():
            if isinstance(v, datetime):
                data[k] = v.isoformat()
            else:
                data[k] = v
        return data

# --- Placeholder para la tabla 'entidades' en Supabase (se implementará en Paso 7) ---
_simulated_entities_db = {} # Simulación de una base de datos en memoria

def entidades_tool(session_id: str, client_id: str, action: str, entity_data: Optional[Dict[str, Any]] = None,
                   entity_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Gestiona entidades (personas, organizaciones, jerga, conceptos) en la base de datos.
    Esta es una FunctionTool que los agentes usarán.
    Args:
        session_id: ID de la sesión actual.
        client_id: ID del cliente asociado.
        action: Acción a realizar ("guardar", "actualizar", "leer", "eliminar").
        entity_data: Datos de la entidad para guardar/actualizar (diccionario).
        entity_id: ID de la entidad para acciones de leer/actualizar/eliminar.
    Returns:
        Diccionario con el resultado de la operación (ej. {"status": "ok", "entity": {...}}).
    """
    print(f"\n[TOOL]: entidades_tool invocada - Acción: '{action}'")

    # TODO: Implementar la lógica REAL de interacción con Supabase (Paso 7)
    # Por ahora, simulación básica de operaciones CRUD en memoria.

    if action == "guardar":
        if not entity_data:
            print("       -> ERROR: Datos de entidad no proporcionados para 'guardar'.")
            return {"status": "error", "message": "Datos de entidad requeridos."}

        new_entity_id = str(uuid.uuid4()) # Generar un ID único para la nueva entidad
        _simulated_entities_db[new_entity_id] = {**entity_data, "id": new_entity_id, "created_at": datetime.now().isoformat()}
        print(f"       -> ENTIDAD GUARDADA (Simulado): ID {new_entity_id}, Tipo: {entity_data.get('tipo_entidad')}, Nombre: {entity_data.get('nombre_entidad')}")
        return {"status": "ok", "entity_id": new_entity_id, "entity": _simulated_entities_db[new_entity_id]}

    elif action == "leer":
        if not entity_id:
            print("       -> ERROR: ID de entidad no proporcionado para 'leer'.")
            return {"status": "error", "message": "ID de entidad requerido."}

        entity = _simulated_entities_db.get(entity_id)
        if entity:
            print(f"       -> ENTIDAD LEÍDA (Simulado): ID {entity_id}, Nombre: {entity.get('nombre_entidad')}")
            return {"status": "ok", "entity": entity}
        else:
            print(f"       -> ENTIDAD NO ENCONTRADA (Simulado): ID {entity_id}")
            return {"status": "not_found", "message": "Entidad no encontrada."}

    elif action == "actualizar":
        if not entity_id or not entity_data:
            print("       -> ERROR: ID o datos de entidad no proporcionados para 'actualizar'.")
            return {"status": "error", "message": "ID y datos de entidad requeridos."}

        if entity_id in _simulated_entities_db:
            _simulated_entities_db[entity_id].update(entity_data)
            print(f"       -> ENTIDAD ACTUALIZADA (Simulado): ID {entity_id}")
            return {"status": "ok", "entity": _simulated_entities_db[entity_id]}
        else:
            print(f"       -> ENTIDAD NO ENCONTRADA para actualizar (Simulado): ID {entity_id}")
            return {"status": "not_found", "message": "Entidad no encontrada para actualizar."}

    elif action == "eliminar":
        if not entity_id:
            print("       -> ERROR: ID de entidad no proporcionado para 'eliminar'.")
            return {"status": "error", "message": "ID de entidad requerido."}

        if entity_id in _simulated_entities_db:
            del _simulated_entities_db[entity_id]
            print(f"       -> ENTIDAD ELIMINADA (Simulado): ID {entity_id}")
            return {"status": "ok"}
        else:
            print(f"       -> ENTIDAD NO ENCONTRADA para eliminar (Simulado): ID {entity_id}")
            return {"status": "not_found", "message": "Entidad no encontrada para eliminar."}
    else:
        print(f"       -> ERROR: Acción de entidades_tool no reconocida: {action}")
        return {"status": "error", "message": "Acción no válida."}
