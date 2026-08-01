const listaModos = document.getElementById("modo")
url = "http://127.0.0.1:8000/controle";

async function trocarModo(event) {
    const modoEscolhido = event.target.value;
    
    //envia apenas se modo selecionado está nessa lista, para evitar problemas
    if ([1,2,3].includes(Number(modoEscolhido))){
        try{
            const resposta = await fetch(url,{
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
        } catch(erro){
            console.error("Erro enviando data: ",erro);
        }
    }
}


listaModos.addEventListener("change",trocarModo);