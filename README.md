`<link>` : <https://github.com/sebalopezx/Gestion_Automotriz_2.0>
`<link>` : <https://gestion-automotriz.onrender.com/>

![](https://github.com/sebalopezx/Gestion_Automotriz_2.0/blob/master/static/images/logo_car.png)
> Logo del proyecto

![Static Badge](https://img.shields.io/badge/versi%C3%B3n-2.0-orange)                            ![Static Badge](https://img.shields.io/badge/creador-Sebasti%C3%A1n%20L%C3%B3pez-orange)


**Tabla de Contenido**
*[TOCM]

[TOC]

## Tecnologías usadas

- Django
- Bootstrap 5
- SCSS
- Javascript
- JSON

## Descripción de la aplicación

El objetivo principal de este proyecto es implementar un eficiente sistema de reservas para el departamento de mantenimiento de un taller mecánico.
Este sistema permitirá gestionar la programación de citas de mantenimiento, cuentas de usuario, vehículos registrados, y un sistema de puntos para descuentos por servicio.
>Proyecto de estudio

## Detalles de uso
### Manejo de la aplicación
El sistema provee de tres intefaces de usuario:

##### Clientes
El cliente podra gestionar:
- Cuenta de usuario y password
- Agregar vehículos al sistema
- Agendar cita de mantenimiento
- Listar sus citas agendadas
- Listar sus vehículos
- Visualizar estado de vehículo en mantenimiento
![](https://github.com/sebalopezx/Gestion_Automotriz_2.0/blob/master/static/images/user_data.PNG)
> Información de usuario con puntos obtenidos y cupones canjeados

![](https://github.com/sebalopezx/Gestion_Automotriz_2.0/blob/master/static/images/register_vehicle.PNG)
> Registro de vehículos

![](https://github.com/sebalopezx/Gestion_Automotriz_2.0/blob/master/static/images/register_date2.PNG)
> Agendar cita de mantenimiento

![](https://github.com/sebalopezx/Gestion_Automotriz_2.0/blob/master/static/images/list_vehicles.PNG)
> Listar vehículos y entrar a ver estado en tiempo real

##### Recepcionista
El recepcionista podra gestionar:
- Gestionar de citas diarias (día actual)
- Gestionar todas las citas agendadas
- Gestionar citas finalizadas o canceladas
- Gestionar mecánicos

![](https://github.com/sebalopezx/Gestion_Automotriz_2.0/blob/master/static/images/list_jobs2.PNG)
> Listar vehículos con citas agendadas

![](https://github.com/sebalopezx/Gestion_Automotriz_2.0/blob/master/static/images/checklist_finalizado.PNG)
> Checklist de vehículo seleccionado y cambiar estados de mantenimiento

![](https://github.com/sebalopezx/Gestion_Automotriz_2.0/blob/master/static/images/list_mechanic.PNG)
> Listar mecánicos para su gestión

#### Administrador
El administrador del sistema tendra su interfaz propia donde:
- Gestionara todo los aspectos del sistema
- Gestionara valores, visualización de la página de inicio
- Gestionara nuevos recepcionistas

![](https://github.com/sebalopezx/Gestion_Automotriz_2.0/blob/master/static/images/admin.PNG)
> Panel de administración



## Instalación de entorno localhost

Para poder ejecutar el proyecto en un entorno de localhost, se debera:
1. Clonar el repositorio
```
git clone https://github.com/sebalopezx/Gestion_Automotriz_2.0
```
2. Abrir en editor de código, ir a modulo de settings dentro del proyecto y cambiar tres estados comentados del proyecto. 
El primero es descomentar DEBUG=True.
```
DEBUG = True
# DEBUG = 'RENDER' not in os.environ
```
El segundo es descomentar la base de datos a Sqlite3.
```
# DATABASES = {
#     'default': dj_database_url.config(
#         # default=os.environ.get('DATABASE_URL')
#         default='postgresql://postgres:postgres@localhost/postgres'
#     )
# }
DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
El tercero es descomentar la línea de SESSION = False.
```
# SESSION_COOKIE_SECURE = True  
SESSION_COOKIE_SECURE = False  
```

3. Ejecutar mediante cmd o dentro del terminal de Python el siguiente archivo:
```
ejectute_project.bat
```

> Este archivo contiene los **pip** para instalar todas las dependencias y requerimientos del proyecto creando todo dentro de un entorno virtual **'venv'** de Python.
