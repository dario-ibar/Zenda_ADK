from google.adk.agents.llm_agent import LlmAgent
from core.utils.prompt_utils import read_prompt_file # Importa la función de utilidad

# Cargar el prompt del Agente QA (usaremos un prompt por defecto por ahora)
try:
    # En un paso posterior, diseñaremos el prompt QA
    qa_prompt_content = read_prompt_file("qa_system_prompt.md") # Asumiendo que existirá este archivo
except FileNotFoundError:
    qa_prompt_content = "Eres un Agente de Calidad. Tu rol es auditar las conversaciones de IA."
except IOError as e:
    print(f"Error de IO al cargar prompt de QA: {e}")
    qa_prompt_content = "Eres un Agente de Calidad. Tu rol es auditar las conversaciones de IA."


# Definir el Agente QA
qa_agent = LlmAgent(
    name="qa",
    instruction=qa_prompt_content,
    tools=[],  # Las FunctionTools se añadirán en un paso posterior
    # Puedes añadir el modelo aquí si lo necesitas para un test básico,
    # ej. model="gemini-1.5-pro-preview-0506"
)

print("Agente QA configurado exitosamente.")
