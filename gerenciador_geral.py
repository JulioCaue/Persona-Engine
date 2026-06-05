#import live_mouth as LM
from TTS_e_STT import sistema_STT as STT
from IA import chamar_IA as IA
from TTS_e_STT import sistema_TTS as TTS
import falar_audio as dublar

#live mouth comentado para evitar erros

while True:
    escolha=input("Oque deseja usar?\n\n1- Boca ao vivo\n2- Perguntar IA\n\nEscolha (1/2): ")
    if escolha == "1":
        try:
            #LM.imitar_fala() removido por enquanto para suprimir mensagens de erro
            pass
        except KeyboardInterrupt:
            continue
    else:
        try:
            TTS.voz_para_wav(IA.perguntar_ia(STT.pegar_transcricao()))
            dublar.dublar_audio()
        except KeyboardInterrupt:
            continue