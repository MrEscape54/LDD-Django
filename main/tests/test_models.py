from django.test import TestCase
from decimal import Decimal
from main import models

class TestModel(TestCase):
   def test_active_manager_works(self):
      models.Product.objects.create(name='TAG', price=Decimal('1000'))
      models.Product.objects.create(name='Rolex', price=Decimal('1000.30'), active=False)
      self.assertEqual(len(models.Product.objects.active()), 1)
      

