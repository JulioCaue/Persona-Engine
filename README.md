# Persona-Engine

[ Ler em Português ](README.pt-br.md)

> Experimental AI assistant combining local LLMs, voice interaction, web interfaces and physical robotics.

Persona-Engine is a personal project focused on building an interactive AI assistant that can communicate through text and voice, execute tools, interact with a web interface and control physical hardware.

The project is developed as an ongoing experiment in **Python, local AI, backend development and robotics**.

## Features

- Local LLM integration through [Ollama](https://ollama.com/)
- Conversational history
- Text-based interaction
- Speech-to-text interaction
- Text-to-speech responses
- Tool/function calling
- Web interface
- Real-time communication through WebSockets
- REST API built with FastAPI
- Arduino integration
- Servo-controlled facial animation
- Logging and error handling
- Experimental audio and animation system

## Architecture

The project is divided into several components:

```text
Persona-Engine
│
├── ai/
│   ├── LLM communication
│   ├── conversation history
│   ├── prompts
│   └── tools
│
├── animation/
│   └── facial/audio animation
│
├── arduino/
│   └── hardware control
│
├── audios/
│   └── audio playback
│
├── interface_web/
│   ├── FastAPI backend
│   └── WebSocket communication
│
├── translators/
│   ├── speech-to-text
│   └── text-to-speech
│
├── logs/
│   └── application logging
│
└── controlador.py
    └── main interaction controller
```

## Technologies

### Backend

- Python
- FastAPI
- Uvicorn
- WebSockets
- REST APIs
- Pydantic
- Requests

### Artificial Intelligence

- Ollama
- Local Large Language Models
- Tool/function calling
- Conversation history

### Audio

- Speech-to-text
- Text-to-speech
- WAV audio playback

### Hardware

- Arduino
- Serial communication
- Servo motors

### Development

- Git
- GitHub
- Linux
- Python virtual environments

# Platform Support

Persona-Engine is currently being developed and tested primarily on **Linux**.

Other operating systems are **not officially supported at this time**, and some features may not work as expected outside Linux, especially hardware and system-level integrations.

Support for additional operating systems may be added in the future.

## How it works

At a high level, the system works as follows:

```text
User
 │
 ├── Text ───────────────┐
 │                       │
 └── Voice → STT ────────┤
                         ▼
                  Persona Controller
                         │
                         ▼
                    Local LLM
                         │
                ┌────────┴────────┐
                │                 │
             Response          Tool Call
                │                 │
                │                 ▼
                │               Tool
                │                 │
                └────────┬────────┘
                         ▼
                  Response / TTS
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
          Web Interface          Hardware
                                  Arduino
                                     │
                                   Servos
```

## Requirements

- Python 3.10+
- Ollama
- A compatible local language model
- Microphone (for voice interaction) (optional)
- Arduino + compatible hardware (optional)

The project can run without the Arduino for software-only testing.

## Installation

Clone the repository:

```bash
git clone https://github.com/JulioCaue/Persona-Engine.git
cd Persona-Engine
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install and start Ollama, then download a compatible model.

For example:

```bash
ollama pull qwen2.5:3b
```

The model configured by the current implementation can be changed in:

```text
ai/llm.py
```

## Running the web interface

Start the FastAPI application with:

```bash
uvicorn interface_web.backend.main:app --reload
```

The web interface should then be available at:

```text
http://127.0.0.1:8000
```

## Hardware

Arduino functionality is optional.

When the Arduino is not connected, the software can still be used for software-only interaction.

Hardware communication is currently designed around a serial device exposed by Linux.

## Project status

Persona-Engine is an **active experimental project**.

The architecture and features are still evolving. Some components are prototypes and may change as the project develops.

The current focus is improving:

- Architecture
- Reliability
- Testing
- Web interface
- AI tool integration
- Hardware interaction
- Documentation

## Demo

A demonstration of the project is planned to show:

1. The web interface
2. A text conversation with the local LLM
3. Tool execution
4. Voice interaction
5. The AI response being converted to speech
6. The physical head reacting to the response

## Why I built this

I built Persona-Engine because I wanted to create something I thought was genuinely interesting while challenging myself to learn by building it.

The project started as an experiment and continues to grow into a way to study Python, backend development, local LLMs, audio processing, and robotics in a single system.

## Author

**Cauê**

GitHub:
https://github.com/JulioCaue

---

> This project is developed for learning and experimentation.
