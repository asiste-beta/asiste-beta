// Utilidades compartidas por los paneles.

// Hace una petición al servidor y devuelve el JSON de la respuesta.
// Si algo sale mal lanza un Error con un mensaje entendible, para que cada
// panel pueda mostrarlo en pantalla en vez de quedarse en blanco.
async function pedirJSON(url, opciones) {
    let respuesta;

    try {
        respuesta = await fetch(url, opciones);
    } catch (error) {
        throw new Error("No hay conexión con el servidor");
    }

    let cuerpo = null;

    try {
        cuerpo = await respuesta.json();
    } catch (error) {
        if (respuesta.status >= 500) {
            throw new Error(
                `Error interno del servidor (HTTP ${respuesta.status}). ` +
                "Revisa los logs y la conexión a la base de datos."
            );
        }
        throw new Error(
            `El servidor respondió algo inesperado (HTTP ${respuesta.status})`
        );
    }

    if (!respuesta.ok) {
        // FastAPI manda "detail" como texto en errores normales y como lista
        // en errores de validación (422); solo mostramos el texto.
        const detalle = cuerpo && typeof cuerpo.detail === "string" ? cuerpo.detail : null;
        throw new Error(detalle || `Error del servidor (HTTP ${respuesta.status})`);
    }

    return cuerpo;
}

// El servidor guarda las fechas en UTC pero las manda sin la "Z" final
// (ej: "2026-09-20T18:30:00"). Sin la "Z" el navegador las lee como hora
// local y la hora mostrada queda corrida (en Colombia, 5 horas).
function parseFechaUTC(texto) {
    const tieneZona = /(Z|[+-]\d{2}:?\d{2})$/i.test(texto);
    return new Date(tieneZona ? texto : texto + "Z");
}

// ---------- Tema (oscuro por defecto) ----------

// El tema se guarda en localStorage y se aplica en <html data-theme="...">.
// El bloque <script> de templates/_head.html lo aplica antes de pintar la
// página; aquí solo se maneja el botón que lo cambia.
const CLAVE_TEMA = "asiste_tema";

function temaActual() {
    return document.documentElement.getAttribute("data-theme") === "light" ? "light" : "dark";
}

function aplicarTema(tema) {
    document.documentElement.setAttribute("data-theme", tema);

    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", tema === "light" ? "#f6f6f7" : "#0a0a0b");

    try {
        localStorage.setItem(CLAVE_TEMA, tema);
    } catch (error) {
        // si el navegador no deja guardar, el cambio vale solo para esta visita
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const boton = document.getElementById("btn-tema");
    if (!boton) return;

    boton.addEventListener("click", () => {
        aplicarTema(temaActual() === "dark" ? "light" : "dark");
    });
});

// ---------- Iconos y mensajes ----------

// Crea un icono SVG tomado del sprite de templates/_iconos.html.
// Ejemplo: crearIcono("camera")  ->  <svg class="icono"><use href="#i-camera"/></svg>
function crearIcono(nombre) {
    const ns = "http://www.w3.org/2000/svg";
    const svg = document.createElementNS(ns, "svg");
    const uso = document.createElementNS(ns, "use");

    svg.setAttribute("class", "icono");
    svg.setAttribute("aria-hidden", "true");
    uso.setAttribute("href", `#i-${nombre}`);
    svg.appendChild(uso);

    return svg;
}

// Cambia el contenido de un botón por un icono + un texto.
function ponerContenidoBoton(boton, nombreIcono, texto) {
    boton.replaceChildren(crearIcono(nombreIcono), document.createTextNode(texto));
}

// Muestra un mensaje en un <p class="mensaje">. tipo: "exito", "error" o nada.
// El texto se pone con textContent (nunca innerHTML) para que un nombre raro
// guardado en la base de datos no pueda inyectar HTML en la página.
function pintarMensaje(elemento, texto, tipo) {
    elemento.replaceChildren();
    elemento.className = tipo ? `mensaje ${tipo}` : "mensaje";

    if (!texto) return;

    if (tipo === "exito") elemento.appendChild(crearIcono("circle-check"));
    if (tipo === "error") elemento.appendChild(crearIcono("circle-alert"));

    const span = document.createElement("span");
    span.textContent = texto;
    elemento.appendChild(span);
}

// "María Pérez Gómez" -> "MG" (inicial del primer nombre y del último apellido)
function iniciales(nombre) {
    const partes = String(nombre || "").trim().split(/\s+/).filter(Boolean);

    if (partes.length === 0) return "?";

    const primera = partes[0][0];
    const ultima = partes.length > 1 ? partes[partes.length - 1][0] : "";

    return (primera + ultima).toUpperCase();
}
