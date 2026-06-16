#import live_mouth as LM
from ai import llm as IA
from translators import text_to_speech as TTS
from translators import speech_to_text as STT
from animation import falar_audio as dublar

#live mouth removido por enquanto para evitar erros

while True:
    escolha=input("Oque deseja usar?\n\n1- Boca ao vivo\n2- Perguntar IA\n\nEscolha (1/2): ")
    if escolha == "1":
        try:
            pass #removido por enquanto para lidar com mensagens de erro depois
        except KeyboardInterrupt:
            continue
    else:
        try:
            TTS.voz_para_wav(IA.perguntar_ia(STT.pegar_transcricao()))
            dublar.dublar_audio()
        except KeyboardInterrupt:
            continue