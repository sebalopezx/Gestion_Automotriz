from django.db import models
from django.contrib.auth.models import User, Group
from django.forms import CheckboxInput, DateField, DateTimeField, TimeField

import string
import secrets

# Validadores
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator


# Create your groups here.
# Crear el grupo de clientes
# group_customer, created = Group.objects.get_or_create(name='Customer')
# Crear el grupo de recepcionistas
# group_recepcionist, created = Group.objects.get_or_create(name='Recepcionist')


# Create your models here.


class Vehicle(models.Model):
    customer = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                null=False,
                                blank=False,)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    patent = models.CharField(max_length=10)
    year = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.brand.capitalize()} {self.model.capitalize()}, Patente: {self.patent}  de: {self.customer.first_name} {self.customer.last_name}"

class Workshop(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    num_addres = models.IntegerField()

    def __str__(self):
        return f"{self.name}. {self.address} # {self.num_addres}"

class Mechanic(models.Model):
    SPECIALTY_CHOICES = (
        ('Mecánico', 'Mecánico'),
        ('Eléctrico', 'Eléctrico'),
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=9,
                             validators=[
                                MaxLengthValidator(limit_value=9)
                             ])
    specialty = models.CharField(max_length=50, choices=SPECIALTY_CHOICES, blank=True)
    image = models.ImageField(upload_to='mechanics/', default="mechanics/foto_personal.jpg")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Attention(models.Model):
    attention = models.TimeField()
    def formatted_attention(self):
        if self.attention.hour == 8:
            context = ('AM')
        else:
            context = ('PM') 
        return f"{self.attention.__format__('%H:%M')} {context}"
    
    def __str__(self):
        return f"{self.formatted_attention()}"

class Appointment(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
    attention = models.ForeignKey(Attention, on_delete=models.CASCADE)
    date_register = models.DateField()
    date_created = models.DateTimeField(auto_now_add=True) # auto add: ingresa time automaticamente si no se ingresa manualmente
    date_finished = models.DateTimeField(null=True, blank=True) # Blank , se puede dejar vacio para llenado posterior
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    description_customer = models.TextField(null=True, blank=True)
    inprogress = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Cita para vehículo: {self.vehicle} ~> Fecha de la Cita: {self.date_register.strftime('%d-%m-%Y')} {self.attention}"  

class Service(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    earn_points = models.PositiveIntegerField()

    def formatted_price(self):
        return '${:,.0f} pesos'.format(self.price)
    
    def __str__(self):
        return f"{self.id}. {self.name} {self.formatted_price()}"


class VehicleStatus(models.Model):
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.status}"

class Job(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    description_job = models.TextField(null=True, blank=True)
    status = models.ForeignKey(VehicleStatus, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.appointment}"

class Work(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    status_service = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}. {self.job} {self.service} {self.status_service}"

class Point(models.Model):
    customer = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                null=False,
                                blank=False,)
    points = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f" {self.customer} - Puntos: {self.points}"

class Coupon(models.Model):
    customer = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 null=False,
                                 blank=False)
    coupon = models.CharField(max_length=50, unique=True)
    valid = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.coupon}"

    @staticmethod
    def generate_coupon_code():
        # Generar un código de cupón único
        alphabet = string.ascii_letters + string.digits
        coupon = ''.join(secrets.choice(alphabet) for i in range(8))  # Ajustar la longitud del cupon
        return coupon

class Checklist(models.Model):
    job = models.OneToOneField(Job, on_delete=models.CASCADE)
    front_lights = models.BooleanField(default=False)
    rear_lights = models.BooleanField(default=False)
    chassis = models.BooleanField(default=False)
    cleaning = models.BooleanField(default=False)  
    extinguisher = models.BooleanField(default=False)
    first_aid_kit = models.BooleanField(default=False)
    triangles = models.BooleanField(default=False)
    hydraulic_jack = models.BooleanField(default=False)
    spare_wheel = models.BooleanField(default=False)

    def __str__(self):
        return f"""Checklist: 
                {self.id}.
                {self.front_lights}
                {self.rear_lights}
                {self.chassis} 
                {self.cleaning} 
                {self.extinguisher} 
                {self.first_aid_kit}
                {self.triangles}
                {self.hydraulic_jack}
                {self.spare_wheel}"""
