import asyncio
import threading
import controlador
import os
import json
from pathlib import Path
from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from serial import SerialException
from logs import log_writer


app = FastAPI()
ultimo_modo: int
tarefa_atual: asyncio.Task | None = None
evento_atual: threading.Event | None = None
lock_modo = asyncio.Lock()
conexao_frontend: WebSocket | None = None

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"

#CSS, JavaScript, imagens etc.
app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static",
)

class Resposta_controle(BaseModel):
    modo: int | bool;
    input: str | None

class Receber_resposta_ia(BaseModel):
    resposta: str;
    autor: str


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
async def frontend() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/status/arduino")
def verificar_arduino():
    return os.path.exists("/dev/ttyUSB0")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print("ENTROU NA ROTA WEBSOCKET")
    global conexao_frontend

    await websocket.accept()
    conexao_frontend = websocket
    print("websocket conectado")

    while True:
        await websocket.receive_text()

async def mandar_resposta(resposta_ia):
    print("entrou em mandar resposta")
    if conexao_frontend is None:
        print("Frontend não conectado")
        return
    await conexao_frontend.send_json(resposta_ia)

@app.post("/receber_mensagem")
async def receber_resposta(resposta: Receber_resposta_ia):
    print("entrou em receber resposta")
    resposta_ia = resposta.resposta
    autor  = resposta.autor

    mensagem = {
        "resposta": resposta_ia,
        "autor": autor
    }
    if resposta_ia:
        await mandar_resposta(mensagem)


@app.post("/controle")
async def receber_modo(dados: Resposta_controle):
    global evento_atual, tarefa_atual, ultimo_modo
    #Toggle do uso do audio.
    if isinstance(dados.modo,bool):
        modo_audio = dados.modo
        controlador.trocar_modo_audio(modo_audio)
        return {
            "modo_de_audio": modo_audio
        }
    #Codigo principal, gerencia controle do modo atual.
    else:
        modo_recebido = int(dados.modo)
        ultimo_modo = modo_recebido
        input_usuario = dados.input

        async with lock_modo:
            tarefa_anterior = tarefa_atual
            evento_anterior = evento_atual

            if evento_anterior is not None:
                evento_anterior.set()

            if tarefa_anterior is not None:
                try:
                    await tarefa_anterior

                except SerialException:
                    print("Arduino não conectado.")

                except Exception as e:
                    print(f"Ocorreu um erro: {e}")
                    log_writer.write(__name__,f"Ocorreu um erro: {e}")
                    raise HTTPException(
                        status_code=500,
                        detail="Erro interno inesperado"
                    )

            evento_atual = threading.Event()

            #Apenas chama função se ultimo_modo não for zero, assim permitindo que botão chegue até aqui sem entrar na função controlador.
            if not ultimo_modo == 0:
                tarefa_atual = asyncio.create_task(
                    asyncio.to_thread(
                        controlador.controla_modo,
                        ultimo_modo,
                        evento_atual,
                        input_usuario
                    )
                )

        return {
            "modo_recebido": modo_recebido,
            "input_usuario": input_usuario
        }