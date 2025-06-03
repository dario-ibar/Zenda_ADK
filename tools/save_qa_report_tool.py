save_qa_content = '''from google.adk.tools import FunctionTool
from typing import Dict, Any
from datetime import datetime
from schemas import QaModel
import uuid
import json

def save_qa_report_function(qa_report_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Guarda el reporte de auditoría QA en la tabla 'qa'.
    Esta es una FunctionTool que el Agente QA usará.
    
    Args:
        qa_report_data: Diccionario con todos los datos del reporte QA (métricas, scores, hallazgos)
        
    Returns:
        Dict[str, Any]: Estado de la operación con report_id
    """
    session_id = qa_report_data.get('id_sesion', 'N/A')
    print(f"\\n[SAVE_QA_TOOL]: Guardando reporte QA para sesión {session_id}")
    print(f"                  Adherencia: {qa_report_data.get('adherencia', 'N/A')}")
    print(f"                  Efectividad: {qa_report_data.get('efectividad', 'N/A')}")

    report_id = str(uuid.uuid4())
    
    print(f"       -> REPORTE QA GUARDADO: ID {report_id}")
    
    if qa_report_data.get('violaciones_guardrails'):
        print(f"       -> ⚠️  VIOLACIONES DETECTADAS: {qa_report_data['violaciones_guardrails']}")
    
    if qa_report_data.get('alarma_seguridad'):
        print(f"       -> 🚨 ALARMA DE SEGURIDAD ACTIVADA")
    
    print(f"       -> Métricas principales:")
    print(f"          • CSAT: {qa_report_data.get('CSAT', 'N/A')}")
    print(f"          • QA Labels: {qa_report_data.get('qa_labels', [])}")
    print(f"          • Fallos memoria: {qa_report_data.get('num_fallos_memoria_explicit', 0)} + {qa_report_data.get('num_fallos_memoria_implicit', 0)}")
    
    return {
        "status": "ok", 
        "report_id": report_id,
        "session_id": session_id,
        "message": "Reporte QA guardado exitosamente"
    }

# Crear FunctionTool ADK
save_qa_report_tool = FunctionTool(save_qa_report_function)
'''

with open('/home/jupyter/Zenda_ADK/tools/save_qa_report_tool.py', 'w') as f:
    f.write(save_qa_content)
    
print("✅ save_qa_report_tool.py corregido!")