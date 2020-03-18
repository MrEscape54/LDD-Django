from main.models import Brand, ProductTag, Product
import os
from django.conf import settings
from glob import glob

def add_variable_to_context(request):
    return {
        'brands': Brand.objects.all().order_by('name'),
        'tags': ProductTag.objects.exclude(name='Hombre').exclude(name='Mujer').order_by('name'),
        'searchInput': Product.objects.all().order_by('name'),
    }