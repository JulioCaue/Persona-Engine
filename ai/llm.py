from ollama import chat
from ai import history

with open("ai/prompts/sistema.txt",'r') as f:
  prompt_sistema = f.read()


def perguntar_ia(historico):
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
  
  for chunk in resposta:
    text = chunk["message"]["content"]
    print(text, end="", flush=True)
    mensagem_final += text

  history.add_message_to_history(mensagem_final,"assistant")

  return mensagem_final