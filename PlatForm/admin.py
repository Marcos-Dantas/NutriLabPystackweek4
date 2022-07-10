from django.contrib import admin
from .models import Patients, PatientData, Meal, Option

# Register your models here.
class PatientsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Patients._meta.get_fields()]

class PatientDataAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PatientData._meta.get_fields()]

admin.site.register(Patients,PatientsAdmin)
admin.site.register(PatientData,PatientDataAdmin)
admin.site.register(Meal)
admin.site.register(Option)
