document.addEventListener("DOMContentLoaded", function() {
    const discountButton = document.getElementById('btnDiscount'); 

    if (discountButton && !discountButton.disabled){

    // Obtener el precio total desde el atributo data
    const total_price = parseFloat(discountButton.getAttribute('data-total-price'));

    // Agregar un event listener al botón
    discountButton.addEventListener('click', function() {
        const element = document.getElementById('discount');
        const discount = 0.90;

        if (!isNaN(total_price)) {
            const discounted_price = total_price * discount;
            const formatted_price = discounted_price.toLocaleString('es-CL', {
                style: 'currency',
                currency: 'CLP'
            });

            element.innerHTML = `Precio con descuento: ${formatted_price} pesos.`;
        } else {
            alert('El precio total no es válido.');
        }
    });
    }
});