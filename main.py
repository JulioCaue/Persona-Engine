#import live_mouth as LM
from ai import llm as IA
from translators import text_to_speech as TTS
from translators import speech_to_text as STT
from animation import falar_audio as dublar
from animation import falar_mic
import subprocess
import os

while True:
    subprocess.run('cls' if os.name == 'nt' else 'clear')
    escolha=input("Oque deseja usar?\n\n1- Boca ao vivo\n2- Perguntar IA\n\nEscolha (1/2): ")
    if escolha == "1":
        falar_mic.imitar_fala()
        continue
    else:
        try:
            TTS.voz_para_wav(IA.perguntar_ia(STT.pegar_transcricao()))
            dublar.dublar_audio()
        except KeyboardInterrupt:
            continue