from django.contrib.auth.models import User, Group

from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.utils import timezone

from Management.models import Appointment, Attention, Checklist, Coupon, Description, Job, Mechanic, Point, Service, TitleHeader, Vehicle, VehicleStatus, Work, Workshop


""" First data for de application """

# USERS AND ADMINS


@receiver(post_migrate)
def create_admin(sender, **kwargs):
    user, created = User.objects.get_or_create(
        id=1,
        defaults={
            'username': "admin",
            "first_name": "admin",
            "email": "admin@ga.cl",
            "is_superuser": True,
            "is_staff": True,
            "is_active": True,
            "date_joined": timezone.now(),
        },
    )
    if created:
        user.set_password("admin")
        user.save()


@receiver(post_migrate)
def create_recepcionist(sender, **kwargs):
    user, created = User.objects.get_or_create(
        id=2,
        defaults={
            'username': "recepcionista",
            "first_name": "Alan",
            "last_name": "Brito",
            "email": "recepcionista@ga.cl",
            "is_superuser": False,
            "is_staff": True,
            "is_active": True,
            "date_joined": timezone.now(),
        },
    )
    if created:
        user.set_password("123")
        user.save()

    group = Group.objects.get(name='Recepcionist')
    user.groups.add(group)


@receiver(post_migrate)
def create_client(sender, **kwargs):
    user, created = User.objects.get_or_create(
        id=3,
        defaults={
            'username': "cliente",
            "first_name": "Alan",
            "last_name": "Brito",
            "email": "alan@gmail.com",
            "is_superuser": False,
            "is_staff": False,
            "is_active": True,
            "date_joined": timezone.now(),
        },
    )
    if created:
        user.set_password("123")
        user.save()

    group = Group.objects.get(name='Customer')
    user.groups.add(group)


# SERVICES
@receiver(post_migrate)
def create_services(sender, **kwargs):
    services_data = [
        {'id': 1, 'name': 'Servicio diagnóstico', 'price': 10000, 'earn_points': 10}, 
        {'id': 2, 'name': 'Cambio pastillas o balatas de frenos', 'price': 50000, 'earn_points': 50},
        {'id': 3, 'name': 'Cambio líquido frenos y purga', 'price': 30000, 'earn_points': 30},
        {'id': 4, 'name': 'Cambio bujía', 'price': 10000, 'earn_points': 5},
        {'id': 5, 'name': 'Cambio de aceite', 'price': 20000, 'earn_points': 15},
        {'id': 6, 'name': 'Cambio de neumáticos', 'price': 40000, 'earn_points': 40},
        {'id': 7, 'name': 'Alineación y Balanceo', 'price': 20000, 'earn_points': 15},
        {'id': 8, 'name': 'Cambio de correa', 'price': 80000, 'earn_points': 80},
    ]

    for service in services_data:
        service, created = Service.objects.get_or_create(
            id=service['id'],
            defaults={
                'name': service['name'],
                "price": service['price'],
                "earn_points": service['earn_points'],
            }
        )


# ATTENTIONS
@receiver(post_migrate)
def create_attentions(sender, **kwargs):
    attention_data = [
        {'id': 1, 'attention': '8:00'},
        {'id': 2, 'attention': '13:00'},
    ]
    for attention in attention_data:
        attention, created = Attention.objects.get_or_create(
            id=attention['id'],
            defaults={
                'attention': attention['attention']
            }
        )


# MECHANICS
@receiver(post_migrate)
def create_mechanics(sender, **kwargs):
    mechanics_data = [
        {'id':1, 'first_name': 'Félix ', 'last_name': 'Turbo', 'phone': '123456789', 'specialty': 'mecanico', 'image': 'mechanics/mecanico1.png', 'is_active': True},
        {'id':2, 'first_name': 'Gaspar', 'last_name': 'Pistones', 'phone': '987654321', 'specialty': 'mecanico', 'image': 'mechanics/mecanico2.png', 'is_active': True},
        {'id':3, 'first_name': 'Mario ', 'last_name': 'Neta', 'phone': '123123123', 'specialty': 'electrico', 'image': 'mechanics/electrico1.png', 'is_active': True},
        {'id':4, 'first_name': 'Alex', 'last_name': 'Tintor', 'phone': '321321321', 'specialty': 'electrico', 'image': 'mechanics/electrico2.png', 'is_active': False},
    ]
    for mechanic in mechanics_data:
        mechanic, created = Mechanic.objects.get_or_create(
            id=mechanic['id'],
            defaults={
                'first_name': mechanic['first_name'],
                "last_name":  mechanic['last_name'],
                "phone":  mechanic['phone'],
                "specialty":  mechanic['specialty'],
                "image": mechanic['image'],
                "is_active": mechanic['is_active'],
            }
        )


# WORKSHOP
@receiver(post_migrate)
def create_workshops(sender, **kwargs):
    workshop, created = Workshop.objects.get_or_create(
        defaults={
            'name': "Taller Automotriz Maipú",
            "address": "Maipú, Calle Saturno",
            "num_address": 999,
        }
    )


# STATES
@receiver(post_migrate)
def create_status(sender, **kwargs):
    status_data = [
        {'id': 1, 'status': 'En espera'},  
        {'id': 2, 'status': 'En diagnóstico'},  
        {'id': 3, 'status': 'En espera confirmación de presupuesto'},  
        {'id': 4, 'status': 'En mantención'},  
        {'id': 5, 'status': 'En espera de repuesto'},  
        {'id': 6, 'status': 'Listo para entrega'},  
        {'id': 7, 'status': 'Finalizado'},  
        {'id': 8, 'status': 'Cancelado'},  
        {'id': 9, 'status': 'Eliminado'},  
    ]
    for status in status_data:
        status, created = VehicleStatus.objects.get_or_create(
            id=status['id'],
            defaults={
                'status': status['status']
            }
        )



# INDEX
@receiver(post_migrate)
def create_title_headers(sender, **kwargs):
    titles_data = [
        {'id': 1, "title": "INDEX"},
        {'id': 2, "title": "Bienvenido"},
        {'id': 3, "title": "Aplicación de gestión de citas"},
    ]
    
    for title in titles_data:
        TitleHeader.objects.get_or_create(
            title_header=title["title"]
        )


@receiver(post_migrate)
def create_descriptions(sender, **kwargs):
    descriptions_data = [
        {
            "id": 1,
            "title": "Agendar y reservar citas de mantenimiento",
            "description": "Este sistema le permitirá planificar y agendar citas de mantenimiento para servicios tanto correctivos como preventivos, brindándoles la flexibilidad de elegir una hora conveniente para llevar a cabo el trabajo en sus vehículos. Además de eso podrán elegir el mecánico y la sucursal según sus gustos y preferencias.",
            "description_small": "Podrá registrar más de un vehículo.",
            "image_description": "index/mantenimiento.png",
            "have_constant": False,
        },
        {
            "id": 2,
            "title": "Visualizar el estado de tu vehículo",
            "description": "Al ingresar su vehículo al sistema y reservar una cita, podrá revisar diariamente el estado de su vehículo, viendo los servicios que están en proceso y finalizados, además de un listado de características fundamentales de su vehículo.",
            "description_small": "Detalles de servicios, presupuesto y checklist.",
            "image_description": "index/checklist.png",
            "have_constant": False,
        },
        {
            "id": 3,
            "title": "Descuentos exclusivos",
            "description": "Con cada mantenimiento que realice con esta aplicación podrá conseguir puntos. Con una acumulación de cierta cantidad de puntos podrá canjear un cupón en su próximo mantenimiento, para tener descuentos del 10%.",
            "description_small": "Puntos para canjear cupón:",
            "image_description": "index/cupon.png",
            "have_constant": True,
        },
         {
            "id": 4,
            "title": "Gestionar mecánicos",
            "description": "El sistema le permitirá gestionar los mecánicos del taller, pudiendo agregar, modificar o eliminar en caso de ser necesario.",
            "description_small": "Se puede añadir imagen tipo carnet, o se usara una por defecto.",
            "image_description": "index/list_mechanic.png",
            "have_constant": False,
        },
         {
            "id": 5,
            "title": "Gestionar citas de mantenimiento",
            "description": "El sistema tendrá múltiples interfaces para el control de citas. Citas diarias muestran las citas registradas en el día actual. Citas en progreso muestra listado de todas las citas. Citas finalizadas o canceladas. Y por ultimo un buscador para citas por patente o número de cita.",
            "description_small": "Botones para agregar descripcion y servicios, boton para modificar estado de checklist, y botones para cancelar cita o finalizar (Estos 2 ultimos se activan o desactivan según el estado del vehículo)",
            "image_description": "index/list_jobs2.png",
            "have_constant": False,
        },
         {
            "id": 6,
            "title": "Gestionar estado de vehículo",
            "description": "El sistema tendrá 2 opciones para agregar detalles, descripciones y servicios y otra para modificar el estado del vehículo por medio de un checklist.",
            "description_small": "Este sistema mostrara en tiempo real el estado del vehículo al cliente.",
            "image_description": "index/state_vehicle.png",
            "have_constant": False,
        },
    ]

    for description in descriptions_data:
        description, created = Description.objects.get_or_create(
            id=description['id'],
            defaults={
                'title': description['title'],
                'description': description['description'],
                'description_small': description['description_small'],
                'image_description': description['image_description'],
                'have_constant': description['have_constant'],
            }
        )



""" Second data for de application """

@receiver(post_migrate)
def create_vehicles(sender, **kwargs):
    customer = User.objects.get(id=3)

    vehicles_data = [
        {'id': 1, "brand": "Chevrolet", "model": "Onix", "patent": "ABC123", "year": 2021, "is_active": True},
        {'id': 2, "brand": "Toyota", "model": "Corolla", "patent": "XYZ789", "year": 2017, "is_active": True},
    ]
    for vehicle in vehicles_data:
        vehicle, created = Vehicle.objects.get_or_create(
            id=vehicle['id'],
            defaults={
                'customer': customer,
                "brand": vehicle['brand'],
                "model": vehicle['model'],
                "patent": vehicle['patent'],
                "year": vehicle['year'],
                "is_active": vehicle['is_active'],
            }
        )


@receiver(post_migrate)
def create_appointments(sender, **kwargs):

    customer = User.objects.get(id=3)
    vehicles = Vehicle.objects.filter(customer=customer)
    vehicle1 = vehicles[0]
    vehicle2 = vehicles[1]

    # APPOINTMENT 1

    attention1 = Attention.objects.get(id=1)
    mechanic1 = Mechanic.objects.get(id=1)
    workshop = Workshop.objects.get(id=1)

    appointment1, created = Appointment.objects.get_or_create(
        vehicle=vehicle1,
        attention=attention1,
        defaults={
            "date_created": "2023-11-20T08:00:00Z",
            "date_register": "2023-11-24",
            "date_finished": "2023-11-27T13:30:00Z",
            "mechanic": mechanic1,
            "workshop": workshop,
            "description_customer": "Frenos en mal estado",
            "inprogress": True,
            "completed": True,
        }
    )

    job1, created = Job.objects.get_or_create(
        appointment=appointment1,
        defaults={
            "description_job": "Revisión de frenos y cambio de pastillas",
            "status": VehicleStatus.objects.get(id=7)
        }
    )

    Work.objects.get_or_create(job=job1, service=Service.objects.get(id=1), defaults={"status_service": True})
    Work.objects.get_or_create(job=job1, service=Service.objects.get(id=2), defaults={"status_service": True})
    Work.objects.get_or_create(job=job1, service=Service.objects.get(id=3), defaults={"status_service": False})

    Checklist.objects.get_or_create(
        job=job1,
        defaults={
            "km": 55123,
            "gasoline_tank": "1",
            "front_lights": True,
            "rear_lights": True,
            "chassis": True,
            "cleaning": True,
            "extinguisher": True,
            "first_aid_kit": False,
            "triangles": True,
            "hydraulic_jack": True,
            "spare_wheel": True,
        }
    )

    point, created = Point.objects.get_or_create(
        customer=customer,
        defaults={
            "points": 470,
        }
    )

    coupon, created = Coupon.objects.get_or_create(
        customer=customer,
        defaults={
            "coupon": "AuIjvbrz",
            "valid": True,
        }
    )

    # APPOINTMENT 2

    attention2 = Attention.objects.get(id=2)
    mechanic2 = Mechanic.objects.get(id=2)

    appointment2, created = Appointment.objects.get_or_create(
        vehicle=vehicle1,
        attention=attention2,
        defaults={
            "date_created": "2023-12-01T08:00:00Z",
            "date_register": "2023-12-05",
            # "date_finished": None,
            "mechanic": mechanic2,
            "workshop": workshop,
            "description_customer": "Check engine encendido",
            "inprogress": True,
            "completed": False,
        }
    )

    job2, created = Job.objects.get_or_create(
        appointment=appointment2,
        defaults={
            # "description_job": "Cita de mantenimiento agendada",
            "status": VehicleStatus.objects.get(id=1)
        }
    )

    Checklist.objects.get_or_create(
        job=job2,
        defaults={
            "km": 0,
            "gasoline_tank": "1",
            "front_lights": False,
            "rear_lights": False,
            "chassis": False,
            "cleaning": False,
            "extinguisher": False,
            "first_aid_kit": False,
            "triangles": False,
            "hydraulic_jack": False,
            "spare_wheel": False,
        }
    )
