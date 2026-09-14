# Persona-Engine

[Leia em Português](README.pt-br.md)

> Local AI assistant built in Python with Ollama, FastAPI, WebSockets, speech, tool calling, and optional Arduino-based hardware control.

Persona-Engine is a modular AI assistant that combines a **local language model**, **real-time web communication**, **voice interaction**, **tool execution**, and **physical hardware integration** in a single project.

The core interaction flow is already implemented: the user can interact through text or voice, the local model can answer directly or call registered tools, responses are persisted in conversation history, and output can be sent to the web interface, text-to-speech pipeline, and optional Arduino hardware.

## Engineering highlights

This project demonstrates practical work with:

- Python application architecture
- Local LLM integration with Ollama
- Tool/function calling with explicit function registries
- Conversation history and tool-call persistence
- FastAPI REST endpoints
- WebSocket-based real-time updates
- Async/threaded coordination between backend and blocking tasks
- Speech-to-text and text-to-speech pipelines
- Audio processing with NumPy, SciPy, librosa and PyAudio
- Serial communication with Arduino
- Servo control driven by audio amplitude
- Logging and error handling
- Frontend/backend integration

## Main features

- Local LLM through Ollama
- Text conversation
- Microphone input
- Speech-to-text
- Text-to-speech
- Tool/function calling
- Persistent conversation history
- Web interface
- FastAPI backend
- WebSocket communication
- Automatic WebSocket reconnection on the frontend
- Arduino status detection
- Optional servo-controlled facial animation
- Audio-driven mouth movement
- Application logging
- Linux-first development environment

## Architecture

```text
Persona-Engine
│
├── ai/
│   ├── llm.py              # model communication and tool-call orchestration
│   ├── ferramentas.py      # registered tools and tool schemas
│   ├── history.py          # conversation and tool history persistence
│   └── prompts/
│
├── animation/
│   ├── falar_audio.py      # audio-driven servo animation
│   └── falar_mic.py        # live microphone-driven movement
│
│
│
│
├── audios/
│   └── audio_player.py
│
├── interface_web/
│   ├── backend/
│   │   └── main.py         # FastAPI backend
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
└── controlador.py          # application coordinator
```

## How the system works

```text
User
 │
 ├── Text ─────────────────────┐
 │                             │
 └── Voice → Speech-to-Text ───┤
                               ▼
                       Persona Controller
                               │
                               ▼
                           Local LLM
                               │
                   ┌───────────┴───────────┐
                   │                       │
                Response                Tool Call
                   │                       │
                   │                       ▼
                   │                  Registered Tool
                   │                       │
                   └───────────┬───────────┘
                               ▼
                     Final model response
                               │
                 ┌─────────────┼─────────────┐
                 ▼             ▼             ▼
            Web interface      TTS        Hardware
                                │             │
                                ▼             ▼
                              Audio         Arduino
                                             │
                                           Servos
```

## Tool calling

Tools are defined separately from the model orchestration logic.

Each tool has:

1. A schema describing what the model is allowed to call.
2. A registered Python function responsible for execution.
3. A persistent history entry recording the tool call and its result.

This keeps the model-facing tool definition separate from the actual executable function registry.

Current tools include:

- Playing a supported song
- Stopping a song
- Reading the current system time

The registry can be extended with additional tools without changing the general model-calling flow.

## Web backend

The FastAPI backend is responsible for:

- Serving the frontend
- Receiving user interaction mode changes
- Receiving and forwarding AI responses
- Reporting Arduino connection status
- Maintaining a WebSocket connection with the browser

The frontend automatically attempts to reconnect when the WebSocket connection is lost.

## Voice and audio

Persona-Engine supports:

- Speech-to-text through microphone input
- Text-to-speech output
- WAV playback
- Audio amplitude analysis
- Servo movement based on real-time or generated audio

Text-to-speech currently uses `espeak-ng`, while microphone transcription uses the Python `SpeechRecognition` package.

## Hardware

Arduino support is optional.

When connected, the hardware layer can:

- Detect the serial device
- Send servo positions through serial communication
- Move the mouth based on microphone or generated audio amplitude
- Coordinate simple facial movement with spoken output

The software can still run without the Arduino for software-only testing.

## Requirements

### Python

- Python 3.10+
- Ollama
- A compatible local model

Install Python dependencies with:

```bash
pip install -r requirements.txt
```

### System dependencies

Some audio features depend on native system packages.

At minimum, you may need:

- `espeak-ng`
- PortAudio / audio development libraries required by PyAudio
- Working microphone/audio output support

Exact package names depend on your Linux distribution.

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

Install and start Ollama, then pull the model currently used by the project:

```bash
ollama pull qwen2.5:3b
```

## Running the web interface

Start the FastAPI application:

```bash
uvicorn interface_web.backend.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000
```

## Platform support

Persona-Engine is currently developed and tested primarily on **Linux**.

Other operating systems are not officially supported yet, especially for:

- Serial device paths
- Audio libraries
- Microphone access
- Arduino integration
- System-level TTS

## Current status

The project's core interaction flow is implemented.

The current codebase already supports:

- Local AI responses
- Tool calling
- Persistent conversation history
- Tool-result history
- Web interaction
- WebSocket updates
- Voice input/output
- Optional hardware integration




## Why I built this

Persona-Engine started as a way to build something I genuinely wanted to use while learning through implementation instead of isolated exercises.

It became a project that brings together backend development, local AI, real-time communication, audio processing, hardware integration, and application architecture in one codebase.

## Author

**Cauê**

GitHub: https://github.com/JulioCaue
