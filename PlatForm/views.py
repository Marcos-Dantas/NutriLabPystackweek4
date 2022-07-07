from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from PlatForm.models import Patients
from .utils import post_data_valid
from django.shortcuts import redirect
from django.contrib.messages import constants
from django.contrib import messages

@login_required(login_url='/auth/login/')
def patients(request): 
    if request.method == "POST":
        username = request.POST.get('name')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        if not post_data_valid(request, username, gender, age, email, phone):
            return redirect('/patients/') 
        
        try:
            patient = Patients(name=username,
                                gender=gender,
                                age=age,
                                email=email,
                                phone=phone,
                                nutri=request.user)
            patient.save()
            messages.add_message(request, constants.SUCCESS, 'Paciente cadastrado com sucesso')
            return redirect('/patients/')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
        
    else:
        patients = Patients.objects.filter(nutri=request.user)
       
        return render(request, 'patients.html', {'patients': patients})   