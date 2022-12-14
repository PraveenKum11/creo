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

from cauth import forms

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
    register_form = forms.Register()

    if request.method == "POST":
        register_form = forms.Register(request.POST)
        if register_form.is_valid():
            clean_user = {
                "username" : register_form.cleaned_data["username"],
                "password" : register_form.cleaned_data["password"],
            }
            confirm_password = register_form.cleaned_data["confirm_password"]

            if clean_user["password"] != confirm_password:
                messages.error(request, "Password did not match")
                return HttpResponseRedirect(request.path_info) # Page refresh

            if get_user_model().objects.filter(username = clean_user["username"]).exists():
                messages.error(request, "Username already exists")
                return HttpResponseRedirect(request.path_info)
            else:
                User.objects.create_user(**clean_user)
                return HttpResponseRedirect("/auth/login")

    context = {
        "register_form" : register_form,
    }

    return render(request, "cauth/register.html", context)

def check_username(request):
    username = request.POST.get("username")
    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse("<div id='username-error' class='error'>This username exists</div>")
    else:
        return HttpResponse("<div id='username-error' class='success'>This username is available</div>")