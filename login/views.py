from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout
from .services.seniorBackends import require_authentication




def login_view(request:HttpRequest):
    if (request.method == "GET"): return render(request, 'login.html')          
    elif (request.method == "POST"): 
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user: 
            login(request, user)
            return redirect('home')
        else: 
            msg = "Usuário ou senha inválidos!"
            contexto = {
                "username":username,
                "password":password,
                "message": msg
                } 
            return render(request, 'login.html', contexto)     
        
        
        
def logout_view(request:HttpRequest): 
    logout(request)
    return redirect('login')  


@require_authentication
def home_view(request:HttpRequest):
    return render(request, 'base.html')
    
      



