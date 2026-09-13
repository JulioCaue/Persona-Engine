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

caminho_prompt_sistema = "ai/prompts/sistema/system_prompts.py"

if os.path.exists(caminho_prompt_sistema):
    with open(caminho_prompt_sistema,'r') as f:
        prompt_sistema = system_prompts.system_prompt()

else: 
    prompt_sistema = ""

def chamar_ia(prompt_sistema, historico, tools = None):
    """faz a chamada para a IA"""
    if tools == None:
        tools = ferramentas.TOOLS
    return chat(
    model='qwen2.5:3b',
    messages=[
        {'role': 'system', 'content': prompt_sistema},
        {'role': 'system', 'content': system_prompts.test_prompt()},
        *historico,
        ],
    think= False,
    tools = tools,
    keep_alive="5m"
    )

def gerenciar_ia(
    historico,
    flag_parar: threading.Event):


    """gerencia retorno da resposa da IA."""

    tool_calls = []

    if not prompt_sistema:
        erro = "Arquivo de prompt do sistema não foi encontrado."
        log_writer.write(__name__,erro)
        print(erro)
        return str(f"Ocorreu um erro com o prompt de sistema: {erro}")
    
    resposta = chamar_ia(prompt_sistema,historico)

    if resposta.message.tool_calls:
        for chamada in resposta.message.tool_calls:
            try:
                if chamada.function.name:
                    nome_funcao = chamada.function.name
                    funcao = ferramentas.FUNCOES.get(nome_funcao)
                    argumentos = chamada.function.arguments
                    if funcao is not None:
                        resultado = funcao(**argumentos)
                    else:
                        raise IndexError("Essa funcao nao foi encontrada, ou nao existe.")
                    
            except Exception as e:
                resultado = (
                    f"Erro na ferramenta '{chamada.function.name}' com argumentos {chamada.function.arguments}: {e}\n"
                )
                log_writer.write(__name__,resultado)

            tool_calls.append( {
                "type": "function",
                "function": {
                "name": nome_funcao,
                "arguments": argumentos
                }
            })

        history.add_tool_usage_to_history(tool_calls)
        history.add_message_to_history(resultado,"tool")
        historico = history.pull_history()
        resposta = chamar_ia(prompt_sistema,historico)


    if not flag_parar.is_set() and resposta.message.content:
        ai_output = resposta.message.content
        print(f"\n\nchegou em mensagem final: {ai_output}\n\n")
        #Salva mensagem da IA no historico também.
        history.add_message_to_history(ai_output,"assistant")

        return str(ai_output)