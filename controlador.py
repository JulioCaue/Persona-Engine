"""
Arquivo principal do projeto.

Serve como local de interação do usuario com o projeto. 
Coordena as partes porém não as implementa.
"""

import os
import serial
import threading
from ai import llm as IA
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

def executar_modo(
        modo_recebido: int,
        flag_parar_modo: threading.Event
        ) -> None:


    """
    Inicia loop de conversa com a IA.

    Permite o usuario escolha entre conversa por texto ou microfone.
    Ignora arduino caso não esteja conectado.

    Para sair, digitar "sair","exit","quit" na mensagem para IA (volta para o loop principal)
    """

    #Verifica se arduino está conectado.
    arduino_conectado = os.path.exists("/dev/ttyUSB0")

    if modo_recebido != 1:
        #Loop para manter conversa de usuario -> ia -> usuario...
        while not flag_parar_modo.is_set():
            if modo_recebido == 2:
                mensagem = tipo_interação[modo_recebido](flag_parar_modo)
            else: mensagem = input("\n\nDigite algo: ")

            if flag_parar_modo.is_set():
                break

            #Mensagens extras para tentar evitar problema visto no historico
            #Talvez seja melhor criar um arquivo de lista negra?
            if not mensagem or mensagem.lower() in ("sair","exit","quit"," thank you.", " ."):
                break

            #Coloca mensagem do usuario no historico
            history.add_message_to_history(mensagem,"user")

            #FALTA TESTAR A PARTIR DAQUI!!!!
            break
            try:
                #Dá o historico para a IA e retorna resposta.
                resposta_ia = IA.perguntar_ia(history.pull_history())

                #Transforma resposta em arquivo .wav
                TTS.voz_para_wav(resposta_ia)

                #O movimento da cabeça é independente, então pode ser opcional.
                if arduino_conectado:
                    dublar.dublar_audio()

                #Toca o arquivo wav criado se o arquivo existir.
                audio_player.Tocar_Wav()
            
            except Exception as e:
                print(f"Ocorreu um erro: {e}")
                log_writer.write(__name__,f"Ocorreu um erro: {e}")

    #deixando nesse formato para não precisar alterar dicionario de funções.
    else:
        if modo_recebido == 1 and not arduino_conectado:
            raise serial.SerialException
        tipo_interação[modo_recebido](flag_parar_modo)