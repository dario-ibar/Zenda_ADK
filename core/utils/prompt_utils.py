import os

def read_prompt_file(prompt_name: str) -> str:
    """
    Lee el contenido de un archivo de prompt desde la carpeta 'prompts/'.
    """
    # Asegúrate de que la ruta sea relativa a la raíz del proyecto o a donde se ejecuta el script principal.
    # Asumimos que la carpeta 'prompts' está en la raíz del proyecto o accesible desde ella.
    prompt_path = os.path.join("prompts", prompt_name)
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"El archivo de prompt '{prompt_name}' no se encontró en '{prompt_path}'.")
    except Exception as e:
        raise IOError(f"Error al leer el archivo de prompt '{prompt_name}': {e}")
