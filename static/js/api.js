

$(document).ready(function() {
    $('#id_brand').change(function() {  // Asume que 'id_brand' es el ID del campo de selección de marca en tu formulario
        var brandSlug = $(this).val();
        var url = '/tu-url-para-obtener-modelos/' + brandSlug;  // Asegúrate de reemplazar esto con la URL correcta

        $.ajax({
            url: url,
            success: function(data) {
                var modelsSelect = $('#id_model');  // Asume que 'id_model' es el ID del campo de selección de modelo
                modelsSelect.empty();  // Limpia las opciones existentes
                modelsSelect.append($('<option>').val('').text('Elegir modelo vehículo'));  // Opción por defecto

                // Itera sobre los modelos y los añade al campo de selección
                $.each(data.models, function(index, model) {
                    modelsSelect.append($('<option>').val(model.slugmodelo).text(model.modelo));
                });
            }
        });
    });
});

