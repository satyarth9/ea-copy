from django.shortcuts import render, redirect
from django.contrib import auth


def home(request):
    if request.user.is_authenticated:
        return redirect('landing')
    return render(request, 'accounts/login.html')


def login(request):
    if request.method == "POST":
        user = auth.authenticate(username= request.POST['login_username'], password= request.POST['login_password'])
        if user is not None:
            auth.login(request, user)
            return redirect('landing')
        else:
            error = "Not authenticated"
            context = {
                'error' : error
            }
            return render(request, 'accounts/login.html', context)


def logout(request):
    auth.logout(request)
    return redirect('home')