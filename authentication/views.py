from django.shortcuts import render, redirect
from django.http import HttpResponse
from .utils import valid_post_data
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.messages import constants

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
    
        if not valid_post_data(request, username, email, password, confirm_password):
            return redirect('/auth/signup')
        
        try:
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password,
                                            is_active=False)
            user.save()
            return redirect('/auth/login')
        except:
            return redirect('/auth/signup')

    
    return render(request, 'signup.html', {})
            
def login(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('password')
        usuario = auth.authenticate(username=username, password=senha)
        
        if not usuario:      
            messages.add_message(request, constants.ERROR, '* Username ou senha inválidos')
            return redirect('/auth/login')
        else:   
            auth.login(request, usuario)

        print("teto")
        return redirect('/')

    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/auth/login')