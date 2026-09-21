// Este script funciona con dos tipos de "escaneo":
// 1. Un escáner de código de barras físico (USB), que escribe el código
//    como si fuera un teclado y luego envía un "Enter".
// 2. El estudiante escribiendo o pegando el código manualmente.
//
// En ambos casos, el input de abajo detecta cuándo se presionó Enter
// y llama a registrarDesdeEscaneo(codigo), definida en panel_estudiante.html.

document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("input-codigo");

    if (!input) return;

    // Mantener el foco en el input para que un escáner físico
    // siempre pueda "escribir" ahí sin que el estudiante tenga que hacer clic.
    input.focus();
    document.addEventListener("click", () => input.focus());

    input.addEventListener("keydown", (evento) => {
        if (evento.key === "Enter") {
            evento.preventDefault();
            const codigo = input.value.trim();

            if (codigo.length > 0 && typeof window.registrarDesdeEscaneo === "function") {
                window.registrarDesdeEscaneo(codigo);
            }

            input.value = "";
        }
    });
});
