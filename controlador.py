"""
Arquivo principal do projeto.

Serve como local de interação do usuario com o projeto. 
Coordena as partes porém não as implementa.
"""

import os
import serial
import threading
import requests
from ai import history
from translators import text_to_speech as TTS
from translators import speech_to_text as STT
from animation import falar_audio as dublar
from animation import falar_mic
from audios import audio_player
from logs import log_writer

#Dicionario util para caso expansão seja necessaria.
tipo_interação = {
1: falar_mic.imitar_fala,
2: STT.pegar_transcricao
# terceiro é tipo é manual, no codigo, por simplicidade.
}

url = "http://127.0.0.1:8000"
flag_falar_audio = True

def trocar_modo_audio(escolha_audio: bool):
    global flag_falar_audio
    if escolha_audio == True:
        flag_falar_audio = True
    else:
        flag_falar_audio = False

def func_falar_audio(resposta_ia,arduino_conectado):
    if flag_falar_audio == True:
        #Transforma resposta em arquivo .wav
        TTS.voz_para_wav(resposta_ia)
        #O movimento da cabeça é independente, então pode ser opcional.
        if arduino_conectado:
            dublar.dublar_audio()
        audio_player.Tocar_Wav()

def controla_modo(
        modo_recebido: int,
        flag_parar_modo: threading.Event,
        input_usuario: str | None
        ) -> None:


    """
    Inicia loop de conversa com a IA.

    Permite o usuario escolha entre conversa por texto ou microfone.
    Ignora arduino caso não esteja conectado.

    Para sair, digitar "sair","exit","quit" na mensagem para IA (volta para o loop principal)
    """

    from ai import llm as IA

    #Verifica se arduino está conectado.
    arduino_conectado = os.path.exists("/dev/ttyUSB0")

    if modo_recebido != 1:
        #Loop para manter conversa de usuario -> ia -> usuario...
        while not flag_parar_modo.is_set():
            if modo_recebido == 2:
                mensagem = tipo_interação[modo_recebido](flag_parar_modo)
            else: mensagem = input_usuario

            if flag_parar_modo.is_set():
                break

            #Mensagens extras para tentar evitar problema visto no historico
            #Talvez seja melhor criar um arquivo de lista negra?
            if (not mensagem) or (mensagem.lower() in ("sair","exit","quit"," thank you.", " .")):
                break

            #Coloca mensagem do usuario no historico
            history.add_message_to_history(mensagem,"user")

            if modo_recebido != 3:
                resposta = {
                    "resposta": mensagem,
                    "autor": "usuario"
                }
                requests.post(
                    f"{url}/receber_mensagem",
                    json=resposta
                )


            try:
                #Dá o historico para a IA e retorna resposta.
                resposta_ia = IA.perguntar_ia(
                    historico = history.pull_history(),
                    flag_parar = flag_parar_modo
                )

                if resposta_ia:
                    func_falar_audio(resposta_ia,arduino_conectado)
                else:
                    flag_parar_modo.set()
                    break

                resposta = {
                    "resposta": resposta_ia,
                    "autor": "ia"
                }
                requests.post(
                    f"{url}/receber_mensagem",
                    json=resposta
                )

                if modo_recebido == 3:
                    break
            
            except Exception as e:
                print(f"Ocorreu um erro: {e}")
                log_writer.write(__name__,f"Ocorreu um erro: {e}")

    #deixando nesse formato para não precisar alterar dicionario de funções.
    else:
        if modo_recebido == 1 and not arduino_conectado:
            raise serial.SerialException
        tipo_interação[modo_recebido](flag_parar_modo)