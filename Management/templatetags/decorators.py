from django.contrib.auth.decorators import user_passes_test

def is_customer(user):
    return user.groups.filter(name='Customer').exists()

def is_recepcionist(user):
    return user.groups.filter(name='Recepcionist').exists()

# Decorador de vista para vistas exclusivas de clientes
customer_required = user_passes_test(is_customer)

# Decorador de vista para vistas exclusivas de recepcionistas
recepcionist_required = user_passes_test(is_recepcionist)
