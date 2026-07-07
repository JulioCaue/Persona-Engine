from ollama import chat
import subprocess

with open("ai/prompts/conversa/sistema.txt",'r') as f:
  prompt_sistema = f.read()


def perguntar_ia(historico):
  resposta = chat(
    model='qwen3:1.7b',
    messages=[
      {'role': 'system', 'content': prompt_sistema},
      *historico
      ],
    stream= True,
    think= False
)

  subprocess.run(["clear"])
  
  for chunk in resposta:
    text = chunk["message"]["content"]
    print(text, end="", flush=True)
    mensagem_final+=text

  return mensagem_final