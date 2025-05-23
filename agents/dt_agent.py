from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.agent import AgentResult # Para AgentResult
from google.adk.agent_builder import AgentBuilder
from google.adk.function_tool import FunctionTool
from core.utils.prompt_utils import read_prompt_file
import json # Necesario para manejar JSON en el SessionContext

# --- Importar modelos Pydantic (AÚN NO CREADOS, SE HARÁ EN PASOS POSTERIORES) ---
# En la fase de volcado de modelos Pydantic, crearemos models/session_context.py
# Por ahora, para que el código compile y sea usable, definimos una clase placeholder.
class SessionContext:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    def to_dict(self):
        # Asegurarse de que sub-diccionarios/objetos también se conviertan si SessionContext es complejo
        data = {}
        for k, v in self.__dict__.items():
            if isinstance(v, SessionContext): # Ejemplo para sub-contextos
                data[k] = v.to_dict()
            elif isinstance(v, dict): # Para diccionarios genéricos como 'criterios'
                data[k] = v
            elif hasattr(v, 'isoformat'): # Para objetos datetime.date, datetime.datetime
                data[k] = v.isoformat()
            else:
                data[k] = v
        return data

    @staticmethod
    def from_dict(data):
        # Lógica para reconstruir el objeto desde un diccionario, manejando sub-objetos si aplica.
        # Para el placeholder, una creación directa es suficiente.
        return SessionContext(**data)

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
    print(f"DEBUG: Llamada a update_session_context_tool para sesión {session_id}, cliente {client_id} con datos: {json.dumps(context_data)}")
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
        print(f"\n[DT_AGENT]: Iniciando contexto para cliente {client_id}, sesión {session_id}...")
        
        # 1. Recuperar datos del cliente (simulando tool call)
        client_data = retrieve_client_data_tool(client_id)

        # 2. Asegurar que Context Caching esté poblado (placeholder)
        print("[DT_AGENT]: Asegurando que Context Caching esté poblado (lógica placeholder)...")
        # TODO: Implementar lógica de CC aquí (Paso 5)
        
        # 3. Preparar SessionContext inicial
        initial_context_data = {
            "id_cliente": client_id,
            "id_sesion": session_id,
            "fase_actual": "Inicio_Sesion", # Siempre empieza en inicio
            "modo_asistencia": "Integral", # Valor por defecto para inicio de sesión
            "guion_dt": "Exploración inicial del problema del cliente para establecer el acuerdo de sesión.",
            "acuerdo_sesion": None, # Se definirá con el cliente
            "criterios": {"foco": "rapport", "objetivo_inicial": "identificar_tema_principal"},
            "pautas_priorizadas": ["ICF-1.1_escucha_activa", "ICF-2.0_preg_abiertas"], # Pautas iniciales
            "resumen_memoria_larga": client_data.get("resumen_memoria_larga"),
            "interacciones_recientes": [{"actor": "cliente", "text": initial_input}], # Primera interacción
            "preferencias_usuario": client_data.get("preferencias", {}),
            "especialidad_principal": "ICF", # Placeholder, DT podría decidir
            "especialidades_secundarias": ["Ontología", "Gestalt"], # Placeholder
            "ciclo_rotativo_actual": None, # Solo si es modo rotativo
            "think_tool_activado": False, # DT decide esto en cada turno
            "motivo_tt": None # Motivo si TT activado
        }
        
        session_context = SessionContext.from_dict(initial_context_data)
        update_session_context_tool(session_context.id_sesion, session_context.id_cliente, session_context.to_dict()) # Simula actualización
        print("[DT_AGENT]: Contexto de sesión inicial preparado y actualizado.")
        
        return session_context

    # Este método simula la lógica turno a turno del DT (será parte de un AgentBuilder)
    def decide_turn_strategy(self, current_session_context: SessionContext, user_input: str, recent_events: list = None) -> SessionContext:
        """
        Lógica del DT para decidir la estrategia turno a turno.
        """
        print(f"\n[DT_AGENT]: Decidiendo estrategia para el turno. Fase actual: {current_session_context.fase_actual}")
        
        # Aquí iría el razonamiento del LLM del DT (con dt_prompt_content como instrucción)
        # para analizar el user_input, recent_events y current_session_context.
        # Por simplicidad, se muestra lógica directa aquí, no la llamada al LLM.

        # Actualizar SessionContext para el turno
        new_session_context_data = current_session_context.to_dict() # Convertir a dict para modificar
        new_session_context = SessionContext.from_dict(new_session_context_data) # Crear nuevo objeto a partir de dict para trabajar
        
        # --- Lógica de ejemplo de decisión del DT (simulando razonamiento LLM) ---
        # 1. Detección de tema sensible o falla de memoria para activar Think Tool
        think_tool_activated_in_turn = False
        motivo_tt_in_turn = None

        if "ansiedad" in user_input.lower() or "estrés" in user_input.lower() or \
           "miedo" in user_input.lower() or "depresion" in user_input.lower(): # Simplificación de detección de tema sensible
            new_session_context.think_tool_activado = True
            new_session_context.motivo_tt = "S" # Sensible
            think_tool_activated_in_turn = True
            motivo_tt_in_turn = "S"
            if "foco" not in new_session_context.criterios or new_session_context.criterios.get("foco") != "manejo_emocional":
                new_session_context.criterios["foco"] = "manejo_emocional"
                new_session_context.guion_dt = "Explorar y validar emociones, buscando estrategias de manejo."
                log_dt_finding_tool(
                    session_id=new_session_context.id_sesion,
                    client_id=new_session_context.id_cliente,
                    finding_type="ajuste_estrategia_tema_sensible",
                    description=f"Tema sensible detectado ('{user_input}'). DT ajusta foco y activa TT.",
                    tags=["tema_sensible", "estrat_dt", "tt_activado"]
                )
        elif "olvidaste" in user_input.lower() or "no recuerdas" in user_input.lower(): # Detección de falla de memoria
            new_session_context.think_tool_activado = True
            new_session_context.motivo_tt = "F" # Falla
            think_tool_activated_in_turn = True
            motivo_tt_in_turn = "F"
            log_dt_finding_tool(
                session_id=new_session_context.id_sesion,
                client_id=new_session_context.id_cliente,
                finding_type="falla_memoria_detectada",
                description="Cliente indica falla de memoria. DT activa TT.",
                tags=["falla_memoria", "estrat_dt", "tt_activado"]
            )
        else:
            new_session_context.think_tool_activado = False # Si no hay razón, se desactiva por defecto
            new_session_context.motivo_tt = None

        # 2. Avance de fase (ej., si se cumplió el objetivo inicial)
        if new_session_context.fase_actual == "Inicio_Sesion" and "identificar_tema_principal" in new_session_context.criterios.get("objetivo_inicial", "") and len(new_session_context.interacciones_recientes) > 2:
            # Aquí el DT podría decidir basado en el input si el tema principal ya está claro
            # Simulamos que sí después de unas interacciones
            new_session_context.criterios["objetivo_inicial"] = "tema_identificado" # Marca como hecho
            new_session_context.fase_actual = "Desarrollo_Sesion"
            log_dt_finding_tool(
                session_id=new_session_context.id_sesion,
                client_id=new_session_context.id_cliente,
                finding_type="avance_fase",
                description="Fase cambiada a Desarrollo_Sesion. Tema principal identificado.",
                tags=["fase_sesion", "estrat_dt"]
            )

        # 3. Actualizar pautas priorizadas (ejemplo simple según fase o foco)
        if new_session_context.fase_actual == "Desarrollo_Sesion" and new_session_context.criterios.get("foco") == "manejo_emocional":
            new_session_context.pautas_priorizadas = ["ICF-3.1_manejo_emocional", "ICF-4.2_resp_profunda", "Gestalt-1.0_conciencia_corporal"]
        elif new_session_context.fase_actual == "Desarrollo_Sesion":
            new_session_context.pautas_priorizadas = ["ICF-1.1_escucha_activa", "ICF-2.0_preg_abiertas", "ICF-5.0_desafiar_creencias"]
        else: # Fase de inicio o cierre
            new_session_context.pautas_priorizadas = [] # Las pautas específicas de fase se manejarán en esa sección

        # 4. Ajustar modo de asistencia (ejemplo: si DT detecta necesidad de rotación, cambiaría el modo)
        # Esta lógica sería más compleja e involucraría más razonamiento del DT.
        # Por ejemplo, si el cliente muestra alta resistencia y un tema complejo, DT podría sugerir "Rotativo"

        update_session_context_tool(new_session_context.id_sesion, new_session_context.id_cliente, new_session_context.to_dict()) # Simula actualización
        print(f"[DT_AGENT]: Estrategia del turno decidida. TT activado: {new_session_context.think_tool_activado} (Motivo: {new_session_context.motivo_tt})")
        
        # En un sistema ADK real, el DT devolvería el contexto modificado.
        return new_session_context

# Instanciar el agente DT con su prompt
dt_agent_instance = DtAgent(
    name="dt_master",
    instruction=dt_prompt_content,
    model="gemini-1.5-pro" # O el modelo específico para DT
)

print("\nAgente DT (DtAgent) definido y configurado exitosamente con lógica completa.")
