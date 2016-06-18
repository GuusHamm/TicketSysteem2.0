from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import View

from accounts.forms import LoginForm


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
                    return redirect("tickets:index")
                else:
                    messages.error(request, "Deze account is niet geactiveerd")
                    return self.get(request)
            else:
                messages.warning(request, "Gebruikersnaam of wachtwoord klopt niet")
                return self.get(request)


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Uitloggen is gelukt!")

        return redirect("account:login")
