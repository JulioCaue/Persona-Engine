"""
Gerencia o historico de conversa com IA. 

Esse arquivo é responsavel por salvar mensagens no historico
e as retornar no formato esperado para o modelo.
"""

import json
import os
from datetime import datetime

local_arquivo = "ai/prompts/conversa/historico.json"

def add_message_to_history(input,origem):
    """Adiciona mensagem ao arquivo de historico."""
    if not os.path.exists(local_arquivo):
        with open(local_arquivo,"w",encoding="utf-8") as file:
            json.dump([], file, ensure_ascii=False, indent=4)

    with open(local_arquivo,"r",encoding="utf-8") as file:
        data = json.load(file)

    data_atual = datetime.now()
    data_atual = (
        f"{data_atual.day}/{data_atual.month}/{data_atual.year}, {data_atual.hour}:{data_atual.minute}"
    )

    input = (f"Horario da mensagem: {data_atual}\n\nMensagem: {input}")
    input = {'role': origem, 'content': input}

    data.append(input)
    
    with open(local_arquivo,"w",encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def pull_history():
    """retorna historico completo"""
    if os.path.exists(local_arquivo):
        with open(local_arquivo,"r",encoding="utf-8") as file:
            return json.load(file)
    else:
        return None