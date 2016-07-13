from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import View

from accounts.forms import LoginForm, RegisterForm


class LoginView(View):
    context = {}
    template = "account/login.html"

    def get(self, request):
        if request.user.is_active:
            messages.warning(request, "Je bent al ingelogd")
            return redirect("tickets:index")
        self.context['loginform'] = LoginForm()
        return render(request, self.template, self.context)

    def post(self, request):
        loginform = LoginForm(request.POST)

        if loginform.is_valid():
            user = authenticate(username=loginform.cleaned_data['username'],
                                password=loginform.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, "Succesvol ingelogd")
                    if user.is_staff:
                        return redirect("admin:index")
                    else:
                        return redirect("tickets:index")
                else:
                    messages.error(request, "Deze account is nog niet geactiveerd")
                    return self.get(request)
            else:
                messages.warning(request, "Gebruikersnaam of wachtwoord klopt niet")
                return self.get(request)


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Uitloggen is gelukt!")

        return redirect("account:login")


class CreateNewAccountView(View):
    def get(self, request):
        context = {}

        context['registerform'] = RegisterForm()
        return render(request, "account/new.html", context)

    def post(self, request):
        registerform = RegisterForm(request.POST)

        if registerform.is_valid():
            username = registerform.cleaned_data['username']
            email = registerform.cleaned_data['email']
            password = registerform.cleaned_data['password']
            password_conf = registerform.cleaned_data['password_repeat']
            first_name = registerform.cleaned_data['first_name']
            last_name = registerform.cleaned_data['last_name']

            if password != password_conf:
                messages.error(request, "De wachtwoorden kwamen niet overeen")
                return self.get(request)

            User.objects.create_user(username=username, password=password, email=email, first_name=first_name,
                                     last_name=last_name, is_staff=False, is_superuser=False, is_active=False)

            user = User.objects.get(username=username)

            if user.pk is not None:
                messages.success(request, "Account aangemaakt!")
            else:
                messages.error(request, "Account niet aangemaakt")

            return redirect("tickets:index")
        else:
            context = {'registerform': registerform}

            return render(request, "account/new.html", context)
