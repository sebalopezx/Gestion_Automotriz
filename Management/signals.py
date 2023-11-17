
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group
from django.db import connection

def create_groups(sender, **kwargs):
    if "default" not in connection.alias:
        # Solo ejecutar esto en la base de datos predeterminada
        return

    # Crear el grupo de clientes si no existe
    group_customer, created = Group.objects.get_or_create(name='Customer')

    # Crear el grupo de recepcionistas si no existe
    group_recepcionist, created = Group.objects.get_or_create(name='Recepcionist')

post_migrate.connect(create_groups)
