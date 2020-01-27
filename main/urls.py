from django.urls import path
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from main import forms
from main import views
from main import models

app_name = 'main'   

urlpatterns = [
    path('about/', TemplateView.as_view(template_name='about_us.html'), name='about-us'),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('faq/', TemplateView.as_view(template_name='faq.html'), name='faq'),
    path('products/brand/<slug:brand>', views.ProductByBrandListView.as_view(), name='product-brand'),
    path('products/tags/<slug:tag>', views.ProductListView.as_view(), name='products'),
    path('product/<slug:slug>', DetailView.as_view(model=models.Product), name='product'),
    path('register/', views.SignupView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html', form_class=forms.AuthenticationForm), name='login'),
    path('logout/', LogoutView.as_view(), {'next_page': 'index'}, name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password-change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='main/reset_password.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='main/reset_password_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]