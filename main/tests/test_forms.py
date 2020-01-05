from django.test import TestCase
from django.core import mail
from main import forms

class TestForms(TestCase):
    def test_contact_us_send_email_form(self):
        form = forms.ContactForm({'name': 'Diego', 'message': 'Hola', 'subject': 'asunto', 'email': 'diego@diego.com', 'gender': 'M'})
        self.assertTrue(form.is_valid())

        with self.assertLogs('main.forms', level='INFO') as cm:
            form.send_mail()
        
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Site Message')
        self.assertGreaterEqual(len(cm.output), 1)

        def test_invalid_contact_us_form(self):
            form = forms.ContactForm({'message': "Hi there"})
            self.assertFalse(form.is_valid())
        

    