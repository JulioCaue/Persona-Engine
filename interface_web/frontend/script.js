const listaModos = /** @type {HTMLSelectElement} */ (
    document.getElementById("modoComportamento")
);
const modoAudio = /** @type {HTMLSelectElement} */ (
    document.getElementById("modo_audio")
);
const caixaMensagem = document.getElementById("form_mensagem");
const btnParar = document.getElementById("botao_parar");
const caixaInput = document.getElementById("campo_input");
const formMensagem = document.getElementById("form_mensagem");
const btnEnviar = document.getElementById("btnEnviar");
const sinalArduino = document.getElementById("status_arduino");
const janelaChat = document.getElementById("chat-mensagens");
url = "http://127.0.0.1:8000";
const socket = new WebSocket("ws://127.0.0.1:8000/ws")

function adicionarMensagem(texto,tipo){
    const mensagem = document.createElement("div");
    mensagem.classList.add("mensagem",tipo);

    const conteudo = document.createElement("p");
    conteudo.textContent = texto;

    mensagem.appendChild(conteudo);
    janelaChat.appendChild(mensagem);
}

async function verificar_arduino(){
    const resposta = await fetch(`${url}/status/arduino`);
    const status = await resposta.json();
    if (status){
        sinalArduino.classList.add("ativo");
        sinalArduino.classList.remove("desativado")
    }
    else{
        sinalArduino.classList.add("desativado");
        sinalArduino.classList.remove("ativo")
    }
    return status
}

async function receberInput(click) {
    const textoEscrito = caixaInput.value;

    adicionarMensagem(textoEscrito,"usuario")
    caixaInput.value = ""

    try{
        const resposta = await fetch(`${url}/controle`,{
            method:"POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                modo: 3,
                input: textoEscrito
            })
        });
        
        const resultado = await resposta.json();

        console.log(resultado)
    } 
    catch(erro){
        console.error("Erro enviando data: ",erro);
    }
}

async function trocarAudio(event) {
    const modoEscolhido = event.target.value;
    if ([1,2].includes(parseInt(modoEscolhido))){
        if (parseInt(modoEscolhido) == 1){escolha = true;}
        else{escolha = false;}
        try{
            const resposta = await fetch(`${url}/controle`,{
                method:"POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    modo: escolha,
                    input: null
                })
            });
            
            const resultado = await resposta.json();

            console.log(resultado);
        } 
        catch(erro){
            console.error("Erro enviando data: ",erro);
        }
    }
}

async function pararModo(onclick) {
    // usa zero para não entrar na função controlador (zero não é usado)
    const modoEscolhido = 0;
    try{
        const resposta = await fetch(`${url}/controle`,{
            method:"POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                modo: modoEscolhido,
                input: null
            })
        });
        
        const resultado = await resposta.json();

        console.log("o botão foi apertado!");
    } 
    catch(erro){
        console.error("Erro enviando data: ",erro);
    }
}

async function mostrarInput(event) {
    const modoEscolhido = event.target.value;

    if (Number(modoEscolhido) == 3){
        caixaMensagem.classList.remove('esconder');
    }
    else {
        caixaMensagem.classList.add('esconder');
    }
}

async function trocarModo(event) {
    const modoEscolhido = event.target.value;
    
    //envia apenas se modo selecionado está nessa lista, para evitar problemas
    if ([1,2,3].includes(Number(modoEscolhido))){
        try{
            const resposta = await fetch(`${url}/controle`,{
                method:"POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    modo: modoEscolhido,
                    input: null
                })
            });
            
            const resultado = await resposta.json();

            console.log(resultado)
        } 
        catch(erro){
            console.error("Erro enviando data: ",erro);
        }
    }
}

socket.onmessage = (event) => {
    const {resposta, autor} = JSON.parse(event.data);
    adicionarMensagem(resposta,autor);
}

verificar_arduino().then(status => {
    console.log(status);
})
setInterval(verificar_arduino,5000)

window.addEventListener("pageshow", () => {
    listaModos.selectedIndex = 0;
    modoAudio.selectedIndex = 0;
})

formMensagem.addEventListener("submit", (event) => {
    event.preventDefault();
    receberInput();
});

btnParar.addEventListener("click",pararModo);

modoAudio.addEventListener("change",trocarAudio);

listaModos.addEventListener("change",mostrarInput);

listaModos.addEventListener("change",trocarModo);