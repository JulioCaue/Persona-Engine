from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from serial import SerialException
import asyncio
import threading
import controlador
from logs import log_writer


app = FastAPI()
ultimo_modo: int
tarefa_atual: asyncio.Task | None = None
evento_atual: threading.Event | None = None
lock_modo = asyncio.Lock()

class ModoEscolha(BaseModel):
    modo: int

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/controle")
async def receber_modo(dados: ModoEscolha):
    global evento_atual, tarefa_atual, ultimo_modo
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
                log_writer.write(f"Ocorreu um erro: {e}")
                raise HTTPException(
                    status_code=500,
                    detail="Erro interno inesperado"
                )

        evento_atual = threading.Event()

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