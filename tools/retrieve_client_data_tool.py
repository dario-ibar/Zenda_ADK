retrieve_content = '''from google.adk.tools import FunctionTool
from typing import Dict, Any
from schemas import ClienteModel, SesionModel, EntidadModel
import json

# Simulación de base de datos (TODO: reemplazar por Supabase real)
_simulated_db_clients = {
    "test_client_id_1": {
        "preferencias": {"idioma": "es", "tono": "cercano", "voz": "femenina", "canal_comunicacion": "T"},
        "resumen_memoria_larga": "El cliente tiene un conflicto laboral. En sesiones anteriores, expresó frustración y ha trabajado en técnicas de gestión de estrés. Su objetivo actual es mejorar la comunicación en el trabajo.",
        "entidades_iniciales": [
            {"tipo_entidad": "Persona", "nombre_entidad": "Jefe", "datos_entidad": {"rol": "superior"}, "tipo_relacion": "Disfuncional"},
            {"tipo_entidad": "Concepto", "nombre_entidad": "Burnout", "datos_entidad": {"definicion": "Estado de agotamiento físico y emocional."}, "estado": "Confirmado"}
        ],
        "CSAT": 8,
        "comentario_usuario": "Zenda me ayudó a ver el problema desde otra perspectiva."
    }
}

def retrieve_client_data_function(client_id: str) -> Dict[str, Any]:
    """
    Recupera datos esenciales del cliente desde la base de datos.
    Esta es una FunctionTool que el Agente DT usará al inicio de la sesión.
    
    Args:
        client_id: ID único del cliente
        
    Returns:
        Dict[str, Any]: Diccionario con preferencias, resumen de memoria larga, y entidades iniciales
    """
    print(f"\\n[RETRIEVE_CLIENT_TOOL]: Recuperando datos para cliente '{client_id}'")

    data = _simulated_db_clients.get(client_id, {})

    if not data:
        print(f"       -> CLIENTE NO ENCONTRADO: '{client_id}' - Devolviendo datos por defecto")
        return {
            "preferencias": {"idioma": "es", "tono": "profesional", "canal_comunicacion": "T"},
            "resumen_memoria_larga": None,
            "entidades_iniciales": [],
            "CSAT": None,
            "comentario_usuario": None
        }
    else:
        resumen = data.get('resumen_memoria_larga', '')
        print(f"       -> DATOS RECUPERADOS - Resumen: '{resumen[:50]}...'")
        print(f"          Preferencias: {data.get('preferencias', {}).get('idioma', 'N/A')}")
        print(f"          Entidades: {len(data.get('entidades_iniciales', []))}")

    return {
        "preferencias": data.get("preferencias", {}),
        "resumen_memoria_larga": data.get("resumen_memoria_larga"),
        "entidades_iniciales": data.get("entidades_iniciales", []),
        "CSAT": data.get("CSAT"),
        "comentario_usuario": data.get("comentario_usuario")
    }

# Crear FunctionTool ADK
retrieve_client_data_tool = FunctionTool(retrieve_client_data_function)
'''

with open('/home/jupyter/Zenda_ADK/tools/retrieve_client_data_tool.py', 'w') as f:
    f.write(retrieve_content)
    
print("✅ retrieve_client_data_tool.py corregido!")