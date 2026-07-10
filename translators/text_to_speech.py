"""
Arquivo responsavel por transformar texto da IA em wav com TTS.
"""

import subprocess
#Faz comando no terminal para evitar erros presentes no linux
def voz_para_wav(resposta_IA, arquivo="audios/audio_output.wav"):
    subprocess.run(
        ['espeak-ng', '-v', 'pt-br', '-s', '140', '-p', '0', '-a', '100',
         '-w', arquivo,
         resposta_IA],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )