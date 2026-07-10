from ai import llm as IA
from translators import text_to_speech as TTS
from translators import speech_to_text as STT
from animation import falar_audio as dublar
from animation import falar_mic
from audios import audio_player
from ai import history
import subprocess
import os
import serial
from logs import log_writer

arduino_conectado = True

while True:
    subprocess.run('cls' if os.name == 'nt' else 'clear')
    escolha=input("Oque deseja usar?\n\n1- Boca ao vivo\n2- Perguntar IA\n\nEscolha (1/2): ")
    if escolha == "1":
        try:
            falar_mic.imitar_fala()
        except KeyboardInterrupt:
            continue

    else:
        while True:
            escolha_tipo = input("Escolha 1 para conversa por voz ou 2 para conversa por texto: ")
            try:
                escolha_tipo = int(escolha_tipo)
                if escolha_tipo not in (1,2):
                    print("Escolha apenas 1 ou 2")
                    continue
                else: 
                    break
            except ValueError:
                print("Apenas numeros")
                pass
            except Exception as e:
                print(f"Um erro ocorreu: {e}")


        while True:
            if int(escolha_tipo) == 1:
                history.add_message_to_history(STT.pegar_transcricao(),"user")

            elif int(escolha_tipo) == 2:
                history.add_message_to_history(input("\n\nDigite algo: "),"user")

            try:
                TTS.voz_para_wav(IA.perguntar_ia(history.pull_history()))
                audio_player.Tocar_Wav()
                try:
                    if arduino_conectado:
                        dublar.dublar_audio()
                except serial.SerialException:
                    arduino_conectado = False
                    continue

            except KeyboardInterrupt:
                print("Encerrado pelo usuario.")
                break
            
            except Exception as e:
                print(f"Ocorreu um erro: {e}")
                log_writer.write(f"Ocorreu um erro: {e}")
                