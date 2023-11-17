from django.contrib import admin
from .models import Vehicle, VehicleStatus, Workshop, Appointment, Mechanic, Job, Checklist, Point, Attention, Service, Coupon

# Register your models here.
admin.site.register(Vehicle)
admin.site.register(Workshop)
admin.site.register(Appointment)
admin.site.register(Mechanic)
admin.site.register(Job)
admin.site.register(Checklist)
admin.site.register(Point)
admin.site.register(Attention)
admin.site.register(Service)
admin.site.register(VehicleStatus)
admin.site.register(Coupon)