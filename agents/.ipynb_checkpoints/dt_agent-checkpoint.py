# Contenido actualizado del dt_agent.py
new_dt_content = '''from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.agent import AgentResult # Para AgentResult
from google.adk.agent_builder import AgentBuilder
from google.adk.function_tool import FunctionTool
from core.utils.prompt_utils import read_prompt_file
from schemas import SessionContext  # Importar SessionContext real
import json # Necesario para manejar JSON en el SessionContext

# --- DEFINICIÓN DE FUNCTIONTOOLS (PLACEHOLDERS, SE IMPLEMENTARÁN EN PASOS POSTERIORES) ---
# Estas son las herramientas que el Agente DT usará.

def retrieve_client_data_tool(client_id: str) -> dict:
    """
    Recupera datos básicos del cliente (preferencias, resumen_memoria_larga, entidades iniciales).
    Args:
        client_id: ID único del cliente.
    Returns:
        Un diccionario con las preferencias, el último resumen_memoria_larga, y entidades_iniciales.
    """
    print(f"DEBUG: Llamada a retrieve_client_data_tool para cliente: {client_id}")
    # TODO: Implementar la lógica real para leer de Supabase (Paso 4)
    # Valores de ejemplo para que la lógica del DT pueda operar
    return {
        "preferencias": {"idioma": "es", "tono": "cercano", "voz": "femenina"},
        "resumen_memoria_larga": "El cliente tiene un conflicto laboral y ha mostrado frustración en sesiones anteriores. Ha trabajado en la gestión del estrés.",
        "entidades_iniciales": [] # Por ahora, vacío
    }

def update_session_context_tool(session_id: str, client_id: str, context_data: dict) -> bool:
    """
    Actualiza el SessionContext global en el ADK State con nuevos datos.
    En un entorno ADK real, esto se haría manejando el ADK State directamente
    o a través de un servicio de estado.
    Args:
        session_id: ID de la sesión.
        client_id: ID del cliente.
        context_data: Diccionario con los datos a actualizar en el SessionContext.
    Returns:
        True si la actualización fue exitosa.
    """
    print(f"DEBUG: Llamada a update_session_context_tool para sesión {session_id}, cliente {client_id} con datos: {json.dumps(context_data, default=str)}")
    # TODO: Implementar la lógica real para actualizar el ADK State (Paso 4/5)
    # Aquí solo simulamos la acción.
    return True

def log_dt_finding_tool(session_id: str, client_id: str, finding_type: str, description: str, tags: list = None) -> bool:
    """
    Registra hallazgos y decisiones estratégicas del DT en la bitácora para "aprendizaje en frío".
    Args:
        session_id: ID de la sesión actual.
        client_id: ID del cliente.
        finding_type: Tipo de hallazgo (ej., "tema_sensible", "ajuste_estrategia", "falla_memoria_detectada").
        description: Descripción detallada del hallazgo o decisión.
        tags: Lista de etiquetas adicionales (ej., ["prioridad_alta", "revisar_manualmente"]).
    Returns:
        True si el registro fue exitoso.
    """
    print(f"DEBUG: Llamada a log_dt_finding_tool: {finding_type} - {description} (Tags: {tags})")
    # TODO: Implementar la lógica real para guardar en la tabla bitacora (Paso 7)
    return True

# --- Cargar el prompt del Agente DT ---
try:
    dt_prompt_content = read_prompt_file("dt_system_prompt.md")
except FileNotFoundError as e:
    print(f"Error al cargar prompt de DT: {e}")
    dt_prompt_content = "Rol: Agente DT de Zenda. Misión: Guiar la sesión." # Prompt de fallback
except IOError as e:
    print(f"Error de IO al cargar prompt de DT: {e}")
    dt_prompt_content = "Rol: Agente DT de Zenda. Misión: Guiar la sesión." # Prompt de fallback


# --- Definición Completa del Agente DT ---

class DtAgent(LlmAgent):
    def __init__(self, name: str, instruction: str, model: str = "gemini-1.5-pro"):
        super().__init__(name=name, instruction=instruction, model=model)
        # Se registrarían las herramientas en el AgentBuilder al ensamblar el flujo

    # Método que encapsula la lógica de inicialización de la sesión por el DT
    def initialize_session_context(self, client_id: str, session_id: str, initial_input: str) -> SessionContext:
        """
        Lógica del DT para inicializar el SessionContext al inicio de una nueva sesión.
        """
        print(f"\\n[DT_AGENT]: Iniciando contexto para cliente {client_id}, sesión {session_id}...")
        
        # 1. Recuperar datos del cliente (simulando tool call)
        client_data = retrieve_client_data_tool(client_id)

        # 2. Asegurar que Context Caching esté poblado (placeholder)
        print("[DT_AGENT]: Asegurando que Context Caching esté poblado (lógica placeholder)...")
        # TODO: Implementar lógica de CC aquí (Paso 5)
        
        # 3. Preparar SessionContext inicial usando Pydantic
        session_context = SessionContext(
            id_cliente=client_id,
            id_sesion=session_id,
            fase_actual="Inicio_Sesion",
            modo_asistencia="Integral",
            guion_dt="Exploración inicial del problema del cliente para establecer el acuerdo de sesión.",
            acuerdo_sesion=None,
            criterios={"foco": "rapport", "objetivo_inicial": "identificar_tema_principal"},
            pautas_priorizadas=["ICF-1.1_escucha_activa", "ICF-2.0_preg_abiertas"],
            resumen_memoria_larga=client_data.get("resumen_memoria_larga"),
            interacciones_recientes=[{"actor": "cliente", "text": initial_input}],
            preferencias_usuario=client_data.get("preferencias", {}),
            especialidad_principal="ICF",
            especialidades_secundarias=["Ontología", "Gestalt"],
            ciclo_rotativo_actual=None,
            think_tool_activado=False,
            motivo_tt=None
        )
        
        update_session_context_tool(str(session_context.id_sesion), str(session_context.id_cliente), session_context.model_dump()) 
        print("[DT_AGENT]: Contexto de sesión inicial preparado y actualizado.")
        
        return session_context

    # Este método simula la lógica turno a turno del DT (será parte de un AgentBuilder)
    def decide_turn_strategy(self, current_session_context: SessionContext, user_input: str, recent_events: list = None) -> SessionContext:
        """
        Lógica del DT para decidir la estrategia turno a turno.
        """
        print(f"\\n[DT_AGENT]: Decidiendo estrategia para el turno. Fase actual: {current_session_context.fase_actual}")
        
        # Crear nuevo SessionContext modificado usando Pydantic
        new_session_context = current_session_context.model_copy(deep=True)
        
        # --- Lógica de ejemplo de decisión del DT (simulando razonamiento LLM) ---
        # 1. Detección de tema sensible o falla de memoria para activar Think Tool
        if "ansiedad" in user_input.lower() or "estrés" in user_input.lower() or \
           "miedo" in user_input.lower() or "depresion" in user_input.lower():
            new_session_context.think_tool_activado = True
            new_session_context.motivo_tt = "S"
            if "foco" not in new_session_context.criterios or new_session_context.criterios.get("foco") != "manejo_emocional":
                new_session_context.criterios["foco"] = "manejo_emocional"
                new_session_context.guion_dt = "Explorar y validar emociones, buscando estrategias de manejo."
                log_dt_finding_tool(
                    session_id=str(new_session_context.id_sesion),
                    client_id=str(new_session_context.id_cliente),
                    finding_type="ajuste_estrategia_tema_sensible",
                    description=f"Tema sensible detectado ('{user_input}'). DT ajusta foco y activa TT.",
                    tags=["tema_sensible", "estrat_dt", "tt_activado"]
                )
        elif "olvidaste" in user_input.lower() or "no recuerdas" in user_input.lower():
            new_session_context.think_tool_activado = True
            new_session_context.motivo_tt = "F"
            log_dt_finding_tool(
                session_id=str(new_session_context.id_sesion),
                client_id=str(new_session_context.id_cliente),
                finding_type="falla_memoria_detectada",
                description="Cliente indica falla de memoria. DT activa TT.",
                tags=["falla_memoria", "estrat_dt", "tt_activado"]
            )
        else:
            new_session_context.think_tool_activado = False
            new_session_context.motivo_tt = None

        # 2. Avance de fase
        if (new_session_context.fase_actual == "Inicio_Sesion" and 
            "identificar_tema_principal" in new_session_context.criterios.get("objetivo_inicial", "") and 
            len(new_session_context.interacciones_recientes) > 2):
            
            new_session_context.criterios["objetivo_inicial"] = "tema_identificado"
            new_session_context.fase_actual = "Desarrollo_Sesion"
            log_dt_finding_tool(
                session_id=str(new_session_context.id_sesion),
                client_id=str(new_session_context.id_cliente),
                finding_type="avance_fase",
                description="Fase cambiada a Desarrollo_Sesion. Tema principal identificado.",
                tags=["fase_sesion", "estrat_dt"]
            )

        # 3. Actualizar pautas priorizadas
        if new_session_context.fase_actual == "Desarrollo_Sesion" and new_session_context.criterios.get("foco") == "manejo_emocional":
            new_session_context.pautas_priorizadas = ["ICF-3.1_manejo_emocional", "ICF-4.2_resp_profunda", "Gestalt-1.0_conciencia_corporal"]
        elif new_session_context.fase_actual == "Desarrollo_Sesion":
            new_session_context.pautas_priorizadas = ["ICF-1.1_escucha_activa", "ICF-2.0_preg_abiertas", "ICF-5.0_desafiar_creencias"]
        else:
            new_session_context.pautas_priorizadas = []

        update_session_context_tool(str(new_session_context.id_sesion), str(new_session_context.id_cliente), new_session_context.model_dump())
        print(f"[DT_AGENT]: Estrategia del turno decidida. TT activado: {new_session_context.think_tool_activado} (Motivo: {new_session_context.motivo_tt})")
        
        return new_session_context

# Instanciar el agente DT con su prompt
dt_agent_instance = DtAgent(
    name="dt_master",
    instruction=dt_prompt_content,
    model="gemini-1.5-pro"
)

print("\\nAgente DT (DtAgent) definido y configurado exitosamente con SessionContext Pydantic real.")
'''

# Escribir el archivo actualizado
with open('/home/jupyter/Zenda_ADK/agents/dt_agent.py', 'w') as f:
    f.write(new_dt_content)
    
print("✅ dt_agent.py actualizado con SessionContext Pydantic real!")
print("✅ Eliminado placeholder SessionContext")
print("✅ Agregado import desde schemas")
print("✅ Actualizado para usar .model_dump() y .model_copy()")