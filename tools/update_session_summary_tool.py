update_summary_content = '''from google.adk.tools import FunctionTool
from typing import Dict, Any
from schemas import SesionModel

# Simulación de base de datos de sesiones (TODO: reemplazar por Supabase)
_simulated_sessions_db = {}

def update_session_summary_function(session_id: str, historical_summary: str) -> Dict[str, Any]:
    """
    Actualiza el campo historical_summary de la sesión en la base de datos.
    Esta es una FunctionTool que el Agente QA usará para la memoria a largo plazo.
    
    Args:
        session_id: ID de la sesión
        historical_summary: El nuevo resumen acumulativo de la sesión
        
    Returns:
        Dict[str, Any]: Estado de la operación
    """
    print(f"\\n[UPDATE_SUMMARY_TOOL]: Actualizando resumen para sesión {session_id}")
    print(f"                        Resumen: '{historical_summary[:100]}...'")

    _simulated_sessions_db[session_id] = {
        "historical_summary": historical_summary,
        "updated_at": "2025-01-01T00:00:00Z"
    }
    
    print(f"       -> RESUMEN ACTUALIZADO exitosamente")
    print(f"          Longitud: {len(historical_summary)} caracteres")
    
    # Verificar calidad del resumen
    summary_quality_indicators = {
        "length_appropriate": 50 <= len(historical_summary) <= 500,
        "contains_key_elements": any(keyword in historical_summary.lower() 
                                   for keyword in ["cliente", "sesión", "tema", "progreso"]),
        "coherent_structure": historical_summary.count('.') >= 2
    }
    
    quality_score = sum(summary_quality_indicators.values()) / len(summary_quality_indicators)
    print(f"          Calidad estimada: {quality_score:.1%}")
    
    return {
        "status": "ok", 
        "session_id": session_id,
        "summary_length": len(historical_summary),
        "quality_score": quality_score,
        "message": "Resumen de sesión actualizado exitosamente"
    }

# Crear FunctionTool ADK
update_session_summary_tool = FunctionTool(update_session_summary_function)
'''

with open('/home/jupyter/Zenda_ADK/tools/update_session_summary_tool.py', 'w') as f:
    f.write(update_summary_content)
    
print("✅ update_session_summary_tool.py corregido!")
print("\n🎯 TODAS LAS TOOLS CORREGIDAS! Ahora probemos que funcionan...")