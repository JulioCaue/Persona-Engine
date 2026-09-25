import requests
import librosa
import numpy as np
import pyaudio
import time
from logs import log_writer

# --- variaveis de audio ---
ARQUIVO_AUDIO = "audios/audio_output.wav"
TAMANHO_CHUNK = 1024

# --- variaveis de movimento ---
boca_min_pos = 40
boca_max_pos = 140


def sincronizar_com_audio():
    """
    move a boca conforme um arquivo de audio pré-criado.
    """

    y, sr = librosa.load(ARQUIVO_AUDIO, sr=44100)

    AUDIO_FORMAT = pyaudio.paFloat32
    CHANNELS = 1
    RATE = int(sr)

    RMS_MAX = 0.3
    ALPHA = 0.6
    angulo_anterior = float(boca_min_pos)

    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=AUDIO_FORMAT, 
        channels= CHANNELS, 
        rate= RATE, 
        output=True,frames_per_buffer=TAMANHO_CHUNK
    )

    frame_start = 0

    # --- inicio da conexão ---
    try:
        while frame_start < len(y):
            chunk_audio = y[frame_start : frame_start + TAMANHO_CHUNK]
            
            if len(chunk_audio) < TAMANHO_CHUNK:
                chunk_audio = np.pad(
                    chunk_audio, (0, TAMANHO_CHUNK - len(chunk_audio))
                )

            rms = np.sqrt(np.mean(chunk_audio**2))

            if np.isnan(rms):
                rms = 0.0

            #suaviza o angulo atual para movimentos menos brutos
            angulo_calculado = boca_min_pos + (rms / RMS_MAX) * (boca_max_pos - boca_min_pos)
            angulo_suavizado = ALPHA * angulo_calculado + (1 - ALPHA) * angulo_anterior
            angulo_anterior = angulo_suavizado
            angulo_final = int(round(angulo_suavizado))

            #transforma angulo final em valor que bottango entende (entre 0.0 e 1.0)
            valor_angulo_final = (angulo_final - boca_min_pos) / (boca_max_pos - boca_min_pos)
            valor_angulo_final = max(0.0, min(1.0, valor_angulo_final))

            #Envia angulos direto para o bottango pois o codigo do arduino que observa a porta serial é substituido quando uma animação do arduino é tocada.
            print(f"Valor da boca: {valor_angulo_final}")
            """respose = requests.put(
                "http://localhost:59224/ControlInput/",
                json={
                    "identifier": "moverBoca",
                    "value": valor_angulo_final
                }
            )

            respose.raise_for_status()"""

            stream.write(chunk_audio.astype(np.float32).tobytes())

            frame_start += TAMANHO_CHUNK

            return frame_start

    except Exception as e:
        log_writer.write(__name__,e)

    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()

#trazer parar_modo:threading.Event
def sincronizar_com_microfone():
    """
    Envia comandos de servo para arduino com base em volume da voz em loop até detectar troca de flag.
    """

    #limite dos servos:
    # boca: 170, 40
    # olhos: 150 (esquerda), 35 (direita)
    # palpebras: 160 (abertas), 40 (fechada)

    TAMANHO_CHUNK = 128
    AUDIO_FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000


    #RMS_MAX = 0.3
    ALPHA = 0.8

    angulo_anterior = float(boca_min_pos)
    valor_bottango_anterior = None

    pa=pyaudio.PyAudio()
    stream = pa.open(
        format=AUDIO_FORMAT,
        channels=CHANNELS,
        rate = RATE,
        input=True,
        frames_per_buffer=TAMANHO_CHUNK
    )

    try:
        print("Microfone ativo. Fale para mover boca... (ctrl + c para parar)")

        while True:
            #print(f"entrou no loop com flag {parar_modo.is_set()}")
            #ler data binaria do audio da stream do microfone
            data = stream.read(TAMANHO_CHUNK,exception_on_overflow=False)
            
            #converter data binaria para float para evitar overflow
            audio_data=np.frombuffer(data,dtype=np.int16).astype(np.float32)

            #computar raiz quadrada media para determinar a amplitude do volume
            rms = np.sqrt(np.mean(audio_data**2))

            #proteçao contra audio silencioso ou corrompido 
            if np.isnan(rms):
                rms=0.0

            # -- logica de mapeamento --
            #ajustar o volume maximo dependendo da sensibilidade do microfone
            volume_minimo = 50
            volume_max = 500

            if rms <= volume_minimo:
                intensidade = 0

            else:
                intensidade = (rms - volume_minimo) / (volume_max - volume_minimo)
                intensidade = max(0.0, min(1.0, intensidade))

            angulo_calculado = boca_min_pos + intensidade * (boca_max_pos - boca_min_pos)

            #suaviza o angulo atual para movimentos menos brutos
            angulo_suavizado = ALPHA * angulo_calculado + (1 - ALPHA) * angulo_anterior

            angulo_anterior = angulo_suavizado

            angulo_final = round(angulo_suavizado)

            #transforma angulo final em valor que bottango entende (entre 0.0 e 1.0)
            valor_bottango_final = round((angulo_final - boca_min_pos) / (boca_max_pos - boca_min_pos),3)

            valor_bottango_final = max(0.0, min(1.0, valor_bottango_final))

            if not valor_bottango_anterior or abs(valor_bottango_anterior - valor_bottango_final) > 0.07:
                print(f"Valor da boca: {valor_bottango_final}")
                """respose = requests.put(
                    "http://localhost:59224/ControlInput/",
                    json={
                        "identifier": "moverBoca",
                        "value": valor_bottango_final
                    }
                )

                respose.raise_for_status()"""

                valor_bottango_anterior = valor_bottango_final

            time.sleep(0.05)

    except Exception as e:
        log_writer.write(__name__,e)

    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()