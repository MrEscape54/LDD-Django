from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
import os
from main import forms, models, views

def show_images(request):
	image_list=[]
	app_static_dir = os.path.join(os.path.join(os.path.join(os.path.join(settings.BASE_DIR,'main'),'static'),'images'),'logos')
	for file in os.listdir(app_static_dir):
		image_list.append(file)
	
	return render(request, 'main/index.html', {'image_brands': image_list})

class ContactView(FormView):
	template_name = 'contact.html'
	form_class = forms.ContactForm
	success_url = '/'

	def form_valid(self, form):
		form.send_mail()
		return super().form_valid(form)

class ProductListView(ListView):
	""" template_name = 'main/product_list.html' """
	""" context_object_name = 'product_list' """
	model = models.Product
	paginate_by = 24
   
	""" def get_context_data(self, **kwargs):
		context = super(ProductListView, self).get_context_data(**kwargs)
		context.update({'product_images_list': models.ProductImage.objects.all()})
		return context """
		
	def get_queryset(self):
		tag = self.kwargs['tag']
		self.tag = None
		if tag != 'all':
			self.tag = get_object_or_404(models.ProductTag, slug=tag)
		if self.tag:
			products = models.Product.objects.active().filter(tags=self.tag)
		else:
			products = models.Product.objects.active()
		
		return products.order_by('name')

class ProductByBrandListView(ListView):
	template_name = 'main/product_list.html'
	context_object_name = 'product_by_brand_list'
	model = models.Product
	paginate_by = 24

	def get_queryset(self):
		brand = self.kwargs['brand']
		self.brand = None
		if brand != 'all':
			self.brand = get_object_or_404(models.Brand, slug=brand)
		if self.brand:
			products = models.Product.objects.active().filter(brand=self.brand)
		else:
			products = models.Product.objects.active()
		
		return products.order_by('name')