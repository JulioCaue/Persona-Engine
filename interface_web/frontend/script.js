const listaModos = document.getElementById("modoComportamento")
const caixa_mensagem = document.getElementById("section_input_mensagem")
const btn_parar = document.getElementById("botao_parar")
const modo_audio = document.getElementById("modo_audio")
const caixa_input = document.getElementById("campo_input")
const btn_enviar = document.getElementById("btnEnviar")
const sinal_arduino = document.getElementById("status_arduino")
url = "http://127.0.0.1:8000";


async function verificar_arduino(){
    const resposta = await fetch(`${url}/status/arduino`);
    const status = await resposta.json();
    if (status){
        sinal_arduino.classList.add("ativo");
        sinal_arduino.classList.remove("desativado")
    }
    else{
        sinal_arduino.classList.add("desativado");
        sinal_arduino.classList.remove("ativo")
    }
    return status
}

async function receberInput(click) {
    const textoEscrito = caixa_input.value;

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
        caixa_mensagem.classList.remove('esconder');
    }
    else {
        caixa_mensagem.classList.add('esconder');
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

verificar_arduino().then(status => {
    console.log(status);
})
setInterval(verificar_arduino,5000)

btn_enviar.addEventListener("click",receberInput)

btn_parar.addEventListener("click",pararModo);

modo_audio.addEventListener("change",trocarAudio);

listaModos.addEventListener("change",mostrarInput);

listaModos.addEventListener("change",trocarModo);