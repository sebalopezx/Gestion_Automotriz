import os
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
# Creacion de usuario mediante django
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User, Group
# Creacion y Actualización de Cookies
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import update_session_auth_hash
# Manejo de error de integridad
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
# Decoradores para login
from django.contrib.auth.decorators import login_required
from .templatetags.decorators import customer_required, recepcionist_required

# MODELOS 
from .models import Mechanic, Vehicle, Appointment, Job, Checklist, Point, Service, Work, VehicleStatus, Coupon
# FORMULARIO
from .forms import CustomUserCreationForm, UpdateUserCustomForm, VehicleForm, AppointmentForm, MechanicForm, JobForm, ChecklistForm, ServiceForm, WorkForm, VehicleStatusForm
from django.forms import ValidationError, formset_factory, modelformset_factory

# CONSTANTES
from .constants import POINTS
# 
from django.utils import timezone
from django.db.models import Q
# CACHE
from django.core.cache import cache




# Create your views here.

def index(request):
    user_type_value = user_type(request.user)
    base_template = template_base(user_type_value)
    return render(request, 'index.html',{
        'base_template':base_template,
        'POINTS':POINTS
    })

# VIEWS LOGIN 

def signup(request):
    if request.method == 'POST':
        form_register = CustomUserCreationForm(request.POST)
        if form_register.is_valid():
            user = form_register.save()
            messages.success(request, 'Usuario registrado con éxito')
            login(request, user)

            # Asigna el usuario al grupo "Clientes"
            customer_group = Group.objects.get(name='Customer')
            customer_group.user_set.add(user)

            # Inicializar sistema de puntos
            points = Point.objects.create(customer=user)
            points.save()
            return redirect('index') 
        else:
            messages.error(request, 'Error al registrar usuario')
    else:
        form_register = CustomUserCreationForm()
    
    return render(request, 'signup.html', {
        'form_register': form_register
        })


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form_login':AuthenticationForm()
        })
    else:
        user = authenticate(request, 
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is None:
            return render(request,'signin.html',{
                'form_login':AuthenticationForm(),
                'error':'Usuario o Contraseña inválidos.'
            })
        else:
            # Crea la cookie con fecha de expiracion
            login(request, user)
            if request.user.groups.filter(name='Customer').exists():
                return redirect('index')
            elif request.user.groups.filter(name='Recepcionist').exists():
                return redirect('list_jobs_diary')



@login_required
def signout(request):
    logout(request)
    print(cache)
    cache.clear()
    # session.clear()
    request.session.flush()
    return redirect('index')

    # # Agregar encabezados para evitar el almacenamiento en caché
    # response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    # response['Pragma'] = 'no-cache'
    # response['Expires'] = '0'

    # return response


# VIEWS  PARA AMBOS

# Verifica el usuario segun su grupo 
def user_type(user):
    is_customer = user.groups.filter(name='Customer').exists()
    is_recepcionist = user.groups.filter(name='Recepcionist').exists()
    if is_customer:
        return "Customer"
    elif is_recepcionist:
        return "Recepcionist"
    else:
        return "AnonymousUser"

# Verifica si el path del base pertenece a cliente o recepcionista
def template_base(user_type):
    if user_type == "Customer":
        base_template = 'base_customer.html'
    elif user_type == "Recepcionist":
        base_template = 'base_recepcionist.html'
    else:
        base_template = "base.html"
    return base_template


@login_required
def list_user_data(request):
    # Mostramos la data del usuario y sus puntos
    user = User.objects.filter(username=request.user)
    points = None
    coupons = None
    user_points = User.objects.filter(username=request.user).first() 
    # if Point.objects.filter(customer=user).exists():
    if user_points:
        try:
            points = Point.objects.get(customer=request.user)
            coupons = Coupon.objects.filter(customer=request.user)
        except ObjectDoesNotExist:
            pass
    error =  'No tiene datos'
    user_type_value = user_type(request.user)
    base_template = template_base(user_type_value)
    # is_customer = user.groups.filter(name='Customer').exists()
    return render(request, 'user_data.html',{
        'list_data':user,
        'points':points,
        'POINTS':POINTS,
        'coupons':coupons,
        'error':error,
        'base_template':base_template,
        'user_type_value':user_type_value
        # 'is_customer':is_customer
    })





@login_required
def detail_user_data(request, id):
    # Identificamos al usuario por el id
    user = get_object_or_404(User, pk=id)
    user_type_value = user_type(request.user)
    base_template = template_base(user_type_value)
    if request.method == 'POST':
        # Formulario customizado para data principal y username solo de lectura
        form_update = UpdateUserCustomForm(request.POST, instance=user)
        form_update.fields['username'].widget.attrs['readonly'] = True
        try:
            if form_update.is_valid():
                form_update.save()
                messages.success(request, 'Datos actualizados exitosamente.') 
                return redirect('detail_user_data', id=id)
            else:
                messages.error(request, 'Error al actualizar datos.')
        except IntegrityError:
            messages.error(request, 'Error de integridad.')

    else:
        form_update = UpdateUserCustomForm(instance=user)
        # Deshabilitar edición del campo username
        form_update.fields['username'].widget.attrs['readonly'] = True
        
    return render(request, 'detail_user_data.html', {
        'user': user,
        'form_update': form_update,
        'base_template':base_template
    })


@login_required
def update_password(request, id):
    # Identificamos al usuario autenticado 
    user = request.user
    user_type_value = user_type(request.user)
    base_template = template_base(user_type_value)
    if request.method == 'POST':
        # Formulario customizado password
        form_update = PasswordChangeForm(user, request.POST)
        # form_update.fields['username'].widget.attrs['diabled'] = True
        try:
            if form_update.is_valid():
                form_update.save()
                # Actualización de cookie del usuario
                update_session_auth_hash(request, user)
                messages.success(request, 'Contraseña actualizada exitosamente.') 
                return redirect('update_password', id=id)
            else:
                messages.error(request, 'Error al actualizar contraseña.')
        except IntegrityError:
            messages.error(request, 'Error de integridad.')

    else:
        form_update = PasswordChangeForm(user)
        # Deshabilitar edición del campo username
        # form_update.fields['username'].widget.attrs['disabled'] = True
        
    return render(request, 'update_password.html', {
        'user': user,
        'form_update': form_update,
        'base_template':base_template
    })




# VIEWS CUSTOMERS

@login_required
@customer_required
def register_vehicle(request):
    if request.method == 'POST':
        form_vehicle = VehicleForm(request.POST)
        try:
            if form_vehicle.is_valid():
                vehicle = form_vehicle.save(commit=False)
                vehicle.customer = request.user
                vehicle.save()
                messages.success(request, 'Vehículo creado exitosamente.')
                return redirect('vehicle')
            else:
                messages.error(request, 'Error al registrar vehículo')
        except ValidationError as e:
            messages.error(request, 'Error de ejecución')
    else:
        form_vehicle = VehicleForm()

    
    return render(request, 'register_vehicle.html', {
        'form': form_vehicle
    })



@login_required
@customer_required
def register_date(request):
    user = request.user  # Usuario Autenticado
    # Obtener los vehículos del usuario logeado
    user_vehicles = Vehicle.objects.filter(customer=user)

    if request.method == 'POST':
        form_appointment = AppointmentForm(request.POST, user=user)
        if form_appointment.is_valid():
            # Obtenemos los datos del formulario
            date_register = form_appointment.cleaned_data['date_register']
            attention = form_appointment.cleaned_data['attention']
            mechanic = form_appointment.cleaned_data['mechanic']

            # Verifica si ya existe una cita en ese horario y fecha
            existing_appointment = Appointment.objects.filter(
                attention=attention, date_register=date_register, mechanic=mechanic
            ).exists()

            if existing_appointment:
                # Error : ya existe un registro en esa fecha y hora
                form_appointment.add_error(
                    'attention',
                    f'El mecánico {mechanic}, ya tiene cita programada para fecha {date_register} {attention}'
                )
            else:
                form_appointment.save()
                # Creamos el trabajo y checklist con estado en espera
                # Buscamos el id de la cita recien creada
                latest_appointment = Appointment.objects.latest('id').id
                id_appointment = Appointment.objects.get(id=latest_appointment)
                status = VehicleStatus.objects.get(pk=1)
                job = Job.objects.create(appointment=id_appointment, status=status)
                checklist = Checklist.objects.create(job=job)

                messages.success(request, 'Cita confirmada') 
                return redirect('appointment')
        else:
            # form_appointment = AppointmentForm()
            messages.error(request, 'Error al crear cita')

    else:
        # Filtro de vehiculos por usuario autenticado
        # vehiculos_usuario = Vehiculo.objects.filter(cliente=user)
        # form = CitaForm(vehiculo=vehiculos_usuario) 
        form_appointment = AppointmentForm(user=user)
        existing_appointment = False
        if not user_vehicles:
            # form_appointment.fields['vehicle'].widget.attrs['readonly'] = True
            for field in form_appointment.fields.values():
                field.widget.attrs['disabled'] = True
   
    return render(request, 'register_date.html', {
        'form': form_appointment,
        'user_vehicles': user_vehicles,
        'existing_appointment': existing_appointment
    })



@login_required
@customer_required
def create_coupon_points(request):
    points = get_object_or_404(Point, customer=request.user)
    try:
        points.points -= POINTS
        points.save()
        new_coupon = Coupon(customer=request.user, coupon=Coupon.generate_coupon_code())
        new_coupon.save()
        messages.success(request, "Cupón creado exitosamente.")
        return redirect('user_data')
    except:
        messages.error(request, "No se ha podido crear el cupón.")


@login_required
@customer_required
def delete_coupon(request, id):
    coupon = get_object_or_404(Coupon, id=id, customer=request.user)
    if request.method == 'POST':
        coupon.delete()
        messages.success(request, "Cupón eliminado exitosamente.")
        return redirect('user_data')
    

@login_required
@customer_required
def list_vehicles(request):
    # Además de obtener los objetos vehiculos segun el id del usuario logeado
    # Debe traer todas las citas relacionadas a ese idvehiculo, ademas dentro de cada cita
    # agregar cada trabajo relacionado
    vehicles = Vehicle.objects.filter(customer=request.user).prefetch_related('appointment_set__job_set')
    error = 'No tiene vehículos'
    return render(request, 'vehicle.html', {
        'list_vehicle': vehicles,
        'error': error
    })

@login_required
@customer_required
def delete_vehicle(request, id):
    vehicle = get_object_or_404(Vehicle, pk=id, customer=request.user)
    if request.method == 'POST':
        vehicle.delete()
        messages.success(request, "Vehículo eliminado con éxito.")
        return redirect('vehicle')


@login_required
def state_vehicle(request, id):
    user_type_value = user_type(request.user)
    base_template = template_base(user_type_value)
    earn_points = 0
    total_price = 0
    estimated_total_price = 0
    # vehicles = Vehicle.objects.filter(pk=id, customer=request.user)
    # state_vehicle = Job.objects.filter(job_appointment_vehicle_id=id)
    # state_vehicle = get_object_or_404(Appointment, pk=id, vehicle__customer=request.user)
    state_vehicle = get_object_or_404(Job, appointment_id=id)
    services = state_vehicle.work_set.all()
    
    appointment = get_object_or_404(Appointment, pk=id)
    user = appointment.vehicle.customer
    # points = Point.objects.get(customer=request.user)
    points = Point.objects.get(customer=user)
    # for s in services:
    #     if s.
    #     earn_points += s.service.earn_points
    #     print(earn_points)
    for service in services:
        if service.status_service == True:
            total_price += service.service.price
            earn_points += service.service.earn_points
        if service.status_service == False or service.status_service == True:
            estimated_total_price = service.service.price

    error =  'No tiene vehículos'
    return render(request, 'state_vehicle.html',{
        # 'list_vehicle':vehicles,
        'base_template':base_template,
        'state_vehicle':state_vehicle,
        'services':services,
        'total_price':total_price,
        'estimated_total_price':estimated_total_price,
        'points':points,
        'earn_points':earn_points,
        'POINTS':POINTS,
        'error':error
    })


@login_required
@customer_required
def list_appointment(request):
    # date = Vehicle.objects.filter(customer=request.user)
    date = Appointment.objects.filter(vehicle__customer=request.user)
    # date = Appointment.objects.all()
    error =  'No tiene citas'
    return render(request, 'appointment.html',{
        'list_dates':date,
        'error':error
    })



@login_required
@customer_required
def cancel_appointment(request, id):
    appointment = get_object_or_404(Appointment, pk=id, vehicle__customer=request.user)
    if request.method == 'POST': 
        # appointment.delete()
        status = VehicleStatus.objects.get(pk=8)
        job = get_object_or_404(Job, appointment=appointment)
        job.status = status
        # job.description_job = "Cancelado"

        appointment.date_finished = timezone.now()

        job.save()
        appointment.save()

        messages.success(request, "Cita cancelada con éxito.")
        return redirect('appointment')




# VIEWS WORK USERS

@recepcionist_required
def register_recepcionist(request):
    if request.method == 'POST':
        form_register = CustomUserCreationForm(request.POST)
        if form_register.is_valid():
            user = form_register.save()
            messages.success(request, 'Usuario registrado con éxito')
            #login(request, user)

            # Asigna el usuario al grupo "Clientes"
            customer_group = Group.objects.get(name='Recepcionist')
            customer_group.user_set.add(user)

            # Inicializar sistema de puntos
            #points = Point.objects.create(customer=user)
            #points.save()
            return redirect('register_recepcionist') 
        else:
            messages.error(request, 'Error al registrar usuario')
    else:
        form_register = CustomUserCreationForm()
    
    return render(request, 'register_recepcionist.html', {
        'form_register': form_register
        })




@login_required
@recepcionist_required
def list_mechanic(request):
    mechanic = Mechanic.objects.all()
    error =  'No existen Mecánicos'   
    return render(request, 'list_mechanic.html', {
        'list_mechanic':mechanic,
        'error':error
    })

@login_required
@recepcionist_required
def register_mechanic(request):
    error = ""
    if request.method == 'POST':
        form_mechanic = MechanicForm(request.POST, request.FILES)
        try:
            if form_mechanic.is_valid():
                form_mechanic.save()
                messages.success(request, 'Mecánico agregado exitosamente.')
                return redirect('list_mechanic')
            else:
                error = "El teléfono solo debe contener números y 9 digitos."
        except:
             messages.error(request, 'Error al registrar mecánico.')
    else:
        form_mechanic = MechanicForm()
        
    return render(request, 'register_mechanic.html', {
        'form_mechanic': form_mechanic,
        'error': error
    })


@login_required
@recepcionist_required
def update_mechanic(request, id):
    if request.method == 'POST':
        mechanic = get_object_or_404(Mechanic, pk=id)
        form_update = MechanicForm(request.POST, request.FILES, instance=mechanic)
        try:   
            if form_update.is_valid():
                form_update.save()
                messages.success(request, 'Mecánico actualizado exitosamente.')
                return redirect('list_mechanic')
        except:
            messages.error(request, "Error al actualizar mecánico.")
    else:
        mechanic = get_object_or_404(Mechanic, pk=id)
        form_update = MechanicForm(instance=mechanic)

    return render(request, 'update_mechanic.html',{
            'data_mechanic': mechanic,
            'form_update': form_update,
        })


@login_required
@recepcionist_required
def delete_mechanic(request, id):
    mechanic = get_object_or_404(Mechanic, pk=id)
    if request.method == 'POST':
        try:
            image_path = mechanic.image.path
            mechanic.delete()
            if os.path.exists(image_path) and not image_path.endswith('foto_personal.jpg'):
                os.remove(image_path)
            messages.success(request, "Mecánico eliminado exitosamente.")
            return redirect('list_mechanic')
        except:
            messages.error(request, "Error al eliminar mecánico.")




# JOBS

@login_required
@recepcionist_required
def list_jobs_pending(request):
    # appointments = Appointment.objects.all()
    appointments = Appointment.objects.filter(
        inprogress=False,  
        completed=False, 
        date_finished__isnull=True).order_by('date_register', 'attention')
    form_job = JobForm(request.POST)
    # form_services = ServiceForm(request.POST)
    error =  'No existen citas para trabajos'
     
    return render(request, 'list_jobs_pending.html', {
        'list_appointments':appointments,
        'form_job':form_job,
        # 'form_services':form_services,
        'error':error
    })


@login_required
@recepcionist_required
def list_jobs_diary(request):
    current_date = timezone.now().date()
    appointments_diary = Appointment.objects.filter(
        inprogress=True, 
        completed=False, 
        date_register=current_date)
    jobs_diary = Job.objects.filter(appointment__in=appointments_diary).order_by('appointment__attention')
    error_diary =  'No existen trabajos el día de hoy'

    return render(request, 'list_jobs_diary.html', {
        'list_jobs_diary':jobs_diary,
        'error_diary':error_diary,
        'current_date':current_date
    })

@login_required
@recepcionist_required
def list_jobs_inprogress(request):
    # appointments = Appointment.objects.all()
    # jobs = Job.objects.all()
    current_date = timezone.now().date()

    # appointments = Appointment.objects.filter(inprogress=True, completed=False, ~Q(date_register=current_date), date_finished__isnull=True)
    appointments = Appointment.objects.filter(
        Q(inprogress=True, completed=False) 
        & ~Q(date_register=current_date) 
        & Q(date_finished__isnull=True))
    jobs = Job.objects.filter(appointment__in=appointments).order_by('appointment__date_register')
    error =  'No existen trabajos en progreso'

    # appointments_diary = Appointment.objects.filter(
    #     inprogress=True, 
    #     completed=False, 
    #     date_register=current_date)
    # jobs_diary = Job.objects.filter(appointment__in=appointments_diary).order_by('appointment__attention')
    # error_diary =  'No existen trabajos el día de hoy'

    return render(request, 'list_jobs_inprogress.html', {
        # 'list_appointments':appointments,
        'list_jobs':jobs,
        'error':error,
        # 'list_jobs_diary':jobs_diary,
        # 'error_diary':error_diary,
        # 'current_date':current_date
    })

@login_required
@recepcionist_required
def list_jobs_completed(request):
    # appointments = Appointment.objects.all()
    # jobs = Job.objects.all()
    # appointments = Appointment.objects.filter(inprogress=True, completed=True)
    appointments = Appointment.objects.filter(date_finished__isnull=False)
    jobs = Job.objects.filter(appointment__in=appointments)
    error =  'No existen trabajos finalizados'
     
    return render(request, 'list_jobs_completed.html', {
        # 'list_appointments':appointments,
        'list_jobs':jobs,
        'error':error
    })




@login_required
@recepcionist_required
def generate_ot(request, id):
    appointment = get_object_or_404(Appointment, pk=id)
    job = Job.objects.get(appointment=appointment)
    status = VehicleStatus.objects.get(pk=2)
    if request.method == 'POST':
        
        # Se genera una descripcion mas técnica del trabajo
        description = request.POST.get('description_job')
        # Al generar OT se genera el trabajo y checklist de la cita
        # job = Job.objects.create(appointment=appointment, description_job=description, status=status)
        # checklist = Checklist.objects.create(job=job)
        # form_services = ServiceForm(request.POST, instance=job)
        job.status = status
        job.description_job = description.capitalize()
        job.save()
        # checklist.save()
        # if form_services.is_valid():

        #     # Procesar los servicios seleccionados y asignarlos al trabajo
        #     selected_service_ids = request.POST.getlist('service')
        #     services_to_add = Service.objects.filter(id__in=selected_service_ids)
        #     for service in services_to_add:
        #         Work.objects.create(job=job, service=service)

        # Cambio de estado de la cita
        appointment.inprogress = True
        appointment.save()

        messages.success(request, "Trabajo creado exitosamente.")
        return redirect('list_jobs_pending')
    else:
        messages.error(request, "Error al crear trabajo.")
        return redirect('list_jobs_pending')




@login_required
@recepcionist_required
def job_checklist (request, id):

    job = get_object_or_404(Job, pk=id)
    works = Work.objects.filter(job_id=job)

    if request.method == 'POST':
        # Servicios
        form_work = WorkForm(request.POST, instance=job)
        form_update = ChecklistForm(request.POST, instance=job.checklist)  # , instance=job.checklist        
        form_status = VehicleStatusForm(request.POST, instance=job)

        # for service in works:
        #     checkbox_name = f"service_{service.id}"
        #     status = checkbox_name in request.POST
        #     print(f'Service: {service.id}, Checkbox Name: {checkbox_name}, State: {status}')
        #     service.status_service = status
        #     service.save()
        form_update.save()
        try:   
            if form_update.is_valid():
                form_update.save()

            if form_work.is_valid():
                for service in works:
                    checkbox_name = f"service_{service.id}"
                    status = checkbox_name in request.POST
                    service.status_service = status
                    service.save()

            if form_status.is_valid():
                form_status.save()

            messages.success(request, "Trabajo actualizado exitosamente.")
            return redirect('checklist', id=id)
        except ValidationError:
            messages.error(request, "Error al cargar")
    else:
        # Servicios
        form_work = WorkForm(instance=job)
        form_update = ChecklistForm(instance=job.checklist)
        form_status = VehicleStatusForm(instance=job)

    # Obtén los servicios relacionados al trabajo actual
    list_services = Work.objects.filter(job=job)
    checklist = job.checklist
    return render(request, 'checklist.html', {
        'form_work':form_work,
        'form_checklist':form_update,
        'checklist':checklist,
        'form_status':form_status,
        'list_services': list_services
    })



@login_required
@recepcionist_required
def delete_service(request, id_service, id):
    service = get_object_or_404(Work, pk=id_service)
    if request.method == 'POST':
        service.delete()
        messages.success(request, "Servicio eliminado con éxito.")
        return redirect('checklist', id=id)



@login_required
@recepcionist_required
def update_job(request, id):

    if request.method == 'POST':
        job = get_object_or_404(Job, pk=id)
        description = job.description_job.capitalize() if job.description_job else ''
        services = Work.objects.filter(job=job) 
        try:   
            form_job = JobForm(request.POST, initial={'description_job':description}) 
            form_service = ServiceForm(request.POST)

            if form_job.is_valid():
                # Actualizar la descripción
                job.description_job = request.POST['description_job'].capitalize()
                job.save()
                
            if form_service.is_valid():
                # Agrega los nuevos servicios seleccionados
                new_selected_service_ids = request.POST.getlist('service')
                services_to_add = Service.objects.filter(id__in=new_selected_service_ids)
                for service in services_to_add:
                    Work.objects.create(job=job, service=service)
                
            messages.success(request, "Trabajo actualizado exitosamente.")
            return redirect('update_job', id=id)
        except ValidationError:
            messages.error(request, "Error al cargar")
    else:
        job = get_object_or_404(Job, pk=id)
        description = job.description_job.capitalize() if job.description_job else ''
        form_job = JobForm(initial={'description_job':description}) 
        form_service = ServiceForm()

    return render(request, 'update_job.html', {
        'form_job':form_job,
        'form_service':form_service,
        'job':job
    })




@login_required
@recepcionist_required
def delete_job(request, id, job_type):
    job = get_object_or_404(Job, appointment_id=id)
    status = VehicleStatus.objects.get(pk=8)
    description = request.POST.get('description_job_cancel')
    if request.method == 'POST':
        # return redirect('list_jobs_pending')
        if job_type == 'pending':
            job.description_job = description
            job.status = status
            job.appointment.date_finished = timezone.now()
            job.save()
            job.appointment.save()
            messages.success(request, "Cita cancelada con éxito.")
            return redirect('list_jobs_pending')
        elif job_type == 'inprogress':
            job.status = status
            job.appointment.date_finished = timezone.now()
            job.save()
            job.appointment.save()
            messages.success(request, "Cita cancelada con éxito.")
            return redirect('list_jobs_inprogress')
        elif job_type == 'completed':
            job.delete()
            job.appointment.delete()
            messages.success(request, "Cita eliminada con éxito.")
            return redirect('list_jobs_completed')
      

@login_required
@recepcionist_required
def completed_job(request, id):
    job = get_object_or_404(Job, pk=id)
    user = job.appointment.vehicle.customer

    if request.method == 'POST':
        # Cambio de estado de la cita
        # job.appointment.description_customer = job.description_job
        
        # Cambios de estado del trabajo
        job.appointment.completed = True
        job.appointment.date_finished = timezone.now()
        job.appointment.save()

        services = job.work_set.all()
        total_points = Point.objects.get(customer=user)
        for point in services:
            point_earned = point.service.earn_points
            total_points.points += point_earned
        total_points.save()

        messages.success(request, "Trabajo finalizado exitosamente.")
        return redirect('list_jobs_inprogress')

    return messages.error(request, "Error al finalizar trabajo.")





@login_required
@recepcionist_required
def search_patent(request):
    data = request.GET.get('patent').upper()
    patent = None
    date = None
    error = "Patente o cita no existe."

    if data is not None:
        vehicle = Vehicle.objects.filter(patent=str(data))
        if vehicle.exists():
            appointments = Appointment.objects.filter(vehicle_id=vehicle.first())

            # search = Appointment.objects.filter(vehicle_id=vehicle.first())
            patent = Job.objects.filter(appointment__in=appointments)
            error = "Patente no tiene citas."
            search = True
        else:
            try:
                appointment = Appointment.objects.filter(pk=data)
                job = Job.objects.filter(appointment__in=appointment)
                date = job
                search = True
            except (Appointment.DoesNotExist, ValueError):
                search = False


    return render(request, 'search_patent.html',{
        'data' : data,
        'search': search,
        'patent':patent,
        'date': date,
        'error':error
    })