import re
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.models import User

def valid_post_data(request, username, email, password, confirm_password):
    if username == '' and email == '' and password == '':
        messages.add_message(request, constants.ERROR, '* E necessario preencher os campos para avançar')
        return False
    if len(password) < 6:
        messages.add_message(request, constants.ERROR, '* Sua senha deve conter 6 ou mais caracteres')
        return False
    if not password == confirm_password:
        messages.add_message(request, constants.ERROR, '* As senhas não coincidem!')
        return False
    if not re.search('[A-Z]', password):
        messages.add_message(request, constants.ERROR, '* Sua senha não contem letras maiúsculas')
        return False
    if not re.search('[a-z]', password):
        messages.add_message(request, constants.ERROR, '* Sua senha não contem letras minúsculas')
        return False
    if not re.search('[1-9]', password):
        messages.add_message(request, constants.ERROR, '* Sua senha não contém números')
        return False
    if User.objects.filter(username=username):
        messages.add_message(request, constants.ERROR, '* Já existe um usuario com esse nome')
        return False
        
    return True