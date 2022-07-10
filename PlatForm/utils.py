from django.contrib.messages import constants
from django.contrib import messages
from .models import Patients


def post_meal_data_valid(request, title, time, carbohydrates, proteins, grease):
    if (len(title.strip()) == 0) or (len(time.strip()) == 0) or (len(carbohydrates.strip()) == 0) or (len(proteins.strip()) == 0) or (len(grease.strip()) == 0):
        messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
        return False
    
    if (not carbohydrates.isnumeric()) or (not proteins.isnumeric()) or (not grease.isnumeric()):
        messages.add_message(request, constants.ERROR, 'Digite um valor válido')
        return False

    if (int(carbohydrates) < 0) or (int(proteins) < 0) or (int(grease) < 0):
        messages.add_message(request, constants.ERROR, 'Digite um valor válido')
        return False

    return True
   
def is_valid_decimal(value):
    try:
        float(value)
    except ValueError:
        return False
    else:
        return True

def post_patient_data_valid(request, weight, height, grease, muscle, hdl, ldl, colesterol_total, triglicerídios):
    if (len(weight.strip()) == 0) or (len(height.strip()) == 0) or (len(grease.strip()) == 0) or (len(muscle.strip()) == 0) or (len(hdl.strip()) == 0) or (len(ldl.strip()) == 0) or (len(colesterol_total.strip()) == 0) or (len(triglicerídios.strip()) == 0):
        messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
        return False
    
    if (not is_valid_decimal(height)):
        messages.add_message(request, constants.ERROR, 'Digite um valor válido')
        return False

    if (not weight.isnumeric()) or (not grease.isnumeric()) or (not muscle.isnumeric()) or (not hdl.isnumeric()) or (not ldl.isnumeric()) or (not colesterol_total.isnumeric()) or (not triglicerídios.isnumeric()):
        messages.add_message(request, constants.ERROR, 'Digite um valor válido')
        return False

    
    if (int(weight) < 0) or (float(height) < 0) or (int(grease) < 0) or (int(muscle) < 0) or (int(hdl) < 0) or (int(ldl) < 0) or (int(colesterol_total) < 0) or (int(triglicerídios) < 0):
        messages.add_message(request, constants.ERROR, 'Digite um valor válido')
        return False

    return True


def post_data_valid(request, name, gender, age, email, phone):
    if (len(name.strip()) == 0) or (len(gender.strip()) == 0) or (len(age.strip()) == 0) or (len(email.strip()) == 0) or (len(phone.strip()) == 0):
        messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
        return False
    
    if not age.isnumeric():
        messages.add_message(request, constants.ERROR, 'Digite uma idade válida')
        return False
    
    pacientes = Patients.objects.filter(email=email)

    if pacientes.exists():
        messages.add_message(request, constants.ERROR, 'Já existe um paciente com esse E-mail')
        return False
    
    return True