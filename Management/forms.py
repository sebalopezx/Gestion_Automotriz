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
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError
import json


# Clase global para capitalizar elementos
class CapitalizeField:
    def clean_capitalize_nameField(self, field_name):
        field_value = self.cleaned_data.get(field_name)
        return field_value.title() if field_value else field_value
    
    def clean_capitalize_field(self, field):
        field_value = self.cleaned_data.get(field)
        return field_value.capitalize() if field_value else field_value



# Formularios

class UpdateUserCustomForm(CapitalizeField, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellidos',
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


from django.http import JsonResponse
from pathlib import Path 
import csv
def get_csv_choices(csv_file, key_column, value_column):
    csv_path = Path(__file__).resolve().parent / csv_file
    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        return [(row[key_column], row[value_column]) for row in reader]
    
# def get_models_choices(brand_slug):
#     try:
#         models = []
#         models_file = Path(__file__).resolve().parent / 'data' / 'modelos.csv'

#         with open(models_file, newline='', encoding='utf-8') as csvfile:
#             reader = csv.DictReader(csvfile)
#             for row in reader:
#                 if row['idmake'] == brand_slug:
#                     models.append((row['id'], row['model']))

#         return [('', 'Elegir modelo vehículo')] + models
#     except Exception as e:
#         # Imprime el error en la consola para depuración
#         print(f"Error en get_models_choices: {e}")
#         return JsonResponse({'error': 'Ocurrió un error'}, status=500)
    
# def get_year_choices(model_id):
#     csv_path = Path(__file__).resolve().parent / 'anios.csv'
#     with open(csv_path, 'r') as file:
#         reader = csv.DictReader(file)
#         return [(row['id'], row['year']) for row in reader if row['idmodel'] == str(model_id)]
    


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['brand', 'model', 'patent', 'year']
        # labels = {
        #     'brand': 'Marca',
        #     'model': 'Modelo',
        #     'patent': 'Patente',
        #     'year': 'Año'
        # }

        # NORMALITO
        # widgets = {
        #     'brand': forms.Select(choices=[('','Elegir marca vehículo'), ('ford', 'Ford'), ('toyota', 'Toyota'), ('honda', 'Honda')]),
        #     'model': forms.Select(choices=[('','Elegir modelo vehículo'), ('focus', 'Focus'), ('corolla', 'Corolla'), ('civic', 'Civic')]),
        #     'year': forms.Select(choices=[('','Elegir Año vehículo')] + [(year, year) for year in range(datetime.date.today().year, 1920, -1)])
        # }

        # WEEEEENOOO
        widgets = {
            'brand': forms.Select(choices=[('','Elegir marca vehículo')] + get_csv_choices('marcas.csv', 'slug', 'make')),
            'model': forms.Select(choices=[('','Elegir modelo vehículo')] + get_csv_choices('modelos.csv', 'slug', 'model')),
            'year': forms.Select(choices=[('','Elegir Año vehículo')] + [(year, year) for year in range(datetime.date.today().year, 1920, -1)])
            # 'year': forms.Select(choices=[('','Elegir Año vehículo')] + get_csv_choices('anios.csv', 'year', 'year'))
        }
        # widgets = {
        #     'brand': forms.Select(choices=[('','Elegir marca vehículo')] + get_csv_choices('marcas.csv', 'slug', 'make')),
        #     'model': forms.Select(choices=[('','Elegir modelo vehículo')]),
        #     'year': forms.Select(choices=[('','Elegir Año vehículo')])
        # }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

        # Obtener las opciones de marcas y modelos desde el archivo CSV
        # brand_choices = [('','Elegir marca vehículo')] + self.get_csv_choices('marcas.csv')
        # model_choices = [('','Elegir modelo vehículo')] + self.get_csv_choices('modelos.csv')

        # self.fields['brand'].widget.choices = get_csv_choices('marcas.csv', 'slug', 'make')
        # self.fields['model'].widget.choices = get_csv_choices('modelos.csv', 'slug', 'model')
        # self.fields['year'].widget.choices = get_csv_choices('anios.csv', 'id', 'year')

        # brand_choices = get_csv_choices('marcas.csv', 'slug', 'make')
        # model_choices = get_csv_choices('modelos.csv', 'slug', 'model')
        # year_choices = get_csv_choices('anios.csv', 'id', 'year')
        # print("Brand Choices:", brand_choices)
        # print("Model Choices:", model_choices)
        # print("Year Choices:", year_choices)
        # self.fields['brand'].widget.choices = brand_choices
        # self.fields['model'].widget.choices = model_choices
        # self.fields['year'].widget.choices = year_choices



        # Asignar las opciones a los campos del formulario
        # self.fields['brand'].widget.choices = brand_choices
        # self.fields['model'].widget.choices = model_choices

        # # Otras configuraciones si es necesario (por ejemplo, para el campo de año)
        # self.fields['year'].widget.choices = [('','Elegir Año vehículo')] + [(year, year) for year in range(datetime.date.today().year, 1920, -1)]

       
    # Capturar el valor de patente
    def clean_patent(self):
        patent = self.cleaned_data['patent']
        # Expresiones regulares para identificar solo números y letras
        patent_upper = patent.upper()
        if not re.match("^[A-Za-z0-9]*$", patent):
            raise forms.ValidationError("La patente solo debe contener letras(A-Z) y números(0-9)")
        if len(patent) != 6:
            raise forms.ValidationError("La patente debe tener exactamente 6 caracteres.")
        
        # Validación para patentes únicas en caso de registro
        if not self.instance and Vehicle.objects.filter(patent=patent_upper).exists():
            raise forms.ValidationError("Ya existe un vehículo con esta patente.")
        # Validación para patentes únicas en caso de modificación
        if self.instance and Vehicle.objects.exclude(id=self.instance.id).filter(patent=patent_upper).exists():
            raise forms.ValidationError("Ya existe un vehículo con esta patente.")
        return patent.upper()




class AppointmentForm(CapitalizeField, forms.ModelForm):
    # Inicializacion de datos previos para mostrar en el formulario la data de la base de datos
    def __init__(self, *args, user=None, mechanic=None):
        super().__init__(*args)
        if user is not None:
            self.fields['vehicle'].queryset = Vehicle.objects.filter(customer=user, is_active=True)
        # if mechanic is not None:
        self.fields['mechanic'].queryset = Mechanic.objects.filter(is_active=True)

    class Meta:
        model = Appointment
        fields = ['vehicle','attention','date_register','mechanic','workshop','description_customer']
        labels = {
            'vehicle':'Vehículo',
            'attention':'Atención',
            'date_register':'Fecha de la cita',
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

    class Meta:
        model = Mechanic
        fields = ['first_name', 'last_name', 'phone', 'specialty', 'image', 'is_active']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'phone': 'Teléfono',
            'specialty': 'Especialidad',
            'image': 'Imágen',
            'is_active': '¿Está activo?'
        }
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    def clean_first_name(self):
        return self.clean_capitalize_nameField('first_name')
    
    def clean_last_name(self):
        return self.clean_capitalize_nameField('last_name')
    
    # def clean_phone(self):
    #     phone = self.cleaned_data['phone']
    #     self.phone_validator(phone)
    #     return phone
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        # Expresión regular para validar que sea un número y tenga 9 digitos
        if not re.match(r'^\d{9}$', phone):
            raise forms.ValidationError("El teléfono solo debe contener números y 9 digitos.")
        # Validación para patentes únicas para registro
        if not self.instance and Mechanic.objects.filter(phone=phone).exists():
            raise forms.ValidationError("Ya existe ese número de teléfono.")
        # Validación para patentes únicas para modificacion
        if self.instance and Mechanic.objects.exclude(id=self.instance.id).filter(phone=phone).exists():
            raise forms.ValidationError("Ya existe ese número de teléfono.")
        return phone



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
    # Campo para seleccionar múltiples servicios
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
