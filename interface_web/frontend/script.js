const listaModos = document.getElementById("modo")

listaModos.addEventListener("change",(event) => {
    switch (event.target.value){
        case("Imitar Fala"):
            console.log("Imitar Fala");
            break;

        case("Conversa por Fala"):
            console.log("Conversa por Fala");
            break;

        case("Conversa por Texto"):
            console.log("Conversa por Texto");
            break;
    }

})