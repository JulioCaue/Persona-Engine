"""
Serve para gerenciar a comunicação com o modelo por meio do prompt do usuario.
Pode configurar os parametros da comunicação.
"""

from ollama import chat
from ai import history

with open("ai/prompts/sistema.txt",'r') as f:
  prompt_sistema = f.read()


def perguntar_ia(historico):
  """Envia prompt para IA."""
  mensagem_final = ""
  resposta = chat(
    model='qwen3:1.7b',
    messages=[
      {'role': 'system', 'content': prompt_sistema},
      *historico
      ],
    stream= True,
    think= False
)
  
  #Serve para que cada letra apareça no momento que for gerada,
  #ao envés de tudo quando a mensagem final estiver pronta
  for chunk in resposta:
    text = chunk["message"]["content"]
    print(text, end="", flush=True)
    mensagem_final += text

  #Salva mensagem da IA no historico também.
  history.add_message_to_history(mensagem_final,"assistant")

  return mensagem_final