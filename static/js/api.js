// TEST DE API MEDIANTE JS

let DATA = null;
let URL = 'https://apicardetails-production.up.railway.app/vehiculos'

document.addEventListener('DOMContentLoaded', function() {
    // Cargar datos iniciales
    fetch(URL)
        .then(response => response.json())
        .then(data => {
            // console.log("Datos cargados desde la API:");
            // console.log(data);
            DATA = data;
            llenarMarcas();
        });

    // Evento change para marcas
    document.querySelector('#id_brand').addEventListener('change', function() {
        const marcaSeleccionada = this.value;
        llenarModelos(marcaSeleccionada);
    });

    // Evento change para modelos
    document.querySelector('#id_model').addEventListener('change', function() {
        const modeloSeleccionado = this.value;
        const marcaSeleccionada = document.querySelector('#id_brand').value;
        llenarAnios(marcaSeleccionada, modeloSeleccionado);
    });
});

const llenarMarcas = () => {
    const selectMarca = document.querySelector('#id_brand');
    // selectMarca.innerHTML = '<option value="">Seleccione una marca...</option>';

    DATA.forEach(marca => {
        const opcion = document.createElement('option');
        opcion.value = marca.slugmarca;
        opcion.textContent = marca.marca;
        selectMarca.appendChild(opcion);
    });
};

const llenarModelos = (marcaSeleccionada) => {
    const selectModelo = document.querySelector('#id_model');
    // selectModelo.innerHTML = '<option value="">Seleccione un modelo...</option>';

    const marca = DATA.find(m => m.slugmarca === marcaSeleccionada);
    if (marca && marca.modelos) {
        marca.modelos.forEach(modelo => {
            const opcion = document.createElement('option');
            opcion.value = modelo.slugmodelo;
            opcion.textContent = modelo.modelo;
            selectModelo.appendChild(opcion);
        });
    }
    // document.querySelector('#hidden_brand').value = marcaSeleccionada;
};

const llenarAnios = (marcaSeleccionada, modeloSeleccionado) => {
    const selectAnio = document.querySelector('#id_year');
    // selectAnio.innerHTML = '<option value="">Seleccione un año...</option>';

    const marca = DATA.find(m => m.slugmarca === marcaSeleccionada);
    const modelo = marca?.modelos.find(m => m.slugmodelo === modeloSeleccionado);
    const anios = modelo?.anios || [];

    anios.forEach(anio => {
        const opcion = document.createElement('option');
        opcion.value = anio;
        opcion.textContent = anio;
        selectAnio.appendChild(opcion);
    });
    // document.querySelector('#hidden_model').value = modeloSeleccionado;
};

