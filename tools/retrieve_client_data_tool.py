# tools/retrieve_client_data_tool.py
from typing import Dict, Any, Optional
import json

# --- Placeholder para simular la base de datos (se reemplazará por la conexión real a Supabase) ---
_simulated_db_clients = {
    "test_client_id_1": {
        "preferencias": {"idioma": "es", "tono": "cercano", "voz": "femenina", "canal_comunicacion": "T"},
        "resumen_memoria_larga": "El cliente tiene un conflicto laboral. En sesiones anteriores, expresó frustración y ha trabajado en técnicas de gestión de estrés. Su objetivo actual es mejorar la comunicación en el trabajo.",
        "entidades_iniciales": [
            {"tipo_entidad": "Persona", "nombre_entidad": "Jefe", "datos_entidad": {"rol": "superior"}, "tipo_relacion": "Disfuncional"},
            {"tipo_entidad": "Concepto", "nombre_entidad": "Burnout", "datos_entidad": {"definicion": "Estado de agotamiento físico y emocional."}, "confirmacion": "Confirmado"}
        ],
        "CSAT": 8,
        "comentario_usuario": "Zenda me ayudó a ver el problema desde otra perspectiva."
    }
}

def retrieve_client_data_tool(client_id: str) -> Dict[str, Any]:
    """
    Recupera datos esenciales del cliente desde la base de datos (simulada por ahora).
    Esta es una FunctionTool que el Agente DT usará al inicio de la sesión.
    Args:
        client_id: ID único del cliente.
    Returns:
        Un diccionario con las preferencias del cliente, el último resumen_memoria_larga,
        y entidades iniciales.
    """
    print(f"\n[TOOL]: retrieve_client_data_tool invocada para cliente: '{client_id}'")

    # TODO: Implementar la lógica REAL de lectura de Supabase (Paso 7: Persistencia)
    # Esto debería leer de las tablas 'clientes', 'sesiones' (para el resumen), 'entidades'.

    data = _simulated_db_clients.get(client_id, {})

    if not data:
        print(f"       -> CLIENTE NO ENCONTRADO (Simulado): ID '{client_id}'. Devolviendo datos vacíos.")
    else:
        print(f"       -> Datos de cliente recuperados (Simulado). Resumen: '{data.get('resumen_memoria_larga', '')[:50]}...'")

    return {
        "preferencias": data.get("preferencias", {}),
        "resumen_memoria_larga": data.get("resumen_memoria_larga", None),
        "entidades_iniciales": data.get("entidades_iniciales", []),
        "CSAT": data.get("CSAT", None), # Añadido para el Agente QA
        "comentario_usuario": data.get("comentario_usuario", None) # Añadido para el Agente QA
    }
