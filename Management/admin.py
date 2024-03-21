from django.contrib import admin
from .models import *

# FILTRO PARA FUNCION DE MODELO DE PUNTOS
from django.utils.translation import gettext_lazy as _
from .models import ConfigConstant
# Vehicle, VehicleStatus, Workshop, Appointment, Mechanic, Job, Checklist, Point, Attention, Service, Coupon

try:
    POINTS_VALUE = ConfigConstant.get_points_value()
except:
    pass

# Register your models here.
@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'brand',
        'model',
        'patent',
        'year',
        'is_active',
    )
    def get_list_display(self, request):
        fields = super().get_list_display(request)
        customer_fields = [
            'user_id',
            'customer',
            # 'user_name',
        ]
        return fields + tuple(customer_fields)
    search_fields = ('patent',)
    search_help_text = "Busqueda por patente del vehiculo"
    ordering = ('id',)
    list_filter = (
        'brand','model',
    )
    raw_id_fields = ('customer',)
    list_editable = ('is_active',)
    list_display_links = ('id','brand','model','patent')


    def user_id(self, obj):
        return obj.customer.id
    user_id.short_description = 'Id usuario'



@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'address',
        'num_address',
    )
    search_fields = ('id',)
    search_help_text = "Busqueda por id del taller"
    ordering = ('id',)
    list_display_links = ('id','name','address','num_address',)



@admin.register(Mechanic)
class MechanicAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'phone',
        'specialty',
    )
    search_fields = ('id',)
    search_help_text = "Busqueda por id del mecánico"
    ordering = ('id',)
    list_filter = (
        'specialty',
    )
    list_display_links = ('id','first_name','last_name',)
    list_editable = ('phone', 'specialty')


@admin.register(Attention)
class AttentionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'attention',
    )
    search_fields = ('id',)
    search_help_text = "Busqueda por id de la atención"
    ordering = ('id',)
    list_display_links = ('id','attention',)



@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'date_register',
        'attention',
        'date_created',
        'date_finished',
        'mechanic',
        'inprogress',
        'completed',
        # 'description_customer',
    )
    def get_list_display(self, request):
        fields = super().get_list_display(request)

        vehicle_fields = [
            'vehicle_id_display',
            'vehicle_patent',
            'vehicle_customer_email',
        ]
        return fields + tuple(vehicle_fields) 
    ordering = ['-id']
    search_help_text = 'Busqueda por id de la cita y Filtrado por fecha de cita registrada'
    search_fields = ('pk',)
    date_hierarchy = 'date_register'
    list_filter = (
        'inprogress', 
        'completed', 
        'date_register',
        'date_created',
        'date_finished', 
        'mechanic',
    )
    list_display_links = ('id', 'date_register', )
    raw_id_fields = ('vehicle',)
    list_editable = ('inprogress', 'completed',)

    def vehicle_id_display(self, obj):
        return obj.vehicle.id
    vehicle_id_display.short_description = 'Vehículo id'
    def vehicle_patent(self, obj):
        return obj.vehicle.patent if obj.vehicle else None
    vehicle_patent.short_description = 'Patente'
    def vehicle_customer_email(self, obj):
        return obj.vehicle.customer.email if obj.vehicle else None
    vehicle_customer_email.short_description = 'Email de usuario'



@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'price',
        'earn_points',
    )
    search_fields = ('id',)
    search_help_text = "Busqueda por id del servicio"
    ordering = ('id',)
    list_filter = (
        'price',
        'earn_points',
    )


@admin.register(VehicleStatus)
class VehicleStatusAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'status',
    )
    search_fields = ('id',)
    search_help_text = "Busqueda por id del estado"
    ordering = ('id',)
    list_display_links = ('id',)
    list_editable = ('status',)



@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'appointment_id_display',
        'appointment_patent',
        'appointment_name',
        # 'appointment_last_name',
        'status',
        # 'status_id_display',
        # 'status_display',
    )
    # def get_list_display(self, request):
    #     fields = super().get_list_display(request)

    #     appointment_fields = [
    #         # 'appointment_id_display',
    #         # 'appointment_patent',
    #         # 'appointment_first_name',
    #         # # 'appointment_last_name',
    #         # 'status',
    #         # 'status_id_display',
    #         # 'status_display',
    #     ]
    #     return fields + tuple(appointment_fields) 

    search_fields = ('appointment__id',)
    search_help_text = "Busqueda por id de la cita"
    ordering = ('-id',)
    list_filter = (
        'status',
    )
    raw_id_fields = ('appointment',)
    list_editable = ('status',)

    def appointment_object(self, obj):
        return obj.appointment
    def appointment_id_display(self, obj):
        return obj.appointment.id
    appointment_id_display.short_description = 'Cita id'
    def appointment_patent(self, obj):
        return obj.appointment.vehicle.patent if obj.appointment.vehicle.patent else None
    appointment_patent.short_description = 'Patente vehículo'
    def appointment_name(self, obj):
        return f"{obj.appointment.vehicle.customer.first_name} {obj.appointment.vehicle.customer.last_name}" if obj.appointment.vehicle.customer.first_name else None
    appointment_name.short_description = 'Cliente'
    # def appointment_last_name(self, obj):
    #     return obj.appointment.vehicle.customer.last_name if obj.appointment.vehicle.customer.last_name else None
    # appointment_last_name.short_description = 'Apellido'
    # def status_id_display(self, obj):
    #     return obj.status.id if obj.status else None
    # status_id_display.short_description = 'Estado id'
    # def status_display(self, obj):
    #     return obj.status.status if obj.status.status else None
    # status_display.short_description = 'Estado'


    
    
    # list_display_links = ('id',)


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'appointment_id_display',
        'job_id_display',
        'service',
        'status_service',
    )
    search_fields = ('job__appointment__id',)
    search_help_text = "Busqueda por id de la cita"
    ordering = ('-id',)
    raw_id_fields = ('job',)
    list_filter = (
        'status_service',
        'service__name',
    )
    list_editable = ('service','status_service',)

    def appointment_object(self, obj):
        return obj.job.appointment
    def appointment_id_display(self, obj):
        return obj.job.appointment.id
    appointment_id_display.short_description = 'Id Cita'
    def job_id_display(self, obj):
        return obj.job.id
    job_id_display.short_description = 'Id Trabajo'




class PointsFilter(admin.SimpleListFilter):
    title = _('Points Filter')
    parameter_name = 'points'

    def lookups(self, request, model_admin):
        return (
            ('lt_point', _(f'Menor que {POINTS_VALUE}')),
            ('gte_point', _(f'Mayor o igual a {POINTS_VALUE}')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'lt_point':
            return queryset.filter(points__lt=10)
        elif self.value() == 'gte_point':
            return queryset.filter(points__gte=10)
        
@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer',
        'user_display',
        'points',
    )
    search_fields = ('id',)
    search_help_text = "Busqueda por id"
    ordering = ('id',)
    raw_id_fields = ('customer',)
    
    list_filter = (
        PointsFilter,
    )
    list_editable = ()

    def user_object(self, obj):
        return obj.customer
    def user_display(self, obj):
        return f"{obj.customer.first_name} {obj.customer.last_name}"
    user_display.short_description = 'Nombre cliente'



@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer',
        'user_display',
        'coupon',
        'valid',
    )
    search_fields = ('id', 'customer__username', 'customer__first_name', 'customer__last_name', 'coupon')
    search_help_text = "Busqueda por id, nombre de usuario, nombre y apellido del cliente, además del cupón."
    ordering = ('id',)
    raw_id_fields = ('customer',)
    
    list_filter = (
        'valid',
    )
    list_editable = ('valid',)

    def user_object(self, obj):
        return obj.customer
    def user_display(self, obj):
        return f"{obj.customer.first_name} {obj.customer.last_name}"
    user_display.short_description = 'Nombre cliente'


@admin.register(Checklist)
class ChecklistAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'km',
        'gasoline_tank', 
        'job_id_display', 
        'front_lights', 
        'rear_lights', 
        'chassis', 
        'cleaning',
        'extinguisher', 
        'first_aid_kit', 
        'triangles', 
        'hydraulic_jack', 
        'spare_wheel',
    )
    search_fields = ('job__id',)
    search_help_text = "Busqueda por id del trabajo."
    ordering = ('id',)
    raw_id_fields = ('job',)
    
    list_editable = ('km','gasoline_tank','front_lights', 'rear_lights', 'chassis', 'cleaning',
                    'extinguisher', 'first_aid_kit', 'triangles', 'hydraulic_jack', 'spare_wheel',)

    def job_object(self, obj):
        return obj.job
    def job_id_display(self, obj):
        return f"{obj.job.id}"
    job_id_display.short_description = 'Id trabajo'




# INDEX
@admin.register(TitleHeader)
class TitleHeaderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title_header',
    )
    search_fields = ('id','title_header',)
    search_help_text = "Busqueda por id y título."
    ordering = ('id',)
    list_editable = ('title_header',)

    # def save_model(self, request, obj, form, change):
    #     # Verifica si la imagen ya existe en la carpeta media
    #     existing_images = Description.objects.filter(image_description=obj.image_description.name)
    #     if existing_images.exists():
    #         obj.image_description = existing_images.first().image_description

    #     super().save_model(request, obj, form, change)


@admin.register(Description)
class DescriptionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
    )
    search_fields = ('id','title',)
    search_help_text = "Busqueda por id y título."
    ordering = ('id',)
    list_display_links = ('id', 'title',)


@admin.register(ConfigConstant)
class ConfigConstantAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'value',
    )
    search_fields = ('id','name',)
    search_help_text = "Busqueda por id y nombre de constante."
    ordering = ('id',)
    list_editable = ('value',)
    list_display_links = ('id', 'name',)
