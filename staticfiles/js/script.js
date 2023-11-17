// TOAST DE ALERTAS PARA CONFIRMACIÓN Y ERRORES

document.addEventListener("DOMContentLoaded", function () {
    const toastContainer = document.getElementById("toast-container");

    // Función para crear y mostrar un toast
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
        const messageText = messageElement.getAttribute("data-message");
        const messageClass = messageElement.getAttribute("data-message-class");
        showToast(messageText, messageClass);
    });
});





// ALERTAS PARA PREGUNTAS DE CONFIRMACIÓN 

document.addEventListener("DOMContentLoaded", function () {
    const confirmButtons = document.querySelectorAll(".confirm-button");

    confirmButtons.forEach(function (button) {
        button.addEventListener("click", function (event) {
        // const shouldPreventDefault = button.getAttribute("data-prevent-default") === "true";

        // if (shouldPreventDefault) {
        //   event.preventDefault(); // Prevenir el envío automático del formulario
        // }
        // event.preventDefault();

        const action = button.getAttribute("data-action");
        const form = button.closest(".confirm-form");

        if (isFormValid(form)){
            event.preventDefault();
      
            // data-action para definir acciones segun boton
            // acción de eliminar
            if (action === "delete") {
                const swalButton = Swal.mixin({
                    customClass:{
                    confirmButton: 'btn btn-success m-1',
                    cancelButton: 'btn btn-danger m-1'
                    },
                    buttonsStyling: false
                })
                swalButton.fire({
                    title: "¿Estás seguro de que deseas eliminar o cancelar?",
                    icon: "warning",
                    showCancelButton: true,
                    confirmButtonText: "Confirmar",
                    cancelButtonText: "Cancelar",
                }).then((result) => {
                    if (result.isConfirmed) {
                        // Realiza la acción de eliminación
                        form.submit();
                    };
                });

            } else if (action === "confirm") {
                // acción de confirmación
                const swalButton = Swal.mixin({
                    customClass:{
                    confirmButton: 'btn btn-success m-1',
                    cancelButton: 'btn btn-danger m-1'
                    },
                    buttonsStyling: false
                })
                swalButton.fire({
                    title: "¿Estás seguro de que deseas realizar esta acción?",
                    icon: "question",
                    showCancelButton: true,
                    confirmButtonText: "Confirmar",
                    cancelButtonText: "Cancelar",
                }).then((result) => {
                    if (result.isConfirmed) {
                        // Realiza la acción de eliminación
                        form.submit();
                    };
                });

            } else if (action === "points") {
                // acción de puntos
                const swalButton = Swal.mixin({
                    customClass:{
                        confirmButton: 'btn btn-success m-1',
                        cancelButton: 'btn btn-danger m-1'
                    },
                    buttonsStyling: false
                })
                swalButton.fire({
                    title: "¿Estás seguro de que deseas canjear tus puntos?",
                    icon: "question",
                    showCancelButton: true,
                    confirmButtonText: "Canjear",
                    cancelButtonText: "Cancelar",
                }).then((result) => {
                    if (result.isConfirmed) {
                        // Realiza la acción de eliminación
                        form.submit();
                    };
                });

            } // end if action
        } // end if formValid

        }); // end listener
    }); // end foreach
  
// analizamos si form es valido, para saltar alerta cuando ya ha finalizado la validación de django
function isFormValid(form) {
    const requiredInputs = form.querySelectorAll("[required]");

    for (const input of requiredInputs) {
        if (!input.value.trim()) {
            return false;
        }
    }
    return true;
    }
}); // end DOMlistener



// FUNCION PARA CAPTURAR DESCRIPCION EN JOB PENDING

function captureDescriptionJob() {
    // Captura el valor del campo description_job del primer formulario.
    var descriptionJob = document.querySelector('#id_description_job').value;

    // Asigna el valor capturado al campo oculto del segundo formulario.
    document.querySelector('#description_job_cancel').value = descriptionJob;
};

