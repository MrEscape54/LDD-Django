from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import UserPassesTestMixin
import os
import logging
from django.contrib.auth import login, authenticate
from django.contrib import messages
from main import forms, models, views

logger = logging.getLogger(__name__)

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

class SignupView(FormView):
	template_name = 'main/auth/register.html'
	form_class = forms.UserCreationForm

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('/')
		return super().dispatch(request, *args, **kwargs)

	def get_success_url(self):
		redirect_to = self.request.GET.get('next', '/')
		return redirect_to
	
	def form_valid(self, form):
		response = super().form_valid(form)
		form.save()
		email = form.cleaned_data.get('email')
		first_name = form.cleaned_data.get('first_name')
		raw_password = form.cleaned_data.get('password1')
		logger.info('Nuevo registro para email=%s a través de SignupView', email)
		user = authenticate(email=email, password=raw_password)
		login(self.request, user)
		form.send_mail()

		return response
	
