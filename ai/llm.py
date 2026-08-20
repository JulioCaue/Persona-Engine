"""
Serve para gerenciar a comunicação com o modelo por meio do prompt do usuario.
Pode configurar os parametros da comunicação.
"""

from ollama import chat
from ai import history
from logs import log_writer
import os
import threading


def perguntar_ia(
    historico,
    flag_parar: threading.Event):


  """Envia prompt para IA."""

  caminho_arquivo = "ai/prompts/sistema.txt"

  if os.path.exists(caminho_arquivo):
    with open(caminho_arquivo,'r') as f:
      prompt_sistema = f.read()
  
  else: 
    prompt_sistema = ""
    log_writer.write(__name__,"Arquivo de prompt do sistema não foi encontrado.")

  mensagem_final = ""

  resposta = chat(
    model='qwen3:1.7b',
    messages=[
      {'role': 'system', 'content': prompt_sistema},
      *historico
      ],
    stream= True,
    think= None
)
  
  #Serve para que cada letra apareça no momento que for gerada,
  #ao envés de tudo quando a mensagem final estiver pronta
  for chunk in resposta:
    text = chunk["message"]["content"]
    print(text, end="", flush=True)
    mensagem_final += text
    if flag_parar.is_set():
      break
  #passar para proxima linha depois da mensagem.
  print("\n")

  #Salva mensagem da IA no historico também.
  history.add_message_to_history(mensagem_final,"assistant")

  return str(mensagem_final)