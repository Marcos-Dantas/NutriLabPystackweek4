from django.contrib import admin
from .models import Patients, PatientData, Meal, Option

admin.site.register(Patients)
admin.site.register(PatientData)
admin.site.register(Meal)
admin.site.register(Option)
