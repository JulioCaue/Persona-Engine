import asyncio
import threading
import controlador
from pathlib import Path
from fastapi import FastAPI
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

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"

#CSS, JavaScript, imagens etc.
app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static",
)

class Resposta_controle(BaseModel):
    modo: int | bool

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

        async with lock_modo:
            tarefa_anterior = tarefa_atual
            evento_anterior = evento_atual

            if evento_anterior is not None:
                evento_anterior.set()

            if tarefa_anterior is not None:
                try:
                    await tarefa_anterior

                except SerialException:
                    raise HTTPException(
                        status_code=503,
                        detail="Arduino não conectado."
                    )

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
                        controlador.executar_modo,
                        ultimo_modo,
                        evento_atual
                    )
                )


        return {
            "modo_recebido": modo_recebido
        }