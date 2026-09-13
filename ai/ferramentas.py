import requests
import serial
import os
from datetime import datetime
bottango_url = "http://localhost:59224"

MUSICAS = [
    "daisy bell",
    "hidden in the sand",
    "hello world",
    "sleeping in the cold below",
    "twist"
]

def tocar_musica(nome: str):
    f"""
    Toca uma musica.
    
    Args:
        nome: Nome da musica.

    Musicas disponiveis:
    cantar_daisy_bell
    cantando_hidden_in_sand
    cantar_hello_world
    cantar_SitCB
    twist

    Returns:
        status da musica, erro ou sucesso.
    """
    arduino_conectado = os.path.exists("/dev/ttyUSB0")
    if arduino_conectado == False:
        raise serial.SerialException("arduino não está conectado.")
    response = requests.put(
        f"{bottango_url}/PlaybackState/",
        json={
            "selectedAnimationName": nome,
            "playbackTimeInMS": 0,
            "isPlaying": True,
        }
    )
    response.raise_for_status()
    return f"Tocando {nome}"

def parar_musica(nome: str):
    f"""
    Para uma musica.
    
    Args:
        nome: Nome da musica.

    Returns:
        Qual musica foi parada.
    """
    arduino_conectado = os.path.exists("/dev/ttyUSB0")
    if arduino_conectado == False:
        raise serial.SerialException
    response = requests.put(
        f"{bottango_url}/PlaybackState/",
        json={
            "selectedAnimationName": nome,
            "playbackTimeInMS": 0,
            "isPlaying": False,
        }
    )
    response.raise_for_status()
    return f"Parando musica {nome}"

def olhar_hora():
    hora = datetime.now().strftime("%H:%M")
    return f"Agora são {hora}"


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "tocar_musica",
            "description": "Toca uma música.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome": {
                        "type": "string",
                        "enum": MUSICAS
                    }
                },
                "required": ["nome"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "parar_musica",
            "description": "Para a música atual.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nome": {
                        "type": "string",
                        "enum": MUSICAS
                    }
                },
                "required": ["nome"]
            }
        }
    },
    
    {
        "type": "function",
        "function": {
            "name": "olhar_hora",
            "description": (
                "Obtém a hora atual do sistema."
                "DEVE ser usada sempre que obter a hora atual for relevante na conversa. "
                "Nunca reutilize horários encontrados no histórico, pois podem estar desatualizados."
            ),
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]


FUNCOES = {
    "tocar_musica": tocar_musica,
    "parar_musica": parar_musica,
    "olhar_hora": olhar_hora,
}