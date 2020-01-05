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