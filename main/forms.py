from django.contrib.auth.forms import (UserCreationForm as DjangoUserCreationForm)
from django.contrib.auth.forms import UsernameField
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django import forms
from django.forms import inlineformset_factory
from django.core.mail import send_mail
import logging
from main import models

logger = logging.getLogger(__name__)

CHOICES = [('M', 'Hombre'), ('F', 'Mujer')]
 
class ContactForm(forms.Form):
    name = forms.CharField(label=False, min_length=3, widget=forms.TextInput(attrs={'placeholder': 'Nombre'}))
    subject = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder': 'Asunto'}))
    email = forms.EmailField(label=False, widget=forms.EmailInput(attrs={'placeholder': 'Correo Electrónico'}))
    message = forms.CharField(label=False, widget=forms.Textarea(attrs={'placeholder': 'Escribe tu mensaje aquí'}))
    gender = forms.ChoiceField(required=False, widget=forms.RadioSelect, choices=CHOICES)

    def send_mail(self):
        logger.info('Sending email to customer service')
        message = f'From: {self.cleaned_data["name"]}\nemail: {self.cleaned_data["email"]}\nSubject: {self.cleaned_data["subject"]}\nMessage: {self.cleaned_data["message"]}'

        send_mail('Site Message', message, 'site@ldd.domain', ['customerservice@ldd.domain'], fail_silently=False)

class UserCreationForm(DjangoUserCreationForm):
    class Meta(DjangoUserCreationForm.Meta):
        model = models.User
        fields = ('email', 'first_name')
        field_classes = {'email': UsernameField}
    
    def send_mail(self):
        logger.info("Enviando correo de registro para email=%s", self.cleaned_data['email'],)
        message = f"Bienvenido {self.cleaned_data['email']}"
        send_mail('Bienvenido a LDD', message, 'site@ldd.com', [self.cleaned_data['email']], fail_silently=True)

class AuthenticationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(strip=False, widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email is not None and password:
            self.user = authenticate(self.request, email=email, password=password)
            if self.user is None:
                raise forms.ValidationError("Usuario o contraseña incorrecta")
            logger.info("Authentication successful for email=%s", email)
    
        return self.cleaned_data

    def get_user(self):
        return self.user

BasketLineFormSet = inlineformset_factory(models.Basket, models.BasketLine, fields=('quantity',), extra=0,)

   

