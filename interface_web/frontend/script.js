const listaModos = document.getElementById("modo")
const caixa_mensagem = document.getElementById("section_input_mensagem")
url = "http://127.0.0.1:8000";


async function mostrar_input(event) {
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

listaModos.addEventListener("change",mostrar_input);

listaModos.addEventListener("change",trocarModo);