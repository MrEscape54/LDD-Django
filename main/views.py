from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
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
	paginate_by = 20
   
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
	paginate_by = 20

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

""" class ProductSearchListView(ListView):
	template_name = 'main/product_list.html'
	context_object_name = 'product_search_list_list'
	model = models.Product
	paginate_by = 20

	def get_queryset(self):
		searchInput = self.kwargs['searchInput']
		self.searchInput = None
		if self.searchInput:
			if request.user.is_staff or request.user.is_supersuser:
				products = model.objects.filter(name=self.searchInput)
			products = models.objects.active().filter(name=self.searchInput)

		return products.order_by('name') """

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

class AddressListView(LoginRequiredMixin, ListView):
	model = models.Address

	def get_queryset(self):
		return self.model.objects.filter(user=self.request.user)

class AddressCreateView(LoginRequiredMixin,CreateView):
	model = models.Address

	fields = ['name', 'address1', 'phone', 'zip_code', 'city', 'country']

	def form_valid(self, form):
		obj = form.save(commit=False)
		obj.user = self.request.user
		obj.save()
		return super().form_valid(form)

class AddressUpdateView(LoginRequiredMixin,UpdateView):
	model = models.Address

	fields = ['name', 'address1', 'phone', 'zip_code', 'city', 'country']

	success_url = reverse_lazy('main:address_list')

	def get_queryset(self):
		return self.model.objects.filter(user=self.request.user)

class AddressDeleteView(LoginRequiredMixin,DeleteView):
	model = models.Address
	success_url = reverse_lazy('main:address_list')

	def get_queryset(self):
		return self.model.objects.filter(user=self.request.user)

def add_basket(request):
	product = get_object_or_404(models.Product, pk=request.GET.get('product_id'))

	basket = request.basket
	if not request.basket:
		if request.user.is_authenticated:
			user = request.user
		else:
			user = None
		basket = models.Basket.objects.create(user=user)
		request.session['basket_id'] = basket.id
	
	basketline, created = models.BasketLine.objects.get_or_create(basket=basket, product=product)

	if not created:
		basketline.quantity += 1
		basketline.save()
	
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def manage_basket(request):
	if not request.basket:
		return render(request, 'basket.html', {'formset': None})

	if request.method == 'POST':
		formset = forms.BasketLineFormSet(request.POST, instance=request.basket)
		if formset.is_valid():
			formset.save()
	
	else:
		formset = forms.BasketLineFormSet(instance=request.basket)
	
	if request.basket.is_empty():
		return render(request, 'basket.html', {'formset': None})

	return render(request, 'basket.html', {'formset': formset})
	





	


		
	
