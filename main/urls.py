from django.urls import path
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from main import views
from main import models

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('about/', TemplateView.as_view(template_name='about_us.html'), name='about_us'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('faq/', TemplateView.as_view(template_name='faq.html'), name='faq'),
    path('products/brand/<slug:brand>', views.ProductByBrandListView.as_view(), name='productsbrand'),
    path('products/tags/<slug:tag>', views.ProductListView.as_view(), name='products'),
    path('product/<slug>', DetailView.as_view(model=models.Product), name='product'),
]