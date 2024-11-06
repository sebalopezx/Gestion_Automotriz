from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return (user.is_superuser and user.is_staff)

def is_customer(user):
    # return user.groups.filter(name='Customer').exists()
    return (user.groups.filter(name='Customer').exists() and not user.is_staff and not user.is_superuser)

def is_recepcionist(user):
    # return user.groups.filter(name='Recepcionist').exists()
    return (user.groups.filter(name='Recepcionist').exists() and user.is_staff and not user.is_superuser) 


# Decorador de vista para vistas exclusivas de administradores
admin_required = user_passes_test(is_admin)

# Decorador de vista para vistas exclusivas de clientes
customer_required = user_passes_test(is_customer)

# Decorador de vista para vistas exclusivas de recepcionistas
recepcionist_required = user_passes_test(is_recepcionist)

