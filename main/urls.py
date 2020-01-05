from django.urls import path
from django.views.generic import TemplateView
from main import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('about/', TemplateView.as_view(template_name='about_us.html'), name='about_us'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('faq/', TemplateView.as_view(template_name='faq.html'), name='faq'),
    path('products/<slug:tag>', views.ProductListView.as_view(), name='products'),
]