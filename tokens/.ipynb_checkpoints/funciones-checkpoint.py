# tokens/funciones.py
from schemas import TokenModel

def guardar_token_en_sistema(datos: dict) -> TokenModel:
    token = TokenModel(**datos)
    print(f"✔️ Guardado: {token.id_origen}, tokens: {token.tokens}")
    return token
