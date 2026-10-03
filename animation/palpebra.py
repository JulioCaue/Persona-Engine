import requests
import time
import threading

def piscar():
    response = requests.put(
        "http://localhost:59224/ControlInput/",
        json={
            "identifier": "MexerPalpebra",
            "value": 0.0
        }
    )

    response.raise_for_status()

    time.sleep(0.3)

    response = requests.put(
        "http://localhost:59224/ControlInput/",
        json={
            "identifier": "MexerPalpebra",
            "value": 0.8
        }
    )

    response.raise_for_status()

    t = threading.Timer(4, piscar); t.daemon = True; t.start()