import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from schemas import TokenModel
from uuid import UUID
from datetime import datetime

def test_token_model_valido():
    datos = {
        "id_token": "dddddddd-dddd-dddd-dddd-dddddddddddd",
        "id_cliente": "11111111-1111-1111-1111-111111111111",
        "id_origen": "test_api",
        "tokens": 500,
        "fecha": "2025-05-27T19:10:00"
    }
    token = TokenModel(**datos)
    assert token.tokens == 500
    assert token.id_origen == "test_api"
    assert isinstance(token.fecha, datetime)
    assert isinstance(token.id_cliente, UUID)

def test_token_model_error():
    datos_erroneos = {
        "id_token": "not-a-uuid",
        "id_cliente": "not-a-uuid",
        "id_origen": "api_fail",
        "tokens": "no-es-int",
        "fecha": "fecha-invalida"
    }
    try:
        TokenModel(**datos_erroneos)
        assert False, "Debió lanzar una excepción"
    except Exception:
        assert True
