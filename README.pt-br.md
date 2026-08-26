# Persona-Engine

[ Read in English ](README.md)

> Assistente experimental de IA combinando modelos locais, interação por voz, interface web e robótica física.

O Persona-Engine é um projeto pessoal focado na criação de um assistente de IA interativo capaz de se comunicar por texto e voz, executar ferramentas, interagir com uma interface web e controlar hardware físico.

O projeto está sendo desenvolvido como um experimento contínuo em **Python, IA local, desenvolvimento backend e robótica**.

## Funcionalidades

- Integração com modelos locais através do [Ollama](https://ollama.com/)
- Histórico de conversação
- Interação por texto
- Interação por reconhecimento de voz
- Respostas por síntese de voz
- Execução de ferramentas / function calling
- Interface web
- Comunicação em tempo real através de WebSockets
- API REST desenvolvida com FastAPI
- Integração com Arduino
- Animação facial controlada por servomotores
- Sistema de logs e tratamento de erros
- Sistema experimental de áudio e animações

## Arquitetura

O projeto é dividido em vários componentes:

```text
Persona-Engine
│
├── ai/
│   ├── comunicação com o LLM
│   ├── histórico de conversação
│   ├── prompts
│   └── ferramentas
│
├── animation/
│   └── animação facial/áudio
│
├── arduino/
│   └── controle do hardware
│
├── audios/
│   └── reprodução de áudio
│
├── interface_web/
│   ├── backend FastAPI
│   └── comunicação via WebSocket
│
├── translators/
│   ├── reconhecimento de voz
│   └── síntese de voz
│
├── logs/
│   └── registro de eventos
│
└── controlador.py
    └── controlador principal da interação
```

## Tecnologias

### Backend

- Python
- FastAPI
- Uvicorn
- WebSockets
- APIs REST
- Pydantic
- Requests

### Inteligência Artificial

- Ollama
- Modelos de linguagem locais
- Function/tool calling
- Histórico de conversação

### Áudio

- Speech-to-text
- Text-to-speech
- Reprodução de arquivos WAV

### Hardware

- Arduino
- Comunicação serial
- Servomotores

### Desenvolvimento

- Git
- GitHub
- Linux
- Ambientes virtuais Python

# Suporte de plataforma

O Persona-Engine está atualmente sendo desenvolvido e testado principalmente no **Linux**.

Outros sistemas operacionais **não são oficialmente suportados neste momento**, e algumas funcionalidades podem não funcionar como esperado fora do Linux, especialmente integrações com hardware e recursos específicos do sistema.

O suporte a outros sistemas operacionais poderá ser adicionado futuramente.

## Como funciona

Em alto nível, o sistema funciona da seguinte maneira:

```text
Usuário
 │
 ├── Texto ───────────────┐
 │                        │
 └── Voz → STT ───────────┤
                          ▼
                   Controlador
                          │
                          ▼
                     LLM local
                          │
                 ┌────────┴────────┐
                 │                 │
              Resposta         Tool Call
                 │                 │
                 │                 ▼
                 │              Ferramenta
                 │                 │
                 └────────┬────────┘
                          ▼
                   Resposta / TTS
                          │
               ┌──────────┴──────────┐
               ▼                     ▼
          Interface Web           Hardware
                                  Arduino
                                     │
                                  Servos
```

## Requisitos

- Python 3.10+
- Ollama
- Um modelo de linguagem compatível
- Microfone (para interação por voz)
- Arduino + hardware compatível (opcional)

O projeto pode ser executado sem o Arduino para testes exclusivamente de software.

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

Ative o ambiente no Linux:

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Instale e inicie o Ollama e, em seguida, baixe um modelo compatível.

Por exemplo:

```bash
ollama pull qwen2.5:3b
```

O modelo configurado pela implementação atual pode ser alterado em:

```text
ai/llm.py
```

## Executando a interface web

Inicie a aplicação FastAPI com:

```bash
uvicorn interface_web.backend.main:app --reload
```

A interface web deverá estar disponível em:

```text
http://127.0.0.1:8000
```

## Hardware

A funcionalidade relacionada ao Arduino é opcional.

Quando o Arduino não está conectado, o software ainda pode ser utilizado para interações exclusivamente de software.

A comunicação com o hardware atualmente utiliza uma interface serial exposta pelo Linux.

## Estado do projeto

O Persona-Engine é um **projeto experimental ativo**.

A arquitetura e as funcionalidades ainda estão em evolução. Alguns componentes são protótipos e podem mudar conforme o desenvolvimento do projeto.

Atualmente, o foco está em melhorar:

- Arquitetura
- Confiabilidade
- Testes
- Interface web
- Integração de ferramentas de IA
- Interação com hardware
- Documentação

## Demo

A demonstração do projeto pretende mostrar:

1. A interface web
2. Uma conversa por texto com o LLM local
3. Execução de ferramentas
4. Interação por voz
5. A resposta da IA sendo convertida em fala
6. A cabeça física reagindo à resposta

## Por que criei isto

Criei o Persona-Engine porque queria desenvolver algo que considerava genuinamente interessante, ao mesmo tempo em que me desafiava a aprender durante o processo de construção.

O projeto começou como um experimento e continua evoluindo para uma forma de estudar Python, desenvolvimento de backend, LLMs locais, processamento de áudio e robótica em um único sistema.

## Autor

**Cauê**

GitHub:
https://github.com/JulioCaue

---

> Este projeto é desenvolvido para aprendizado e experimentação.
