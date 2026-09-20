import requests
import librosa
import numpy as np
import pyaudio
import threading
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

    RMS_MAX = 0.3
    ALPHA = 0.6
    angulo_anterior = float(boca_min_pos)

    y, sr = librosa.load(ARQUIVO_AUDIO, sr=44100)

    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paFloat32, channels=1, rate=int(sr), output=True,frames_per_buffer=TAMANHO_CHUNK
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
            respose = requests.put(
                "http://localhost:59224/ControlInput/",
                json={
                    "identifier": "moverBoca",
                    "value": valor_angulo_final
                }
            )

            respose.raise_for_status()

            stream.write(chunk_audio.astype(np.float32).tobytes())

            frame_start += TAMANHO_CHUNK

    except Exception as e:
        log_writer.write(__name__,e)

    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()


def sincronizar_com_microfone(parar_modo:threading.Event):
    """
    Envia comandos de servo para arduino com base em volume da voz em loop até detectar troca de flag.
    """

    #limite dos servos:
    # boca: 170, 40
    # olhos: 150 (esquerda), 35 (direita)
    # palpebras: 160 (abertas), 40 (fechada)

    CHUNK_SIZE = 128
    AUDIO_FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    boca_min_pos = 40
    boca_max_pos = 170

    THRESHOLD_ABRIR  = 140
    ALPHA = 0.15

    angulo_anterior = float(boca_min_pos)
    boca_aberta = False

    pa=pyaudio.PyAudio()
    stream = pa.open(
        format=AUDIO_FORMAT,
        channels=CHANNELS,
        rate = RATE,
        input=True,
        frames_per_buffer=CHUNK_SIZE
    )

    try:
        print("Microfone ativo. Fale para mover boca... (ctrl + c para parar)")

        while not parar_modo.is_set():
            print(f"entrou no loop com flag {parar_modo.is_set()}")
            #ler data binaria do audio da stream do microfone
            data = stream.read(CHUNK_SIZE,exception_on_overflow=False)
            
            #converter data binaria para float para evitar overflow
            audio_data=np.frombuffer(data,dtype=np.int16).astype(np.float32)

            #computar raiz quadrada media para determinar a amplitude do volume
            rms = np.sqrt(np.mean(audio_data**2))

            #proteçao contra audio silencioso ou corrompido 
            if np.isnan(rms):
                rms=0.0

            # -- logica de mapeamento --
            #ajustar o volume maximo dependendo da sensibilidade do microfone
            max_volume = 250.0

            if not boca_aberta and rms >= THRESHOLD_ABRIR:
                boca_aberta = True
            else:
                boca_aberta = False

            if not boca_aberta:
                servo_angle = boca_min_pos

            else:
                #normalizar volume do som entre 0.0 e 1.0
                normalised_volume = min(rms / max_volume, 1.0)

                #transformar em angulo
                servo_angle = int(boca_min_pos + normalised_volume * (boca_max_pos - boca_min_pos))

            #suaviza o angulo atual para movimentos menos brutos
            angulo_suavizado = ALPHA * servo_angle + (1 - ALPHA) * angulo_anterior
            angulo_anterior = angulo_suavizado
            angulo_final = int(round(angulo_suavizado))

            #transforma angulo final em valor que bottango entende (entre 0.0 e 1.0)
            valor_angulo_final = round(
                (angulo_final - boca_min_pos) / (boca_max_pos - boca_min_pos),
                3 #casas decimais
            )
            valor_angulo_final = max(0.0, min(1.0, valor_angulo_final))

            print(valor_angulo_final)

            if not angulo_anterior or abs(valor_angulo_final - angulo_anterior) > 0.002:
                respose = requests.put(
                    "http://localhost:59224/ControlInput/",
                    json={
                        "identifier": "moverBoca",
                        "value": valor_angulo_final
                    }
                )

                respose.raise_for_status()

    except Exception as e:
        log_writer.write(__name__,e)

    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()