from google.adk.agents.llm_agent import LlmAgent
from core.utils.prompt_utils import read_prompt_file # Importa la función de utilidad

# Cargar el prompt del Agente Zenda
try:
    zenda_prompt_content = read_prompt_file("zenda_system_prompt.md")
except FileNotFoundError as e:
    print(f"Error al cargar prompt de Zenda: {e}")
    # Aquí puedes decidir cómo manejar el error, ej. usar un prompt por defecto o salir
    zenda_prompt_content = "Eres un asistente de IA conversacional básico." # Prompt de fallback
except IOError as e:
    print(f"Error de IO al cargar prompt de Zenda: {e}")
    zenda_prompt_content = "Eres un asistente de IA conversacional básico." # Prompt de fallback


# Definir el Agente Zenda
zenda_agent = LlmAgent(
    name="zenda",
    instruction=zenda_prompt_content,
    tools=[],  # Las FunctionTools se añadirán en un paso posterior
    # Puedes añadir el modelo aquí si lo necesitas para un test básico,
    # ej. model="gemini-1.5-pro-preview-0506"
)

print("Agente Zenda configurado exitosamente.")
