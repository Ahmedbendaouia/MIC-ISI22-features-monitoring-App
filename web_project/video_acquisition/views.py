from django.shortcuts import render, redirect
from django.contrib.auth import authenticate ,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url='login') 
def home(request):
    return render(request,'home.html') 

def loginPage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')        
        user =authenticate(request,username=username, password=password)                
        if user is not None:
            print('user is logged')
            login(request,user)
            return redirect('/')
        else :            
            messages.info(request,'UserName or password is incorrect !')            
    
    context={}
    return render(request, 'registration/login.html',context)


def logoutPage(request):
    logout(request)
    return redirect('login')
     
     
def error_404(request, exception):
    return render(request, 'errors/404.html')     