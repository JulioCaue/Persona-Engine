#import live_mouth as LM
import sistema_STT as STT
import ia_teste as IA

#live mouth comentado para evitar erros

while True:
    escolha=input("Oque deseja usar?\n\n1- Boca ao vivo\n2- Perguntar IA\n\nEscolha (1/2): ")
    if escolha == "1":
        try:
            #LM.imitar_fala()
            pass
        except KeyboardInterrupt:
            continue
    else:
        try:
            input_do_usuario=STT.pegar_transcricao()
            IA.perguntar_ia(input_do_usuario)
        except KeyboardInterrupt:
            continue