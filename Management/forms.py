from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Vehicle, VehicleStatus, Workshop, Appointment, Mechanic, Job, Checklist, Point, Attention, Service, Work

from django.forms import DateTimeInput, DateField, DateInput
from django.utils import timezone
import datetime
from django.utils.text import capfirst
# Validadores
import re
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import json
from django.core.validators import RegexValidator

# Clase global para capitalize
class CapitalizeField:
    def clean_capitalize_nameField(self, field_name):
        field_value = self.cleaned_data.get(field_name)
        return field_value.title() if field_value else field_value
    
    def clean_capitalize_field(self, field):
        field_value = self.cleaned_data.get(field)
        return field_value.capitalize() if field_value else field_value

# Create your forms here.


class UpdateUserCustomForm(CapitalizeField, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Email'
        }

    def clean_first_name(self):
        return self.clean_capitalize_nameField('first_name')
    
    def clean_last_name(self):
        return self.clean_capitalize_nameField('last_name')
    

class CustomUserCreationForm(CapitalizeField, UserCreationForm):  
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')
        labels = {
            'username': 'Nombre de usuario',
            'password1': 'Password',
            'password2': 'Confirmación Password',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Email'
        }

    def clean_first_name(self):
        return self.clean_capitalize_nameField('first_name')
    
    def clean_last_name(self):
        return self.clean_capitalize_nameField('last_name')


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['brand', 'model', 'patent', 'year']
        labels = {
            'brand': 'Marca',
            'model': 'Modelo',
            'patent': 'Patente',
            'year': 'Año'
        }
        widgets = {
            'brand': forms.Select(choices=[('','Elegir marca vehículo'), ('ford', 'Ford'), ('toyota', 'Toyota'), ('honda', 'Honda')]),
            'model': forms.Select(choices=[('','Elegir modelo vehículo'), ('focus', 'Focus'), ('corolla', 'Corolla'), ('civic', 'Civic')]),
            'year': forms.Select(choices=[('','Elegir Año vehículo')] + [(year, year) for year in range(datetime.date.today().year, 1920, -1)])
        }

    def clean_patent(self):
        patent = self.cleaned_data['patent']
        # Expresiones regulares para identificar solo números y letras
        if not re.match("^[A-Za-z0-9]*$", patent):
            raise forms.ValidationError("La patente solo debe contener letras(A-Z) y números(0-9)")
        # Validación para patentes únicas
        if Vehicle.objects.filter(patent=patent).exists():
            raise forms.ValidationError("Ya existe un vehículo con esta patente.")
        return patent.upper()





class AppointmentForm(CapitalizeField, forms.ModelForm):
    
    def __init__(self, *args, user=None):
        super().__init__(*args)
        if user is not None:
            self.fields['vehicle'].queryset = Vehicle.objects.filter(customer=user)

    class Meta:
        model = Appointment
        fields = ['vehicle','attention','date_register','mechanic','workshop','description_customer']
        labels = {
            'vehicle':'Vehículo',
            'attention':'Atención',
            'date_register':'Fecha',
            'mechanic':'Mecánico',
            'workshop':'Sucursal',
            'description_customer':'Descripción'
        }
        widgets = {
             'date_register': DateInput(
                format='%Y-%m-%d',  # Formato de la fecha que se muestra
                attrs={
                    'type': 'date',
                    # cadena que representa 'AAAA-MM-DDTHH:MM'
                    'min': (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
                    'max': (datetime.datetime.now() + datetime.timedelta(days=365)).strftime('%Y-%m-%d'),
                    # 'occupied_dates':json.dumps(occupied_dates)
                }
            ),
        }
    
    def clean_description_customer(self):
        return self.clean_capitalize_field('description_customer')



class MechanicForm(CapitalizeField, forms.ModelForm):
    phone_validator = RegexValidator(
        regex=r'^\d{9}$',
        message="El teléfono solo debe contener números y 9 dígitos.",
        code='invalid_phone'
    )
     
    class Meta:
        model = Mechanic
        fields = ['first_name', 'last_name', 'phone', 'specialty', 'image']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'phone': 'Teléfono',
            'specialty': 'Especialidad',
            'image': 'Imágen'
        }
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    def clean_first_name(self):
        return self.clean_capitalize_nameField('first_name')
    
    def clean_last_name(self):
        return self.clean_capitalize_nameField('last_name')
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        self.phone_validator(phone)
        return phone
    # def clean_phone(self):
    #     phone = self.cleaned_data['phone']
    #     # Expresión regular para un número y 9 digitos
    #     if not re.match(r'^\d{9}$', phone):
    #         raise forms.ValidationError("El teléfono solo debe contener números y 9 digitos.")
    #     # Validación para patentes únicas
    #     # if Mechanic.objects.filter(phone=phone).exists():
    #     #     raise forms.ValidationError("Ya existe ese número de teléfono.")
    #     return phone



class JobForm(CapitalizeField, forms.ModelForm):
    class Meta:
        model = Job
        fields = ['description_job']
        labels = {
            'description_job': 'Descripción del trabajo'
        }

    def clean_description_job(self):
        return self.clean_capitalize_field('description_job')


class ServiceForm(forms.ModelForm):
    # Campo para seleccionmar multiples servicios
    service = forms.ModelMultipleChoiceField(
        queryset = Service.objects.all(),
        widget = forms.CheckboxSelectMultiple(),
        required = False,
        label='Servicios'
    )
    class Meta:
        model = Service
        fields = ['service']
        labels = {
            'service': 'Servicios',
        }


class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ['status_service']
        label = {
            'status_service':'Estado servicio'
        }


class VehicleStatusForm(forms.ModelForm):
    status = forms.ModelChoiceField(
            queryset=VehicleStatus.objects.all(),  # Esto representa todos los estados de vehículos disponibles
            widget=forms.Select(),
            label='Estado del vehículo'  
        )
    class Meta:
        model = VehicleStatus
        fields = ['status']
        


class ChecklistForm(forms.ModelForm):
    class Meta:
        model = Checklist
        fields = ['front_lights', 'rear_lights', 'chassis', 'cleaning', 'extinguisher', 'first_aid_kit', 'triangles', 'hydraulic_jack', 'spare_wheel']
        labels = {
            'front_lights': 'Luces delanteras',
            'rear_lights': 'Luces traseras',
            'chassis': 'Chasis',
            'cleaning': 'Limpieza',
            'extinguisher': 'Extinguidor',
            'first_aid_kit': 'Kit primeros auxilios',
            'triangles': 'Triángulos',
            'hydraulic_jack': 'Gata hidráulica',
            'spare_wheel': 'Rueda de repuesto'
        }
