import json
import os

local_arquivo = "ai/prompts/conversa/historico.json"

def add_message_to_history(input,origem):
    if not os.path.exists(local_arquivo):
        with open(local_arquivo,"w",encoding="utf-8") as file:
            json.dump([], file, ensure_ascii=False, indent=4)

    with open(local_arquivo,"r",encoding="utf-8") as file:
        data = json.load(file)

    input = {'role': origem, 'content': input}

    data.append(input)
    
    with open(local_arquivo,"w",encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def pull_history():
    with open(local_arquivo,"r",encoding="utf-8") as file:
        if file is None:
            return None
        else:
            return json.load(file)