from django import forms


class LoginForm(forms.Form):
    email = forms.CharField(max_length=150, label="Adresse mail")
    password = forms.CharField(max_length=128, widget=forms.PasswordInput, label="Mot de passe")
