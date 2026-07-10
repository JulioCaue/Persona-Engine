from datetime import datetime

def write(error_line):
    """
    Salva erros para um arquivo de texto.
    Arquivos de texto diferentes para cada dia.
    Salva no fim de arquivo caso existente.
    """
    caminho_pastas = "logs/errors/"
    ftype = ".txt"
    agora = datetime.now()
    dia_hoje = agora.strftime("%d-%m-%Y")
    hora_agora = agora.strftime("%H:%M:%S")

    with open(f"{caminho_pastas}{dia_hoje}{ftype}","a") as file:
        file.write(f"[{hora_agora}]: {error_line}\n")