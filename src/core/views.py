from django.shortcuts import render, redirect
from EpicEvent_CRM.settings import LOGIN_REDIRECT_URL
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View

from . import forms

# Create your views here.
def logout_user(request):
    logout(request)
    return redirect('login')


class LoginPage(View):
    form_class = forms.LoginForm
    template_name = "core/login.html"

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(
            request,
            self.template_name,
            context={'form': form, 'message': message}
        )

    def post(self, request):
        form = forms.LoginForm(request.POST)
        message = ''
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('feed')
        message = 'Identifiants invalides.'
        return render(
            request,
            self.template_name,
            context={'form': form, 'message': message}
        )
