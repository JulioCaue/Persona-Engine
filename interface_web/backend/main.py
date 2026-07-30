from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
class ModoEscolha(BaseModel):
    modo: int

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/controle")
def receber_modo(dados: ModoEscolha):
    modo_recebido = int(dados.modo)

    print(modo_recebido)

    return {
        "modo_recebido": modo_recebido
    }