from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404

from main import forms, models

# Create your views here.
class ContactView(FormView):
	template_name = 'contact.html'
	form_class = forms.ContactForm
	success_url = '/'

	def form_valid(self, form):
		form.send_mail()
		return super().form_valid(form)

class ProductListView(ListView):
	template_name = 'product_list.html'
	context_object_name = 'products_list'
	model = models.Product
	paginate_by = 4
   
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
