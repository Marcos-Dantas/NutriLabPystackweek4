from django.contrib.messages import constants
from django.contrib import messages
from .models import Patients

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