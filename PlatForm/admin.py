from django.contrib import admin
from .models import Patients

# Register your models here.
class PatientsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Patients._meta.get_fields()]

admin.site.register(Patients,PatientsAdmin)
