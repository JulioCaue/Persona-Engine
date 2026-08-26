import requests
import serial
import os
bottango_url = "http://localhost:59224"

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