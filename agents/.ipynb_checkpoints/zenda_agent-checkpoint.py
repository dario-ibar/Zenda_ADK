# Contenido actualizado del zenda_agent.py
new_zenda_content = '''from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.agent import AgentResult, GenerationResult # Para AgentResult, GenerationResult
from google.adk.function_tool import FunctionTool
from core.utils.prompt_utils import read_prompt_file
from schemas import SessionContext  # Importar SessionContext real
import json
import uuid # Para generar IDs de sesión/cliente si es necesario en placeholders
from typing import Optional, List, Dict, Any

# --- DEFINICIÓN DE FUNCTIONTOOLS (PLACEHOLDERS, SE IMPLEMENTARÁN EN PASOS POSTERIORES) ---
# Estas son las herramientas que el Agente Zenda usará.

def bitacora_tool(session_id: str, client_id: str, actor: str, tipo: str, texto: str, guia: List[str] = None, tt: str = None, canal: str = None) -> bool:
    """
    Registra un evento en la bitácora de la sesión.
    Args:
        session_id: ID de la sesión.
        client_id: ID del cliente.
        actor: Quién generó el evento (cliente, zenda, memo, dt, emo, qa, sistema).
        tipo: Tipo de entrada (msg, resumen, op, ent, emo, tec, fmem).
        texto: Contenido principal.
        guia: Códigos de guía aplicados (si aplica).
        tt: Si se usó Think Tool (S/F).
        canal: Canal de comunicación (T/S).
    Returns:
        True si el registro fue exitoso.
    """
    print(f"DEBUG: Llamada a bitacora_tool: Sesion={session_id}, Cliente={client_id}, Actor={actor}, Tipo={tipo}, Texto='{texto[:50]}...'")
    # TODO: Implementar la lógica real para guardar en la tabla bitacora (Paso 7)
    return True

def emotion_detection_tool(input_text: str, audio_bytes: bytes = None) -> dict:
    """
    Detecta la emoción/tono del input del cliente.
    Args:
        input_text: Texto del mensaje del cliente.
        audio_bytes: Datos de audio (si la comunicación es por voz).
    Returns:
        Un diccionario con la emoción detectada (ej. {"emocion": "frustracion", "nivel": "alto"}).
    """
    print(f"DEBUG: Llamada a emotion_detection_tool para texto: '{input_text[:50]}...'")
    # TODO: Implementar la lógica real usando Gemini Multimodal (Paso 4)
    # Simulación de detección
    if "frustracion" in input_text.lower() or "agotado" in input_text.lower():
        return {"emocion": "frustracion", "nivel": "alto"}
    if "miedo" in input_text.lower() or "ansiedad" in input_text.lower():
        return {"emocion": "ansiedad", "nivel": "medio"}
    return {"emocion": "neutral", "nivel": "bajo"}

def entidades_tool(session_id: str, client_id: str, action: str, entity_data: dict = None) -> dict:
    """
    Gestiona entidades (personas, organizaciones, jerga, conceptos) en la base de datos.
    Args:
        session_id: ID de la sesión.
        client_id: ID del cliente.
        action: Acción a realizar ("guardar", "actualizar", "leer").
        entity_data: Datos de la entidad para guardar/actualizar.
    Returns:
        Diccionario con el resultado de la operación (ej. {"status": "ok", "entity_id": "xyz"}).
    """
    print(f"DEBUG: Llamada a entidades_tool - Acción: {action}, Datos: {entity_data}")
    # TODO: Implementar lógica real para interactuar con tabla de entidades (Paso 4)
    return {"status": "ok"}

def save_context_info_tool(session_id: str, client_id: str, info_type: str, info_content: str) -> bool:
    """
    Guarda información muy específica del cliente o muy recurrente como entidad tipo "Jargon" o "Concepto".
    Args:
        session_id: ID de la sesión.
        client_id: ID del cliente.
        info_type: Tipo de información (ej. "Jargon", "Concepto", "DatoRelevante").
        info_content: Contenido textual a guardar.
    Returns:
        True si se guardó exitosamente.
    """
    print(f"DEBUG: Llamada a save_context_info_tool: Tipo={info_type}, Contenido='{info_content[:50]}...'")
    # TODO: Implementar lógica real para guardar en entidades (Paso 4)
    return True

# --- Cargar el prompt del Agente Zenda ---
try:
    zenda_prompt_content = read_prompt_file("zenda_system_prompt.md")
except FileNotFoundError as e:
    print(f"Error al cargar prompt de Zenda: {e}")
    zenda_prompt_content = "Rol: Eres Zenda, asistente conversacional. Misión: Asistir al cliente." # Prompt de fallback
except IOError as e:
    print(f"Error de IO al cargar prompt de Zenda: {e}")
    zenda_prompt_content = "Rol: Eres Zenda, asistente conversacional. Misión: Asistir al cliente." # Prompt de fallback

# --- Definición de Callback para Think Tool ---
# Este callback se activará DESPUÉS de que Zenda genere un borrador de respuesta.
def think_tool_callback(response: GenerationResult, tool_context: AgentResult) -> GenerationResult:
    """
    Callback que simula la lógica del Think Tool para evaluar y ajustar el borrador de respuesta de Zenda.
    """
    print("\\n[THINK_TOOL]: Think Tool activado. Evaluando borrador de respuesta...")
    
    # Extraer el borrador de respuesta de Zenda
    draft_response_text = response.text
    
    # --- Aquí iría la lógica del LLM económico (Gemini Flash) del Think Tool ---
    # Este LLM recibe el borrador y un prompt de crítica (ej. "Evalúa este texto. ¿Es empático? ¿Aplica la pauta X? ¿Es seguro?").
    # La respuesta del LLM crítico sería la base para la decisión de ajuste.

    # Simulación de la crítica y ajuste (PLACEHOLDER)
    critique_prompt = f"""
    Eres un auditor de IA. Evalúa el siguiente borrador de respuesta de Zenda.
    Criterios:
    - ¿Es empático y cálido?
    - ¿Aplica correctamente las pautas indicadas en el contexto (ej. from tool_context.state.pautas_priorizadas)?
    - ¿Es seguro y cumple los guardrails?
    - ¿Es conciso y respeta la regla 80/20/80?

    Borrador: "{draft_response_text}"

    Si hay fallos, sugiere una mejora y reescribe la respuesta. Si es bueno, solo di "OK".
    """
    # En una implementación real, aquí llamarías a un modelo LLM (ej. Gemini Flash) con critique_prompt
    # Ejemplo de respuesta simulada del crítico:
    simulated_critique_result = "OK. El borrador es bueno y cumple los criterios."
    
    # Lógica de decisión: si la crítica sugiere un ajuste, lo aplica.
    adjusted_response_text = draft_response_text # Por defecto, usar el original
    if "ajuste" in simulated_critique_result.lower(): # Simulación
        print("[THINK_TOOL]: Crítica indica ajuste. Simula ajuste de respuesta.")
        adjusted_response_text = "RESPUESTA AJUSTADA POR THINK TOOL: " + draft_response_text # Simulación de ajuste
        # En una real, el LLM crítico reescribiría.

    print(f"[THINK_TOOL]: Borrador evaluado. Resultado: '{simulated_critique_result[:50]}...'")
    
    # Devolver un nuevo GenerationResult con la respuesta ajustada o la original
    return GenerationResult(text=adjusted_response_text)

# --- Definición Completa del Agente Zenda ---

class ZendaAgent(LlmAgent):
    def __init__(self, name: str, instruction: str, model: str = "gemini-1.5-pro"):
        super().__init__(name=name, instruction=instruction, model=model)
        # Aquí se registrarían las herramientas en el AgentBuilder al ensamblar el flujo
        self.register_after_model_callback(think_tool_callback) # Registrar el Think Tool como callback

    def process_client_input(self, client_input: str, session_context: SessionContext, tools: list = None) -> str:
        """
        Método principal para que Zenda procese el input del cliente y genere una respuesta.
        Aquí se implementa la lógica detallada de las Partes 2 y 3 del prompt.
        """
        print(f"\\n[ZENDA_AGENT]: Procesando input del cliente: '{client_input[:50]}...'")
        
        # --- 2.1. Recepción y Preparación del Contexto ---
        # Los datos ya vienen en session_context.
        # Simulamos la detección de emoción y registro en bitácora.
        emocion_detectada = emotion_detection_tool(client_input)
        # Esto debería actualizar SessionContext o una base de datos directamente
        bitacora_tool(str(session_context.id_sesion), str(session_context.id_cliente), "cliente", "msg", client_input, canal=session_context.preferencias_usuario.get("canal_comunicacion", "T"))
        bitacora_tool(str(session_context.id_sesion), str(session_context.id_cliente), "emo", "emo", f"Emoción detectada: {emocion_detectada}", guia=[emocion_detectada.get("emocion")])
        
        # --- Construcción del Prompt Dinámico para la llamada al LLM de Zenda ---
        # Este es el input que se le pasa al LLM de Zenda en CADA turno.
        # Combina el prompt de sistema (self.instruction), el SessionContext, y el input del cliente.
        
        # Aquí se traduciría el SessionContext a un formato que el prompt de Zenda pueda entender.
        # Ejemplo: "CONTEXTO DE SESION: ... Criterios: ... Modo: ... Historial: ... Interacciones Recientes: ..."
        context_for_llm = f"""
        # CONTEXTO DE SESIÓN ACTUAL:
        - ID Sesión: {session_context.id_sesion}
        - ID Cliente: {session_context.id_cliente}
        - Fase Actual: {session_context.fase_actual}
        - Modo Asistencia: {session_context.modo_asistencia}
        - Guion DT: {session_context.guion_dt if session_context.guion_dt else 'N/A'}
        - Acuerdo Sesion: {session_context.acuerdo_sesion if session_context.acuerdo_sesion else 'No definido'}
        - Criterios DT: {json.dumps(session_context.criterios)}
        - Pautas Priorizadas por DT: {session_context.pautas_priorizadas}
        - Preferencias Cliente: {json.dumps(session_context.preferencias_usuario)}
        - Resumen Historial Larga: {session_context.resumen_memoria_larga if session_context.resumen_memoria_larga else 'No disponible.'}
        - Interacciones Recientes: {json.dumps(session_context.interacciones_recientes, default=str)}
        - Especialidad Principal: {session_context.especialidad_principal}
        - Especialidades Secundarias: {session_context.especialidades_secundarias}
        - Ciclo Rotativo Actual: {session_context.ciclo_rotativo_actual if session_context.ciclo_rotativo_actual else 'N/A'}
        
        # INPUT DEL CLIENTE PARA ESTE TURNO:
        {client_input}
        """

        # La llamada real al LLM se haría dentro de la lógica del AgentBuilder
        # Aquí simulamos la respuesta del LLM de Zenda basándonos en el prompt y contexto.

        # --- 2.2. Proceso Interno Principal por Modo de Asistencia (Adaptativo) ---
        # Esta lógica compleja es la que se guía por el System Prompt de Zenda (self.instruction)
        # y usaría el 'context_for_llm' para generar la respuesta.
        # Aquí se simula el resultado de ese procesamiento.

        draft_response = f"Simulando respuesta de Zenda en modo {session_context.modo_asistencia}, fase {session_context.fase_actual}. "
        if session_context.modo_asistencia == "Integral":
            draft_response += "Integrando perspectivas para una respuesta unificada. "
            if session_context.especialidad_principal:
                draft_response += f"Foco principal: {session_context.especialidad_principal}. "
        elif session_context.modo_asistencia == "Rotativo":
            if session_context.ciclo_rotativo_actual == "Exploracion":
                draft_response += "Sintetizando preguntas desde múltiples especialidades."
            elif session_context.ciclo_rotativo_actual == "Integracion":
                draft_response += "Consolidando asistencia integrando múltiples visiones."
        elif session_context.modo_asistencia == "Especialidad":
            draft_response += f"Enfocado en {session_context.especialidad_principal}. "
        elif session_context.modo_asistencia == "Urgente":
            draft_response += "Priorizando contención y rapidez. "

        # --- 2.3. Síntesis y Conciliación ---
        # El borrador 'draft_response' ya lo contiene, ahora se identifica la guía.
        pauta_aplicada_codes = session_context.pautas_priorizadas if session_context.pautas_priorizadas else ["DEFAULT_NO_PAUTA"]

        # --- 2.4. Think Tool (Activación Condicional) ---
        final_response_text = draft_response
        if session_context.think_tool_activado:
            print(f"[ZENDA_AGENT]: Think Tool activado por DT. Motivo: {session_context.motivo_tt}. Enviando borrador al callback...")
            # En una implementación real, aquí se usaría un LlmAgent con callback
            # Simulamos el callback Think Tool aquí:
            simulated_gen_result = GenerationResult(text=draft_response)
            simulated_agent_result_for_tt = AgentResult(state=session_context.model_dump()) # Estado para el TT usando Pydantic
            tt_output = think_tool_callback(simulated_gen_result, simulated_agent_result_for_tt)
            final_response_text = tt_output.text
        else:
            print("[ZENDA_AGENT]: Think Tool no activado por DT para este turno.")

        # --- 2.5. Generación de Respuesta y Registro Final ---
        # Registrar la respuesta final de Zenda
        bitacora_tool(session_id=str(session_context.id_sesion), client_id=str(session_context.id_cliente),
                      actor="zenda", tipo="msg", texto=final_response_text,
                      guia=pauta_aplicada_codes, tt=session_context.motivo_tt,
                      canal=session_context.preferencias_usuario.get("canal_comunicacion", "T"))

        print(f"[ZENDA_AGENT]: Respuesta final generada: '{final_response_text[:100]}...'")
        return final_response_text

# Instanciar el agente Zenda con su prompt
zenda_agent_instance = ZendaAgent(
    name="zenda_core", # Usamos un nombre de instancia
    instruction=zenda_prompt_content,
    model="gemini-1.5-pro" # O el modelo específico para Zenda
)

print("\\nAgente Zenda (ZendaAgent) definido y configurado exitosamente con SessionContext Pydantic real.")
'''

# Escribir el archivo actualizado
with open('/home/jupyter/Zenda_ADK/agents/zenda_agent.py', 'w') as f:
    f.write(new_zenda_content)
    
print("✅ zenda_agent.py actualizado con SessionContext Pydantic real!")
print("✅ Placeholder SessionContext eliminado")
print("✅ Agregado .model_dump() y conversiones str() para UUIDs")