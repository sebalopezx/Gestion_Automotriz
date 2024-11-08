from django.contrib.auth.models import User


from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.utils import timezone

from Management.models import Appointment, Attention, Checklist, Coupon, Job, Mechanic, Point, Service, Vehicle, VehicleStatus, Work, Workshop


""" First data for de application """

# USERS AND ADMINS


@receiver(post_migrate)
def create_admin(sender, **kwargs):
    user, created = User.objects.get_or_create(
        username="cliente",
        defaults={
            "first_name": "admin",
            "email": "admin@gmail.com",
            "is_superuser": True,
            "is_staff": True,
            "is_active": True,
            "date_joined": timezone.now(),
        },
    )
    if created:
        user.set_password("123")
        user.save()


@receiver(post_migrate)
def create_recepcionist(sender, **kwargs):
    user, created = User.objects.get_or_create(
        username="recepcionista",
        defaults={
            "first_name": "Alan",
            "last_name": "Brito",
            "email": "recepcionista@ga.com",
            "is_superuser": False,
            "is_staff": True,
            "is_active": True,
            "date_joined": timezone.now(),
        },
    )
    if created:
        user.set_password("123")
        user.save()


@receiver(post_migrate)
def create_client(sender, **kwargs):
    customer, created = User.objects.get_or_create(
        username="cliente",
        defaults={
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
        customer.set_password("123")
        customer.save()


# SERVICES
@receiver(post_migrate)
def create_services(sender, **kwargs):
    services_data = [
        {'name': 'Servicio diagnóstico', 'price': 10000, 'earn_points': 10},
        {'name': 'Cambio pastillas o balatas de frenos',
            'price': 50000, 'earn_points': 50},
        {'name': 'Cambio líquido frenos y purga',
            'price': 30000, 'earn_points': 30},
        {'name': 'Cambio bujía', 'price': 10000, 'earn_points': 5},
        {'name': 'Cambio de aceite', 'price': 20000, 'earn_points': 15},
        {'name': 'Cambio de neumáticos', 'price': 40000, 'earn_points': 40},
        {'name': 'Alineación y Balanceo', 'price': 20000, 'earn_points': 15},
        {'name': 'Cambio de correa', 'price': 80000, 'earn_points': 80},
    ]

    for service in services_data:
        service, created = Service.objects.get_or_create(
            name=service['name'],
            defaults={
                "price": service['price'],
                "earn_points": service['earn_points'],
            }
        )


# ATTENTIONS
@receiver(post_migrate)
def create_attentions(sender, **kwargs):
    attention_data = [
        {'attention': '8:00'},
        {'attention': '13:00'},
    ]
    for attention in attention_data:
        attention, created = Attention.objects.get_or_create(
            attention=attention['attention']
        )


# MECHANICS
@receiver(post_migrate)
def create_mechanics(sender, **kwargs):
    mechanics_data = [
        {'first_name': 'Mario', 'last_name': 'Neta', 'phone': '123456789',
            'specialty': 'mecanico', 'image': 'mechanics/mecanico1', 'is_active': True},
        {'first_name': 'Alex', 'last_name': 'Tintor', 'phone': '987654321',
            'specialty': 'mecanico', 'image': 'mechanics/mecanico2', 'is_active': True},
        {'first_name': 'Mario', 'last_name': 'Neta', 'phone': '123123123',
            'specialty': 'electrico', 'image': 'mechanics/electrico1', 'is_active': True},
        {'first_name': 'Mario', 'last_name': 'Neta', 'phone': '321321321',
            'specialty': 'electrico', 'image': 'mechanics/electrico2', 'is_active': False},
    ]
    for mechanic in mechanics_data:
        mechanic, created = Mechanic.objects.get_or_create(
            first_name=mechanic['first_name'],
            defaults={
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
        name="Taller Automotriz Maipú",
        defaults={
            "address": "Maipú, Calle Saturno",
            "num_address": 999,
        }
    )

# STATES


@receiver(post_migrate)
def create_status(sender, **kwargs):
    status_data = [
        {'status': 'En espera'}, # 1
        {'status': 'En diagnóstico'}, # 2
        {'status': 'En espera confirmación de presupuesto'}, # 3
        {'status': 'En mantención'}, # 4
        {'status': 'En espera de repuesto'}, # 5
        {'status': 'Listo para entrega'}, # 6
        {'status': 'Finalizado'}, # 7
        {'status': 'Cancelado'}, # 8
        {'status': 'Eliminado'}, # 9
    ]
    for status in status_data:
        status, created = VehicleStatus.objects.get_or_create(
            status=status['status']
        )

# POINTS

# INDEX
# 1


""" Second data for de application """

@receiver(post_migrate)
def create_vehicles(sender, **kwargs):
    customer = User.objects.get(id=3)

    vehicles_data = [
        {"brand": "Chevrolet", "model": "Onix", "patent": "ABC123", "year": 2021, "is_active": True},
        {"brand": "Toyota", "model": "Corolla", "patent": "XYZ789", "year": 2017, "is_active": True},
    ]
    for vehicle in vehicles_data:
        vehicle, created = Vehicle.objects.get_or_create(
            customer=customer,
            defaults = {
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
            "date_created": timezone.datetime(2023, 11, 20, 8, 0),
            "date_register": timezone.datetime(2023, 11, 24),
            "date_finished": timezone.datetime(2023, 11, 27, 13, 30),
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
            "points": 90,
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
        vehicle=vehicle2,
        attention=attention2,
        defaults={
            "date_created": timezone.datetime(2023, 12, 1, 8, 0),
            "date_register": timezone.datetime(2023, 12, 5),
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
