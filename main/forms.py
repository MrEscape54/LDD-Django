from django import forms
from django.core.mail import send_mail
import logging

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

