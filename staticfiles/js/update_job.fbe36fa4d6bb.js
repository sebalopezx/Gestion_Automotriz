// FUNCION AUTO AJUSTE DE TEXTAREAS
// document.addEventListener("DOMContentLoaded", function () {
//     const autoResizeTextarea = document.querySelector("textarea");
//     autoResizeTextarea.addEventListener("keyup", e =>{
//         let height = e.target.scrollHeight;
//         autoResizeTextarea.style.height = `${height}px`;
//     });
// });



document.addEventListener("DOMContentLoaded", function () {
    const textareas = document.querySelectorAll("form textarea");

    textareas.forEach((textarea) => {
        textarea.addEventListener("input", function () {
            this.style.height = this.scrollHeight + "px"; // Ajusta la altura según el contenido
        });
        textarea.dispatchEvent(new Event("input"));

        textarea.addEventListener("keydown", function (event) {
            if (event.key === "Backspace" || event.key === "Delete") {
                // Agrega un pequeño retraso para permitir que el navegador actualice el contenido

                this.style.height = this.scrollHeight + "px";
            };
        });
    });
});