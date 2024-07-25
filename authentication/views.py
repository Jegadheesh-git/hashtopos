from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

def user_login(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,('login successfull!'))
            return redirect('get_menu')
        else:
            messages.success(request,('login failed!'))
            return redirect('login') 

    else:
        return render(request,'login.html')

def user_logout(request):
    logout(request) 
    messages.success(request,('logout successfull!'))
    return redirect('home')

def displayHome(request):
    if request.user.is_authenticated:
        return redirect('get_menu')
    else:
        return redirect('login')


