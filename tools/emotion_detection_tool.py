from google.adk.tools import FunctionTool
from typing import Dict, Any, Optional

def emotion_detection_function(input_text: str, audio_bytes: Optional[bytes] = None) -> Dict[str, Any]:
    """
    Detecta la emoción y el tono del input del cliente (texto y/o audio) usando Gemini multimodal.
    
    Args:
        input_text: Texto del mensaje del cliente
        audio_bytes: Datos de audio del mensaje del cliente (opcional)
        
    Returns:
        Dict[str, Any]: Diccionario con la emoción detectada y su nivel
    """
    print(f"\n[EMOTION_TOOL]: Analizando texto: '{input_text[:50]}...'")
    if audio_bytes:
        print("                 Audio también recibido (simulando análisis)")

    # Simulación basada en palabras clave
    emocion = "neutral"
    nivel = "bajo"
    tono = "informativo"

    input_lower = input_text.lower()
    
    if any(word in input_lower for word in ["frustrado", "agotado", "no puedo", "harto"]):
        emocion = "frustracion"
        nivel = "alto"
        tono = "pesimista"
    elif any(word in input_lower for word in ["feliz", "alegre", "contento", "bien"]):
        emocion = "alegria"
        nivel = "medio"
        tono = "positivo"
    elif any(word in input_lower for word in ["miedo", "ansioso", "nervioso", "preocupado"]):
        emocion = "ansiedad"
        nivel = "alto"
        tono = "nervioso"

    resultado = {
        "emocion": emocion, 
        "nivel": nivel, 
        "tono_general": tono,
        "confianza": 0.8
    }
    
    print(f"       -> EMOCIÓN DETECTADA: {resultado}")
    return resultado

# Crear FunctionTool ADK
emotion_detection_tool = FunctionTool(emotion_detection_function)
