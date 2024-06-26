// TOAST DE ALERTAS PARA CONFIRMACIÓN Y ERRORES

// Toma un contenedor con id #toast-container, que solo aparece si el envio de un formulario POST manda un elemento message
// En caso de que obtenga un valor true en message, muestra un mensaje de confirmacion o error


document.addEventListener("DOMContentLoaded", function () {
    const toastContainer = document.getElementById("toast-container");

    // Función para crear y mostrar un toast, con dos paramentros (el mensaje y las variantes por el tipo de mensaje)
    function showToast(message, variant) {
        const toast = document.createElement("div");
        toast.classList.add("toast", `bg-${variant}`, "text-white");
        toast.setAttribute("role", "alert");
        toast.setAttribute("aria-live", "assertive");
        toast.setAttribute("aria-atomic", "true");

      toast.innerHTML = `
        <div class="toast-body sticky-bottom">
            <button type="button" class="btn-close btn-close-white me-auto pb-2" data-bs-dismiss="toast" aria-label="Close"></button>
            ${message}
        </div>`;
        // console.log("MENSAJE: ", message)
        // console.log("toast-container: ",toastContainer)

        toastContainer.appendChild(toast);

        // Mostrar el toast
        const bootstrapToast = new bootstrap.Toast(toast);
        bootstrapToast.show();

        // Eliminar el toast después de ocultarlo
        toast.addEventListener("hidden.bs.toast", function () {
            toastContainer.removeChild(toast);
        });
    }

    const messages = document.querySelectorAll(".message");
    messages.forEach(function (messageElement) {
        // const messageText = messageElement.textContent.trim();
        // Obtener mensaje
        const messageText = messageElement.getAttribute("data-message");
        // get atrr =  danger o success
        const messageClass = messageElement.getAttribute("data-message-class");
        showToast(messageText, messageClass);
    });
});




// PREGUNTAS DE CONFIRMACION  sacadas desde los elementos html como etiquetas data = {}
var actionDataTitles = {
    'delete': 'error',
    'question': 'question',
    'confirm': 'success',
    'warning': 'warning',
    'info': 'info',
}
var confirmationTitles = {
    'delete-mechanic': '¿Estás seguro de que deseas eliminar el mecánico? <br>Cambiara su disponibilidad a inactivo y eliminaras su imágen.',
    'confirm': '¿Estás seguro de que deseas realizar esta acción?',
    'cancel': '¿Estás seguro de que deseas cancelar la cita?',
    'register': '¿Estás seguro que quieres seguir con el registro?',
    'update': '¿Estás seguro que deseas actualizar los datos?',
    'points': '¿Estás seguro de que deseas canjear tus puntos?',
};

// ALERTAS PARA PREGUNTAS DE CONFIRMACIÓN 
document.addEventListener("DOMContentLoaded", function () {
    const confirmButtons = document.querySelectorAll(".confirm-button");

    confirmButtons.forEach(function (button) {
        button.addEventListener("click", function (event) {
            event.preventDefault();

            // Se toman los valores cercanos al click y la info de los data={}
            const form = button.closest(".confirm-form");
            const formDelete = button.closest(".delete-form");
            const actionKey = button.getAttribute("data-action-key");
            const titleKey = button.getAttribute("data-title-key")
            // console.log("ACTIONKEY:", actionKey)
            // console.log("TITLEKEY", titleKey)

            // event.preventDefault();
    
            const action = actionDataTitles[actionKey]
            const title = confirmationTitles[titleKey]
            // console.log("ACTION", action)
            // console.log("TITLE", title)

            // data-action para definir acciones segun boton

            const swalButton = Swal.mixin({
                customClass:{
                confirmButton: 'btn btn-success m-1',
                cancelButton: 'btn btn-danger m-1'
                },
                buttonsStyling: false
            })
            swalButton.fire({
                title: title,
                icon: action,
                showCancelButton: true,
                confirmButtonText: "Confirmar",
                cancelButtonText: "Cancelar",
            }).then((result) => {
                if (result.isConfirmed) {
                    // Realiza la acción de eliminación
                        form.submit();         
                };
            });
        } // end if formValid

    ); // end listener
}); // end foreach

// analizamos si form es valido, para saltar alerta cuando ya ha finalizado la validación de django
// function isFormValid(form) {
//     const requiredInputs = form.querySelectorAll("[required]");

//     for (const input of requiredInputs) {
//         if (!input.value.trim()) {
//             return false;
//         }
//     }
//     return true;
//     }
}); // end DOMlistener



// FUNCION PARA CAPTURAR DESCRIPCION EN JOB PENDING

// function captureDescriptionJob() {
//     console.log("Capture Description Job function called");
//     // Captura el valor del campo description_job del primer formulario.
//     var descriptionJob = document.querySelector('#id_description_job').value;
//     console.log(descriptionJob);

//     // Asigna el valor capturado al campo oculto del segundo formulario.
//     document.querySelector('#description_job_cancel').value = descriptionJob;
// };

