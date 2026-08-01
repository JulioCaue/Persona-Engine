"""
Arquivo responsavel por transformar fala do usuario em texto para IA.
Grava microfone e gera arquivo wav.
"""
from logs import log_writer

#suprimir mensagens de erros do ALSA
from ctypes import cdll, CFUNCTYPE, c_char_p, c_int
_alsa_handler_ref = None
try:
    _HANDLER_TYPE = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
    _alsa_handler_ref = _HANDLER_TYPE(lambda *_: None)  # guardado na global
    cdll.LoadLibrary('libasound.so.2').snd_lib_error_set_handler(_alsa_handler_ref)
except Exception:
    pass

#continua normalmente

import speech_recognition as sr

def pegar_transcricao(parar_modo):
    """
    cria wav a partir de audio captado.
    """
    recognizer = sr.Recognizer()
    TIMEOUT_ESPERAR_FALA = 5
    TEMPO_AJUSTE_AMBIENTE = 3
    TEMPO_MAXIMO_FALA = 50
    TEMPO_FIM_FALA = 2

    try:
        with sr.Microphone() as mic:
            if mic.stream is None:
                raise RuntimeError("O stream do microfone não foi aberto.")

            recognizer.adjust_for_ambient_noise(mic, TEMPO_AJUSTE_AMBIENTE)
            recognizer.pause_threshold = TEMPO_FIM_FALA
            
            print("Ouvindo microfone...\n\n")

            #verifica flag antes e depois de escutar só por garantia
            if parar_modo.is_set():
                return

            audio = recognizer.listen(
                mic,
                timeout= TIMEOUT_ESPERAR_FALA,
                phrase_time_limit = TEMPO_MAXIMO_FALA
            )

            if parar_modo.is_set():
                return

            print("Enviando áudio ao Google...")

            #recognize_google dá erro mas funciona mesmo assim.
            texto = recognizer.recognize_google( # type: ignore[attr-defined]
                audio,
                language="pt-BR",
            )

            return texto

    except sr.WaitTimeoutError:
        log_writer.write(__name__,"Nenhuma fala foi detectada em 5 segundos.")

    except sr.UnknownValueError:
        log_writer.write(__name__,"O Google recebeu o áudio, mas não conseguiu entendê-lo.")

    except sr.RequestError as erro:
        log_writer.write(__name__,f"Erro ao acessar o serviço do Google: {erro}")

    except OSError as erro:
        log_writer.write(__name__,f"Erro ao acessar o microfone: {erro}")