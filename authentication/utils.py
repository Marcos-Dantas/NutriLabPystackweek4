import re
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def email_html(path_template: str, assunto: str, para: list, **kwargs) -> dict:
    html_content = render_to_string(path_template, kwargs)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(assunto, text_content, settings.EMAIL_HOST_USER, para)
    email.attach_alternative(html_content, "text/html")
    email.send()

    return {'status': 1}

def post_data_valid(request, username, email, password, confirm_password):
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