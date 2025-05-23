from google.adk.agents.llm_agent import LlmAgent
from core.utils.prompt_utils import read_prompt_file # Importa la nueva función

# Cargar el prompt del Agente DT
try:
    dt_prompt_content = read_prompt_file("dt_system_prompt.md")
except FileNotFoundError as e:
    print(f"Error al cargar prompt de DT: {e}")
    # Aquí puedes decidir cómo manejar el error, ej. usar un prompt por defecto o salir
    dt_prompt_content = "Eres un asistente de IA para DT. Responde de forma básica." # Prompt de fallback
except IOError as e:
    print(f"Error de IO al cargar prompt de DT: {e}")
    dt_prompt_content = "Eres un asistente de IA para DT. Responde de forma básica." # Prompt de fallback


# Definir el Agente DT
dt_agent = LlmAgent(
    name="dt",
    instruction=dt_prompt_content,
    tools=[],  # Las FunctionTools se añadirán en un paso posterior
    # Puedes añadir el modelo aquí si lo necesitas para un test básico,
    # ej. model="gemini-1.5-pro-preview-0506"
)

print("Agente DT configurado exitosamente.")