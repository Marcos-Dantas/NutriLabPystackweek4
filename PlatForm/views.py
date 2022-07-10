import datetime
from ssl import Options
from tkinter import HORIZONTAL
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from .utils import post_data_valid, post_patient_data_valid, post_meal_data_valid
from django.shortcuts import redirect
from django.contrib.messages import constants
from django.contrib import messages
from .models import Patients, PatientData, Meal, Option
from django.views.decorators.csrf import csrf_exempt

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


@login_required(login_url='/auth/login/')
def patient_info_list(request):
    patients = Patients.objects.filter(nutri=request.user)
  
    return render(request, 'patient_info_list.html', {'patients': patients})

@login_required(login_url='/auth/login/')
def patient_information(request, id):
    patient = get_object_or_404(Patients, id=id)
    if not patient.nutri == request.user:
        messages.add_message(request, constants.ERROR, 'Esse paciente não é seu')
        return redirect('/patient-info-list/')
    
    if request.method == "POST":
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        grease = request.POST.get('grease')
        muscle = request.POST.get('muscle')
        hdl = request.POST.get('hdl')
        ldl = request.POST.get('ldl')
        colesterol_total = request.POST.get('ctotal')
        triglicerídios = request.POST.get('triglicerídios')

        if not post_patient_data_valid(request, weight, height, grease, muscle, hdl, ldl, colesterol_total, triglicerídios):
            return redirect(f'/patient/{id}')


        p = PatientData(patient=patient,
                                data=datetime.datetime.now(),
                                weight=weight,
                                height=height,
                                percentage_grease=grease,
                                percentage_muscle=muscle,
                                colesterol_hdl=hdl,
                                colesterol_ldl=ldl,
                                colesterol_total=colesterol_total,
                                trigliceridios=triglicerídios)
        p.save()
        messages.add_message(request, constants.SUCCESS, 'Dados cadastrado com sucesso')
        return redirect('/patient-info-list/')
    else:
        patient_data = PatientData.objects.filter(patient=patient)
        return render(request, 'patient_information.html', {'patient': patient, 'patient_data': patient_data})


@login_required(login_url='/auth/login/')
@csrf_exempt
def weight_graph(request, id):
    patient = Patients.objects.get(id=id)
    datas = PatientData.objects.filter(patient=patient).order_by("data")
    weights = [data.weight for data in datas]
    labels = list(range(len(weights)))
    data = {'weight': weights,
            'labels': labels}
    
    return JsonResponse(data)

@login_required(login_url='/auth/login/')
def food_plan_list(request):
    patients = Patients.objects.filter(nutri=request.user)
    return render(request, 'food_plan_list.html', {'patients': patients})

@login_required(login_url='/auth/login/')
def food_plan(request, id):
    patient = get_object_or_404(Patients, id=id)
    
    if not patient.nutri == request.user:
        messages.add_message(request, constants.ERROR, 'Esse paciente não é seu')
        return redirect('/patient-info-list/')
 
    meals = Meal.objects.filter(patient=patient).order_by('time')    
    options = Option.objects.all()
    return render(request, 'food_plan.html', {'patient': patient, 'meals': meals, 'options': options})

@login_required(login_url='/auth/login/')
def meal(request, id_patient):
    patient = get_object_or_404(Patients, id=id_patient)
    
    if not patient.nutri == request.user:
        messages.add_message(request, constants.ERROR, 'Esse paciente não é seu')
        return redirect('/patient-info-list/')
 
    if request.method == "POST":
        title = request.POST.get('title')
        time = request.POST.get('time')
        carbohydrates = request.POST.get('carbohydrates')
        proteins = request.POST.get('proteins')
        grease = request.POST.get('grease')

        if not post_meal_data_valid(request, title, time, carbohydrates, proteins, grease):
            return redirect(f'/food-plan/{id_patient}')

        r1 = Meal(patient=patient,
                title=title,
                time=time,
                carbohydrates=carbohydrates,
                proteins=proteins,
                grease=grease)
        r1.save()
        messages.add_message(request, constants.SUCCESS, 'Refeição cadastrada')
    
        return redirect(f'/food-plan/{id_patient}')

@login_required(login_url='/auth/login/')
def option(request, id_patient):
    
    if request.method == "POST":
        id_meal = request.POST.get('meal')
        image = request.FILES.get('image')
        description = request.POST.get("description")
        
        if image == None:
            messages.add_message(request, constants.ERROR, 'Obrigatorio adicionar uma imagem')
            return redirect(f'/food-plan/{id_patient}')
        
        if len(description.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Descrição precisa ser preenchido')
            return redirect(f'/food-plan/{id_patient}')
          
        o1 = Option(meal_id=id_meal,
                image=image,
                description=description)
        o1.save()
        messages.add_message(request, constants.SUCCESS, 'Opção cadastrada')
        
        return redirect(f'/food-plan/{id_patient}')



from django_xhtml2pdf.utils import generate_pdf


def generate_meals_pdf(request, id_patient):
    
    patient = get_object_or_404(Patients, id=id_patient)
    
    if not patient.nutri == request.user:
        messages.add_message(request, constants.ERROR, 'Esse paciente não é seu')
        return redirect('/patient-info-list/')
 
    meals = Meal.objects.filter(patient=patient).order_by('time')    
    options = Option.objects.all()
    
    filename = 'meals'

    context = {
        'patient': patient,
        'meals': meals,
        'options': options
    }

    resp = HttpResponse(content_type='application/pdf')
    resp['Content-Disposition'] = f'attachment; filename={filename}.pdf'
    response = generate_pdf('pdf_files/meals_pdf.html',file_object=resp, context=context)

    return response

