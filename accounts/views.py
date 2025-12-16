from django.shortcuts import render,redirect
from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

# Create your views here.
def UserLoginView(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username,password=password)

        if user is not None:
            print('logado com sucesso')
            login(request, user)
            return redirect('home')
        else:
            print('vacilão')
            form = AuthenticationForm()

    return render(request, 'user_login.html',{'form':form})


def logout_view(request):
    logout(request)
    return redirect('user_log')