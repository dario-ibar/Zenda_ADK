# tools/save_context_info_tool.py
from typing import Dict, Any, Optional
import json
from datetime import datetime
import uuid # Para simular IDs si se necesita

# --- Placeholder para la tabla 'entidades' en Supabase (se implementará en Paso 7) ---
_simulated_entities_db = {} # Simulación de una base de datos en memoria

def save_context_info_tool(session_id: str, client_id: str, info_type: str, info_content: str) -> Dict[str, Any]:
    """
    Guarda información muy específica del cliente o muy recurrente (jerga, conceptos)
    como entidad tipo "Jargon", "Concepto" o "DatoRelevante" en la base de datos de entidades.
    Esta es una FunctionTool que los agentes usarán.
    Args:
        session_id: ID de la sesión actual.
        client_id: ID del cliente asociado.
        info_type: Tipo de información (ej. "Jargon", "Concepto", "DatoRelevante").
        info_content: Contenido textual a guardar.
    Returns:
        Diccionario con el resultado de la operación (ej. {"status": "ok", "entity_id": "xyz"}).
    """
    print(f"\n[TOOL]: save_context_info_tool invocada - Tipo: '{info_type}', Contenido: '{info_content[:50]}...'")

    # TODO: Implementar la lógica REAL de persistencia a Supabase (Paso 7)
    # Esto internamente podría usar la lógica de entidades_tool para guardar una entidad.

    new_entity_id = str(uuid.uuid4())
    entity_data = {
        "id_cliente": client_id,
        "session_id_origen": session_id, # Para trazabilidad
        "tipo_entidad": info_type,
        "nombre_entidad": info_content[:100], # Usar parte del contenido como nombre
        "datos_entidad": {"content": info_content, "detected_at": datetime.now().isoformat()},
        "confirmacion": "Detectado",
        "fecha_deteccion": datetime.now().isoformat()
    }
    _simulated_entities_db[new_entity_id] = entity_data

    print(f"       -> CONTEXTO ESPECÍFICO GUARDADO (Simulado): Tipo: {info_type}, ID: {new_entity_id}")
    return {"status": "ok", "entity_id": new_entity_id}
