from django.test import TestCase
from django.urls import reverse
from main import forms

class TestPage(TestCase):
    def test_index_page_works(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'LDD')

    def test_about_us_page_works(self):
        response = self.client.get(reverse('about_us'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about_us.html')
        self.assertContains(response, 'LDD')
    
    def test_contact_page_works(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertContains(response, 'LDD')

    def test_faq_page_works(self):
        response = self.client.get(reverse('faq'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'faq.html')
        self.assertContains(response, 'LDD')

    def test_contact_us_page_works(self):
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertContains(response, 'LDD')
        self.assertIsInstance(response.context["form"], forms.ContactForm)
    
    def test_user_signup_page_loads_correctly(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "signup.html")
        self.assertContains(response, "BookTime")
        self.assertIsInstance(response.context["form"], forms.UserCreationForm)

    def test_user_signup_page_submission_works(self):
        post_data = {
            "email": "user@domain.com",
            "password1": "abcabcabc",
            "password2": "abcabcabc",
        }
        with patch.object(forms.UserCreationForm, "send_mail") as mock_send:
            response = self.client.post(reverse("signup"), post_data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(models.User.objects.filter(email="user@domain.com").exists())
        self.assertTrue(auth.get_user(self.client).is_authenticated)
        mock_send.assert_called_once()
   
