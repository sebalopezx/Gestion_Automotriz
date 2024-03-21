// // FUNCIONES PARA FORMULARIOS MULTIPLES DE CHECKLIST
// document.addEventListener('DOMContentLoaded', function() {
    // Manejar el envío del formulario principal
    const btnChecklist = document.getElementById("btn_update_checklist");

    if (btnChecklist) {
        btnChecklist.addEventListener('click', function() {
            // e.preventDefault();
            let form = document.getElementById("form_update_checklist");
            form.submit();
        });
    }
//     } else {
//         console.error('El botón btn_update_checklist no se encontró');
//     }

//     // Agregar event listeners a los botones de los formularios de servicios
//     document.querySelectorAll('.service-delete-button').forEach(button => {
//         button.addEventListener('click', handleServiceFormSubmit);
//     });
// });

// // Función para manejar el envío de los formularios de servicios
// function handleServiceFormSubmit(event) {
//     event.preventDefault();
//     const serviceForm = event.target.closest('form');
//     console.log('Formulario de servicio enviado:', serviceForm.id);
// }

// // Función para manejar el envío de los formularios de servicios
// function handleServiceFormSubmit(event) {
//     event.preventDefault();

//     const serviceForm = event.target.closest('form');
//     // Lógica para el envío del formulario de servicio
//     console.log('Formulario de servicio enviado:', serviceForm.id);
// }


// // Manejar el envío del formulario principal
// btnChecklist.addEventListener('click', function(e){
//     e.preventDefault();
//     let form = document.getElementById("form_update_checklist");
//     form.submit();
// });






// document.addEventListener('DOMContentLoaded', () => {
//     // Agregar un event listener a cada formulario
//     document.querySelectorAll('.confirm-form').forEach(form => {
//         form.addEventListener('submit', function(e) {
//             // Prevenir el envío automático
//             e.preventDefault();

//             // Obtener el ID del formulario
//             const formId = this.id;
//             console.log('Formulario enviado:', formId);

//             // Aquí decides qué hacer según el ID del formulario
//             if (formId.startsWith('form_services')) {
//                 // Lógica específica para formularios de servicios
//                 console.log('Manejando el formulario de servicios:', formId);

//                 // Aquí puedes implementar la lógica para manejar el formulario.
//                 // Por ejemplo, puedes enviar manualmente los datos del formulario
//                 // a un endpoint específico o realizar cualquier otra acción necesaria.

//                 // Ejemplo de cómo podrías enviar el formulario manualmente
//                 // (Deberás sustituir 'tuUrlDeDestino' con la URL a la que deseas enviar el formulario)
//                 const actionUrl = this.action; // o tu URL específica
//                 const formData = new FormData(this);

//                 fetch(actionUrl, {
//                     method: 'POST',
//                     body: formData,
//                 })
//                 .then(response => response.json())
//                 .then(data => {
//                     console.log('Respuesta recibida:', data);
//                     // Aquí puedes manejar la respuesta, como mostrar un mensaje al usuario
//                 })
//                 .catch(error => {
//                     console.error('Error al enviar el formulario:', error);
//                 });

//             } else {
//                 // Lógica para otros formularios, si es necesaria
//             }
//         });
//     });
// });















// // Capturar el formulario de servicios por su id
// const formServices = document.getElementById("form_services");

// btnChecklist = document.getElementById("btn_update_checklist");

// btnChecklist.addEventListener('click', function(e){
//     e.preventDefault();

//     // Verificar si el botón se encuentra en el primer formulario de servicios
//     if (formServices && formServices.contains(e.target)) {
//         // Si el botón se encuentra en el primer formulario de servicios, enviar el formulario principal
//         let form = document.getElementById("form_update_checklist");
//         form.submit();
//     }
// });








// btnChecklist.addEventListener('click', function(e){
//     // Obtenenemos los 3 formularios
//     e.preventDefault();
//     let form = document.getElementById("form_update_checklist");

//     // Enviar y guardar
//     form.submit();
// })