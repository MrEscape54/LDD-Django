from main.models import Brand, ProductTag
import os
from django.conf import settings
from glob import glob

image_list=[]
app_static_dir = os.path.join(os.path.join(os.path.join(os.path.join(settings.BASE_DIR,'main'),'static'),'images'),'logos')
for file in os.listdir(app_static_dir):
	image_list.append(file)

def add_variable_to_context(request):
    return {
        'brands': Brand.objects.all().order_by('name'),
        'tags' : ProductTag.objects.exclude(name='Hombre').exclude(name='Mujer').order_by('name'),
        'logos' : image_list
    }