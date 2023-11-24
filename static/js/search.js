// Evitar el envío del formulario si el buscador 'patent' está vacío
document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('search-nav'); 

    searchForm.addEventListener('submit', function(event) {
    const patentInput = document.querySelector('[name="patent"]');
    if (patentInput.value.trim() === '') {
        event.preventDefault();  
        return false;           
    }
    });
});
