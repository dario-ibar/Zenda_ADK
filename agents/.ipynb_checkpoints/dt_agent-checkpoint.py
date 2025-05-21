from google.adk.agents.llm_agent import LlmAgent

def cargar_prompt(nombre_archivo):
    with open(f"prompts/{nombre_archivo}", "r", encoding="utf-8") as f:
        return f.read()

instruccion = cargar_prompt("dt_instruccion.txt")

dt_agent = LlmAgent(
    name="dt",
    instruction=instruccion,
    tools=[],  # por ahora vacío
)
