from datetime import datetime
import os

caminho_pastas = "logs/errors/"
ftype = ".txt"
agora = datetime.now()
dia_hoje = agora.strftime("%d-%m-%Y")
hora_agora = agora.strftime("%H:%M")

caminho_arquivo = f"{caminho_pastas}{dia_hoje}{ftype}"

def ler_erros():
    """
    Lê todos os erros no arquivo de erros do dia.
    """
    with open(caminho_arquivo,"r") as file:
        return file.read()

def write(error_line):
    """
    Salva erros para um arquivo de texto.
    Arquivos de texto diferentes para cada dia.
    Salva no fim de arquivo caso existente.
    Precisa apenas da linha de erro.
    """

    #garante que variavel exista (e sem \n feio)
    erros_no_arquivo = ler_erros() if os.path.exists(caminho_arquivo) else ""

    #Escreve cada tipo de erro apenas uma vez por minuto.
    with open(caminho_arquivo,"a") as file:
        if f"[{hora_agora}]: {error_line}" not in erros_no_arquivo:
            file.write(f"[{hora_agora}]: {error_line}\n\n")