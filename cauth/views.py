from django.shortcuts import render
from django.contrib.auth import (
        authenticate,
        login,
        logout,
        get_user_model,
)
from django.http import (
    HttpResponseRedirect,
    HttpResponse,
)
from django.contrib.auth.models import User
from django.contrib import messages

from cauth import (
    forms,
    models,
)

# Create your views here.

def login_user(request):
    error = None
    login_form = forms.Login()

    if request.method == "POST":
        login_form = forms.Login(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                error = "Invalid Username or Password"

    context = {
        "form" : login_form,
        "error" : error
    }

    return render(request, "cauth/login.html", context)

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/auth/login")

def register(request):
    form = forms.UserRegisterForm()

    if request.method == "POST":
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}", extra_tags="success")
            return HttpResponseRedirect("/auth/login")

    context = {
        "form" : form,
    }

    return render(request, "cauth/register.html", context)

def check_username(request):
    username = request.POST.get("username")
    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse("<div id='username-error' class='error'>This username exists</div>")
    else:
        return HttpResponse("<div id='username-error' class='success'>This username is available</div>")
