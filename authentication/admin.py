from django.contrib import admin
from .models import activation
# Register your models here.


class ActivationAdmin(admin.ModelAdmin):
    list_display = ('token', 'user', 'active')

admin.site.register(activation,ActivationAdmin)