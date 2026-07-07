from ai import llm as IA
from translators import text_to_speech as TTS
from translators import speech_to_text as STT
from animation import falar_audio as dublar
from animation import falar_mic
from ai import history
import subprocess
import os

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
            escolha_tipo = input("Escolha 1 para conversa por voz ou 2 para conversa por texto")
            try:
                if int(escolha_tipo) == 1:
                    history.add_input_to_history(STT.pegar_transcricao())
                    break
                elif int(escolha_tipo) == 2:
                    history.add_input_to_history(input("Digite algo: "))
                    break
                else:
                    pass
            except ValueError:
                pass
            except Exception as e:
                print(f"Um erro ocorreu: {e}")

        try:
            TTS.voz_para_wav(IA.perguntar_ia(history.pull_history()))
            dublar.dublar_audio()

        except KeyboardInterrupt:
            continue