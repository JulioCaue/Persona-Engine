"""
Arquivo principal do projeto.

Serve como local de interação do usuario com o projeto. 
Coordena as partes porém não as implementa.
"""


from ai import llm as IA
from ai import history
from translators import text_to_speech as TTS
from translators import speech_to_text as STT
from animation import falar_audio as dublar
from animation import falar_mic
from audios import audio_player
from logs import log_writer
import subprocess
import os
import serial


def perguntar_ia():


    """
    Inicia loop de conversa com a IA.

    Permite o usuario escolha entre conversa por texto ou microfone.
    Ignora arduino caso não esteja conectado.

    Para sair, digitar "sair","exit","quit" na mensagem para IA (volta para o loop principal)
    """


    arduino_conectado = True
    while True:
        escolha_tipo = input("Escolha 1 para conversa por voz ou 2 para conversa por texto: ")
        try:
            escolha_tipo = int(escolha_tipo)
            if escolha_tipo not in tipos_de_mensagem:
                print("Escolha apenas 1 ou 2.")
                continue
            break
        except ValueError:
            print("Apenas numeros.")
        except Exception as e:
            print(f"Um erro ocorreu: {e}")


    while True:
        mensagem = tipos_de_mensagem[escolha_tipo]()
        if mensagem.lower() in ("sair","exit","quit"):
            break
        history.add_message_to_history(mensagem,"user")

        try:
            TTS.voz_para_wav(IA.perguntar_ia(history.pull_history()))
            audio_player.Tocar_Wav()
            #O movimento da cabeça é idenpendente, então pode ser opcional.
            try:
                if arduino_conectado:
                    dublar.dublar_audio()
            except serial.SerialException:
                arduino_conectado = False
                continue
        
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            log_writer.write(f"Ocorreu um erro: {e}")


tipo_interação = {
    1: falar_mic.imitar_fala,
    2: perguntar_ia
}

tipos_de_mensagem = {
    1: STT.pegar_transcricao,
    2: lambda: input("\n\nDigite algo: ")
}


#Limpar terminal antes do loop e depois do not in por conta de estetica
subprocess.run('cls' if os.name == 'nt' else 'clear')
while True:
    try:
        escolha=input(
        "Olá!\n\nOque deseja usar?\n\n1- Boca ao vivo\n2- Perguntar IA\n\nEscolha (1/2): ")
        if escolha.lower() in ("sair","exit","quit"):
            print("\n\nSaindo...")
            break
        if escolha not in tipo_interação:
            subprocess.run('cls' if os.name == 'nt' else 'clear')
            print("Opção invalida.\n")
            continue
        tipo_interação[int(escolha)]()

    except ValueError:
        print("Digite apenas numeros.")
    except KeyboardInterrupt:
        print("\n\nSaindo...")
        break