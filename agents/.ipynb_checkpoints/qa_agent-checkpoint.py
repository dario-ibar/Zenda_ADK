from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.agent import AgentResult, GenerationResult
from google.adk.function_tool import FunctionTool
from core.utils.prompt_utils import read_prompt_file
import json
import uuid
from typing import Optional, List, Dict, Any

# --- Importar modelos Pydantic (PLACEHOLDERS, SE HARÁ EN PASOS POSTERIORES) ---
# Cuando los modelos Pydantic reales estén creados en models/, se reemplazarán estas clases placeholder.

class SessionContext: # Placeholder para el modelo ContextoSesion
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    def to_dict(self):
        return self.__dict__
    @staticmethod
    def from_dict(data):
        return SessionContext(**data)

class BitacoraEntry: # Placeholder para el modelo BitacoraEntry
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    def to_dict(self):
        return self.__dict__
    @staticmethod
    def from_dict(data):
        return BitacoraEntry(**data)

class Sesion: # Placeholder para el modelo Sesion
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    def to_dict(self):
        return self.__dict__
    @staticmethod
    def from_dict(data):
        return Sesion(**data)

# --- DEFINICIÓN DE FUNCTIONTOOLS (PLACEHOLDERS, SE IMPLEMENTARÁN EN PASOS POSTERIORES) ---
# Estas son las herramientas que el Agente QA usará.

def retrieve_bitacora_tool(session_id: str) -> List[dict]:
    """
    Recupera todas las entradas de la bitácora para una sesión específica.
    Args:
        session_id: ID de la sesión.
    Returns:
        Una lista de diccionarios, cada uno representando una entrada de bitácora.
    """
    print(f"DEBUG: Llamada a retrieve_bitacora_tool para sesión: {session_id}")
    # TODO: Implementar la lógica real para leer de la tabla bitacora (Paso 7)
    # Simulación de datos de bitácora
    return [
        {"actor": "cliente", "tipo": "msg", "texto": "Hola, tengo un problema con mi jefe, me siento frustrado."},
        {"actor": "zenda", "tipo": "msg", "texto": "Entiendo tu frustración. ¿Podrías contarme más sobre lo que está pasando?"},
        {"actor": "memo", "tipo": "emo", "texto": "Emoción detectada: frustración"},
        {"actor": "zenda", "tipo": "tec", "texto": "Se aplicó pauta ICF-1.1_escucha_activa", "guia": ["ICF-1.1_escucha_activa"]},
        {"actor": "cliente", "tipo": "msg", "texto": "Sí, me siento agotado y a veces creo que no sirvo para esto."},
        {"actor": "memo", "tipo": "op", "texto": "Oportunidad: Cliente menciona baja autoestima.", "status": "detectado"},
        {"actor": "zenda", "tipo": "msg", "texto": "Parece que te sientes agotado y que hay dudas sobre tu valía. Es normal sentirse así en estas situaciones. ¿Podrías explorar un poco más esa sensación?"},
        {"actor": "dt", "tipo": "tec", "texto": "DT ajusta estrategia: activar TT por tema sensible 'autoestima'.", "tt": "S"},
        {"actor": "zenda", "tipo": "msg", "texto": "DEBUG TT AJUSTÓ: Explorando la valía personal..."}, # Simulando TT
    ]

def save_qa_report_tool(qa_report_data: dict) -> bool:
    """
    Guarda el reporte de auditoría QA en la tabla 'qa'.
    Args:
        qa_report_data: Diccionario con los datos del reporte QA.
    Returns:
        True si el registro fue exitoso.
    """
    print(f"DEBUG: Llamada a save_qa_report_tool con reporte QA: {json.dumps(qa_report_data, indent=2)}")
    # TODO: Implementar la lógica real para guardar en la tabla qa (Paso 7)
    return True

def update_session_summary_tool(session_id: str, historical_summary: str) -> bool:
    """
    Actualiza el campo historical_summary de la sesión en la base de datos.
    Args:
        session_id: ID de la sesión.
        historical_summary: El nuevo resumen acumulativo.
    Returns:
        True si la actualización fue exitosa.
    """
    print(f"DEBUG: Llamada a update_session_summary_tool para sesión {session_id} con resumen: {historical_summary[:100]}...")
    # TODO: Implementar la lógica real para guardar en sesiones.historical_summary (Paso 7)
    return True

# --- Cargar el prompt del Agente QA ---
try:
    qa_prompt_content = read_prompt_file("qa_system_prompt.md")
except FileNotFoundError as e:
    print(f"Error al cargar prompt de QA: {e}")
    qa_prompt_content = "Rol: Eres el Agente QA. Tu misión es auditar sesiones." # Prompt de fallback
except IOError as e:
    print(f"Error de IO al cargar prompt de QA: {e}")
    qa_prompt_content = "Rol: Eres el Agente QA. Tu misión es auditar sesiones." # Prompt de fallback

# --- Definición Completa del Agente QA ---

class QaAgent(LlmAgent):
    def __init__(self, name: str, instruction: str, model: str = "gemini-1.5-pro", # Modelo para auditoría principal
                 summary_gen_model: str = "gemini-1.5-flash", # Modelo para generación de resumen (económico)
                 summary_eval_model: str = "gemini-1.5-pro"): # Modelo para evaluación de resumen (avanzado)
        
        super().__init__(name=name, instruction=instruction, model=model)
        self.summary_gen_model = summary_gen_model
        self.summary_eval_model = summary_eval_model

    def perform_audit(self, session_data: Sesion) -> dict: # Recibe el objeto Sesion completo
        """
        Método principal para que el Agente QA realice una auditoría post-sesión.
        """
        print(f"\n[QA_AGENT]: Iniciando auditoría para sesión {session_data.id_sesion}, cliente {session_data.id_cliente}...")
        
        # 1. Recuperar Bitácora Completa
        bitacora_completa = retrieve_bitacora_tool(session_data.id_sesion)
        if not bitacora_completa:
            print("[QA_AGENT]: No se encontró bitácora para auditar. Saliendo.")
            return {"status": "no_bitacora"}

        # 2. Pre-cálculos para la auditoría (Ej: duración, tokens, etc., que ya están en session_data)
        session_duration_sec = session_data.duracion_segundos
        session_total_tokens = session_data.tokens_total
        client_comment = session_data.comentario_usuario
        client_satisfaction = session_data.satisfaccion

        # --- 3. Lógica del LLM de QA para la Auditoría Holística de Calidad ---
        # Este es el corazón de la evaluación. Se pasaría el prompt de QA (self.instruction)
        # y la bitácora completa al LLM avanzado (self.model).
        
        audit_prompt = f"""
        # INSTRUCCIONES: Eres el Agente QA de Zenda. Realiza una auditoría exhaustiva de la siguiente sesión.
        # BITACORA DE LA SESIÓN: {json.dumps(bitacora_completa, indent=2)}
        # COMENTARIO DEL CLIENTE: "{client_comment if client_comment else 'N/A'}"
        # SATISFACCION DEL CLIENTE (1-10): {client_satisfaction if client_satisfaction else 'N/A'}
        
        # Basado en la bitácora y el feedback del cliente, calcula las siguientes métricas (1-10):
        # 1. Adherencia (1-10): Evalúa si Zenda detectó y seleccionó correctamente las pautas/comportamientos relevantes, incluyendo fallas por omisión.
        # 2. Efectividad (1-10): Evalúa la calidad de la ejecución de las pautas aplicadas y la calidad general de comunicación (tono, empatía, claridad, proactividad, extensión justa).
        # 3. Score_Calidad_Resumen (1-10): Evalúa la calidad del resumen de memoria larga generado para esta sesión.
        # 4. Score_Satisfaccion_Cliente (CSAT) (1-10): Directamente la puntuación del cliente.
        
        # Identifica y lista:
        # - violaciones_guardrails (lista de strings).
        # - num_fallos_memoria_explicit (conteo).
        # - num_fallos_memoria_implicit (conteo).
        # - num_oportunidades_detectadas (conteo).
        # - qa_labels (lista de etiquetas cualitativas del comentario del cliente).
        
        # Si detectas violaciones de guardrails, menciona "ALARMA_SEGURIDAD".
        # Responde solo con un objeto JSON.
        """
        
        # Simulación de la llamada al LLM avanzado para la auditoría principal
        print("[QA_AGENT]: Llamando a LLM avanzado para auditoría principal...")
        # En una implementación real: response = self.model.generate_content(audit_prompt)
        
        # Simulación de la salida del LLM de QA
        qa_raw_output = {
            "adherencia": 8,
            "efectividad": 7.5,
            "Score_Tono_Consistencia": 8,
            "Score_Empatia_Validacion": 7,
            "Score_Claridad_Concisión": 9,
            "Score_Proactividad_Observacion": 6,
            "Score_Extensión_Justa": 7,
            "violaciones_guardrails": [],
            "num_fallos_memoria_explicit": 0,
            "num_fallos_memoria_implicit": 1,
            "num_oportunidades_detectadas": 1,
            "qa_labels": ["frustracion_manejada", "memoria_imprecisa"],
            "score_calidad_resumen": 9, # Placeholder, se calculará abajo
            "alarma_seguridad": False
        }
        
        # --- 4. Generación y Validación del resumen_memoria_larga ---
        # 4.1. Generación (LLM económico)
        print("[QA_AGENT]: Generando resumen de memoria larga (LLM económico)...")
        summary_gen_prompt = f"Basado en la siguiente bitácora de sesión, genera un resumen conciso y coherente para la memoria larga del cliente. Bitácora: {json.dumps(bitacora_completa)}"
        # En una implementación real: raw_summary = self.summary_gen_model.generate_content(summary_gen_prompt)
        raw_summary_text = f"Resumen de la sesión {session_data.id_sesion}: El cliente discutió problemas con su jefe y frustración, mostrando avances en el reconocimiento de sus emociones."
        
        # 4.2. Validación (LLM avanzado)
        print("[QA_AGENT]: Validando resumen de memoria larga (LLM avanzado)...")
        summary_eval_prompt = f"Evalúa la calidad del siguiente resumen de sesión contra la bitácora original. Resumen: '{raw_summary_text}'. Bitácora: {json.dumps(bitacora_completa)}. Puntúa de 1-10."
        # En una implementación real: eval_response = self.summary_eval_model.generate_content(summary_eval_prompt)
        
        # Simulación de score de validación
        qa_raw_output["score_calidad_resumen"] = 9 # Actualizamos el score en el reporte

        # 4.3. Actualizar resumen en la DB
        update_session_summary_tool(session_data.id_sesion, raw_summary_text)

        # --- 5. Consolidación y Registro ---
        qa_report = {
            "id_sesion": str(session_data.id_sesion), # Asegurar str si Pydantic usa UUID
            "id_cliente": str(session_data.id_cliente),
            "adherencia": qa_raw_output["adherencia"],
            "efectividad": qa_raw_output["efectividad"],
            "score_tono_consistencia": qa_raw_output["Score_Tono_Consistencia"],
            "score_empatia_validacion": qa_raw_output["Score_Empatia_Validacion"],
            "score_claridad_concision": qa_raw_output["Score_Claridad_Concisión"],
            "score_proactividad_observacion": qa_raw_output["Score_Proactividad_Observacion"],
            "score_extension_justa": qa_raw_output["Score_Extensión_Justa"],
            "violaciones_guardrails": qa_raw_output["violaciones_guardrails"],
            "num_fallos_memoria_explicit": qa_raw_output["num_fallos_memoria_explicit"],
            "num_fallos_memoria_implicit": qa_raw_output["num_fallos_memoria_implicit"],
            "num_oportunidades_detectadas": qa_raw_output["num_oportunidades_detectadas"],
            "CSAT": client_satisfaction, # Viene directo del Sesion
            "qa_labels": qa_raw_output["qa_labels"],
            "score_calidad_resumen": qa_raw_output["score_calidad_resumen"],
            "alarma_seguridad": qa_raw_output["alarma_seguridad"] # Para disparar alerta
        }
        
        save_qa_report_tool(qa_report) # Guarda el reporte en la tabla 'qa'

        print(f"\n[QA_AGENT]: Auditoría de sesión {session_data.id_sesion} completada y registrada.")
        return qa_report

# Instanciar el agente QA con sus prompts y modelos
qa_agent_instance = QaAgent(
    name="qa_auditor",
    instruction=qa_prompt_content,
    model="gemini-1.5-pro", # Modelo para la auditoría principal
    summary_gen_model="gemini-1.5-flash", # Modelo para generar resumen
    summary_eval_model="gemini-1.5-pro" # Modelo para evaluar el resumen
)

print("\nAgente QA (QaAgent) definido y configurado exitosamente con lógica completa.")
