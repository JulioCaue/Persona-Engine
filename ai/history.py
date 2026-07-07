import json

local_arquivo = "ai/prompts/conversa/historico.json"

def add_input_to_history(input_do_usuario):
    with open(local_arquivo,"r") as file:
        data = json.load(file)
        input = {'role': 'user', 'content': input_do_usuario}

    data.append(input)
    
    with open(local_arquivo,"w") as file:
        json.dump(data, file, indent=4)

def pull_history():
    with open(local_arquivo,"r") as file:
        if file is None:
            return None
        else:
            return json.load(file)