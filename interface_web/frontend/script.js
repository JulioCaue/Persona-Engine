const listaModos = document.getElementById("modoComportamento")
const caixa_mensagem = document.getElementById("section_input_mensagem")
const botao_parar = document.getElementById("botao_parar")
const modo_audio = document.getElementById("modo_audio")
url = "http://127.0.0.1:8000";


async function trocarAudio(event) {
    const modoEscolhido = event.target.value;
    if ([1,2].includes(Number(modoEscolhido))){
        if (Number(modoEscolhido) == 1){escolha = true;}
        else{escolha = false;}
        try{
            const resposta = await fetch(`${url}/controle`,{
                method:"POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    modo: escolha
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
                modo: modoEscolhido
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
                    modo: modoEscolhido
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


botao_parar.addEventListener("click",pararModo);

modo_audio.addEventListener("change",trocarAudio);

listaModos.addEventListener("change",mostrarInput);

listaModos.addEventListener("change",trocarModo);