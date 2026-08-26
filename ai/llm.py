"""
Serve para gerenciar a comunicação com o modelo por meio do prompt do usuario.
Pode configurar os parametros da comunicação.
"""

from ollama import chat
from ai import history
from logs import log_writer
from ai import ferramentas
from ai.prompts.sistema import system_prompts
import os
import threading

musica_atual: str

musicas = [
    "daisy bell",
    "hidden in the sand",
    "hello world",
    "sleeping in the cold below",
    "twist"
]

caminho_prompt_sistema = "ai/prompts/sistema/system_prompts.py"

if os.path.exists(caminho_prompt_sistema):
    with open(caminho_prompt_sistema,'r') as f:
        prompt_sistema = system_prompts.system_prompt()

else: 
    prompt_sistema = ""


tocar_musica_tool = {
    "type": "function",
    "function": {
        "name": "tocar_musica",
        "description": """
        Toca uma música.
        Interprete o que o usuário quis dizer e escolha a música
        disponível que mais corresponde ao pedido, mesmo que ele
        escreva o nome de forma diferente ou com pequenos erros.
        """,
        "parameters": {
            "type": "object",
            "properties": {
                "nome": {
                    "type": "string",
                    "enum": musicas
                }
            },
            "required": ["nome"]
        }
    }
}

parar_musica_tool = {
    "type": "function",
    "function": {
        "name": "parar_musica",
        "description": """
        Pare uma música.
        Interprete o que o usuário quis dizer e escolha a ultima música
        que o usuario pediu.
        """,
        "parameters": {
            "type": "object",
            "properties": {
                "nome": {
                    "type": "string",
                    "enum": musicas
                }
            },
            "required": ["nome"]
        }
    }
}

def chamada_ia(prompt_sistema,historico):
    """faz a chamada para a IA"""
    return chat(
    model='qwen2.5:3b',
    messages=[
        {'role': 'system', 'content': prompt_sistema},
        {'role': 'system', 'content': system_prompts.test_prompt()},
        *historico,
        ],
    think= False,
    tools=[tocar_musica_tool,parar_musica_tool],
    keep_alive="5m"
    )

def perguntar_ia(
    historico,
    flag_parar: threading.Event):


    """gerencia retorno da resposa da IA."""

    if not prompt_sistema:
        erro = "Arquivo de prompt do sistema não foi encontrado."
        log_writer.write(__name__,erro)
        print(erro)
        return
    
    resposta = chamada_ia(prompt_sistema,historico)

    if resposta.message.tool_calls:
        for chamada in resposta.message.tool_calls:
            try:
                print("Ferramenta escolhida:", chamada.function.name)
                print("Argumentos:", chamada.function.arguments)
                if chamada.function.name:
                    nome_funcao = chamada.function.name
                    funcao = getattr(ferramentas, nome_funcao)
                    argumentos = chamada.function.arguments
                    resultado = funcao(**argumentos)
                    print("Resultado:", resultado)
            except Exception as e:
                mensagem_de_erro = (
                    f"Erro na ferramenta '{chamada.function.name}' com argumentos {chamada.function.arguments}: {e}\n"
                )
            input = {'role': 'tool', 'content': mensagem_de_erro}
            historico.append(input)
            resposta = chamada_ia(prompt_sistema,historico)
            history.add_message_to_history(mensagem_de_erro, "tool")
            print ("passou de resposta no erro")

    print (f"resposta atual:  {resposta.message.content}\n\n")
    if not flag_parar.is_set() and resposta.message.content:
        mensagem_final = resposta.message.content
        print(f"\n\nchegou em mensagem final: {mensagem_final}\n\n")
        #Salva mensagem da IA no historico também.
        history.add_message_to_history(mensagem_final,"assistant")

        return str(mensagem_final)