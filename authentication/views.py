from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .utils import post_data_valid, email_html
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.messages import constants
import os
from django.conf import settings
from .models import activation
from hashlib import sha256

def signup(request):
    if request.user.is_authenticated:
        return redirect('/patients/')

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
    
        if not post_data_valid(request, username, email, password, confirm_password):
            return redirect('/auth/signup')
        
        try:
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password,
                                            is_active=False)
            user.save()
            token = sha256(f"{username}{email}".encode()).hexdigest()
            Activation = activation(token=token, user=user)
            Activation.save()
            path_template = os.path.join(settings.BASE_DIR, 'authentication/templates/emails/signup_confirmed_template.html')
            email_html(path_template, 'Cadastro confirmado', [email,], username=username, link_ativacao=f"127.0.0.1:8000/auth/active-account/{token}")
            messages.add_message(request, constants.SUCCESS, 'Usuario cadastrado com sucesso')
            return redirect('/auth/login')
        except:
            return redirect('/auth/signup')

    
    return render(request, 'signup.html', {})
            
def login(request):
    if request.user.is_authenticated:
        return redirect('/patients/')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        
        if not user:      
            messages.add_message(request, constants.ERROR, '* Username ou senha inválidos')
            return redirect('/auth/login')
        else:   
            auth.login(request, user)


        return redirect('/patients/')

    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/auth/login')

def active_account(request, token):
    token = get_object_or_404(activation, token=token)
    if token.active:
        messages.add_message(request, constants.WARNING, 'Essa token já foi usado')
        return redirect('/auth/login')

    user = User.objects.get(username=token.user.username)
    user.is_active = True
    user.save()
    token.ativo = True
    token.save()
    messages.add_message(request, constants.SUCCESS, 'Conta ativa com sucesso')
    
    return redirect('/auth/login')