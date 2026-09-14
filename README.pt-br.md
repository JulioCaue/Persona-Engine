# Persona-Engine

[Read in English](README.md)

> Assistente de IA local desenvolvido em Python com Ollama, FastAPI, WebSockets, voz, tool calling e integração opcional com hardware Arduino.

Persona-Engine é um assistente de IA modular que combina **modelo de linguagem local**, **comunicação web em tempo real**, **interação por voz**, **execução de ferramentas** e **integração com hardware físico** em um único projeto.

O fluxo principal de interação já está implementado: o usuário pode interagir por texto ou voz, o modelo local pode responder diretamente ou chamar ferramentas registradas, as respostas são persistidas no histórico de conversa e a saída pode ser enviada para a interface web, para o sistema de text-to-speech e para hardware Arduino opcional.

## Destaques de engenharia

Este projeto demonstra trabalho prático com:

- Arquitetura de aplicações em Python
- Integração de LLM local com Ollama
- Tool/function calling com registry explícito de funções
- Persistência de histórico de conversa e chamadas de ferramentas
- Endpoints REST com FastAPI
- Comunicação em tempo real com WebSockets
- Coordenação entre asyncio, threads e tarefas bloqueantes
- Pipelines de speech-to-text e text-to-speech
- Processamento de áudio com NumPy, SciPy, librosa e PyAudio
- Comunicação serial com Arduino
- Controle de servos baseado em amplitude de áudio
- Logging e tratamento de erros
- Integração entre frontend e backend

## Principais funcionalidades

- LLM local através do Ollama
- Conversa por texto
- Entrada por microfone
- Speech-to-text
- Text-to-speech
- Tool/function calling
- Histórico persistente de conversa
- Interface web
- Backend com FastAPI
- Comunicação via WebSocket
- Reconexão automática do WebSocket no frontend
- Detecção do status do Arduino
- Animação facial opcional com servos
- Movimento da boca baseado em áudio
- Logging da aplicação
- Ambiente desenvolvido prioritariamente em Linux

## Arquitetura

```text
Persona-Engine
│
├── ai/
│   ├── llm.py              # comunicação com o modelo e orquestração de tools
│   ├── ferramentas.py      # ferramentas registradas e schemas
│   ├── history.py          # persistência do histórico e resultados de tools
│   └── prompts/
│
├── animation/
│   ├── falar_audio.py      # animação dos servos com áudio gerado
│   └── falar_mic.py        # movimento ao vivo baseado no microfone
│
│
│
│
├── audios/
│   └── audio_player.py
│
├── interface_web/
│   ├── backend/
│   │   └── main.py         # backend FastAPI
│   └── frontend/
│       ├── index.html
│       ├── script.js
│       └── style.css
│
├── translators/
│   ├── speech_to_text.py
│   └── text_to_speech.py
│
├── logs/
│   └── log_writer.py
│
└── controlador.py          # coordenador principal da aplicação
```

## Como o sistema funciona

```text
Usuário
 │
 ├── Texto ─────────────────────┐
 │                              │
 └── Voz → Speech-to-Text ──────┤
                                ▼
                        Controlador Persona
                                │
                                ▼
                            LLM local
                                │
                    ┌───────────┴───────────┐
                    │                       │
                 Resposta                Tool Call
                    │                       │
                    │                       ▼
                    │             Ferramenta registrada
                    │                       │
                    └───────────┬───────────┘
                                ▼
                       Resposta final da IA
                                │
                  ┌─────────────┼──────────────┐
                  ▼             ▼              ▼
             Interface web     TTS          Bottango
                                │              │
                                ▼              ▼
                              Áudio         Arduino
                                               │
                                             Servos
```

## Tool calling

As ferramentas ficam separadas da lógica principal de comunicação com o modelo.

Cada ferramenta possui:

1. Um schema que descreve o que o modelo pode chamar.
2. Uma função Python registrada responsável pela execução.
3. Um registro persistente contendo a chamada e o resultado da ferramenta.

Isso mantém a definição apresentada ao modelo separada do registry de funções realmente executáveis.

As ferramentas atuais incluem:

- Tocar uma música suportada
- Parar uma música
- Consultar a hora atual do sistema

O registry pode ser expandido sem alterar o fluxo geral de comunicação com o modelo.

## Backend web

O backend FastAPI é responsável por:

- Servir o frontend
- Receber mudanças de modo de interação
- Receber e encaminhar respostas da IA
- Informar o status da conexão com o Arduino
- Manter a conexão WebSocket com o navegador

O frontend tenta reconectar automaticamente quando a conexão WebSocket é perdida.

## Voz e áudio

Persona-Engine oferece suporte a:

- Speech-to-text pelo microfone
- Text-to-speech
- Reprodução de arquivos WAV
- Análise de amplitude de áudio
- Movimento de servos baseado em áudio em tempo real ou gerado

O text-to-speech atualmente utiliza `espeak-ng`, enquanto a transcrição por microfone utiliza o pacote Python `SpeechRecognition`.

## Hardware

O suporte a Arduino é opcional.

Quando conectado, a camada de hardware pode:

- Detectar o dispositivo serial
- Enviar posições de servos por comunicação serial
- Movimentar a boca com base na amplitude do microfone ou do áudio gerado
- Coordenar movimentos faciais simples com a fala

O software continua funcionando sem Arduino para testes apenas de software.

## Requisitos

### Python

- Python 3.10+
- Ollama
- Um modelo local compatível

Instale as dependências Python com:

```bash
pip install -r requirements.txt
```

### Dependências do sistema

Algumas funcionalidades de áudio dependem de pacotes nativos do sistema.

Você pode precisar de:

- `espeak-ng`
- PortAudio / bibliotecas de desenvolvimento necessárias para PyAudio
- Suporte funcional a microfone e saída de áudio

Os nomes exatos dos pacotes dependem da distribuição Linux utilizada.

## Instalação

Clone o repositório:

```bash
git clone https://github.com/JulioCaue/Persona-Engine.git
cd Persona-Engine
```

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative no Linux:

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Instale e inicie o Ollama, depois baixe o modelo atualmente utilizado pelo projeto:

```bash
ollama pull qwen2.5:3b
```

## Executando a interface web

Inicie a aplicação FastAPI:

```bash
uvicorn interface_web.backend.main:app --reload
```

Depois abra:

```text
http://127.0.0.1:8000
```

## Suporte de plataforma

Persona-Engine atualmente é desenvolvido e testado principalmente em **Linux**.

Outros sistemas operacionais ainda não possuem suporte oficial, especialmente para:

- Caminhos de dispositivos seriais
- Bibliotecas de áudio
- Acesso ao microfone
- Integração com Arduino
- TTS dependente do sistema

## Estado atual

O fluxo principal do projeto já está implementado.

A base atual já oferece suporte a:

- Respostas de IA local
- Tool calling
- Histórico persistente de conversa
- Histórico de resultados de ferramentas
- Interação web
- Atualizações via WebSocket
- Entrada e saída por voz
- Integração opcional com hardware




## Por que eu construí este projeto

Persona-Engine começou como uma forma de construir algo que eu realmente queria usar enquanto aprendia por implementação, em vez de estudar apenas exercícios isolados.

O projeto acabou reunindo desenvolvimento backend, IA local, comunicação em tempo real, processamento de áudio, integração com hardware e arquitetura de aplicações em uma única base de código.

## Autor

**Cauê**

GitHub: https://github.com/JulioCaue
