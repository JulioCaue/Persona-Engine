const listaModos = document.getElementById("modo")

listaModos.addEventListener("change",(event) => {
    switch (event.target.value){
        case("1"):
            console.log("Imitar Fala");
            break;

        case("2"):
            console.log("Conversa por Fala");
            break;

        case("3"):
            console.log("Conversa por Texto");
            break;
    }

})