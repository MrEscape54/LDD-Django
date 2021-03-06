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

    #Search
    #path('products/search/<slug:searchInput>', views.ProductSearchListView.as_view(), name='product-search'), """

    #Address CRUD
    path('address/', views.AddressListView.as_view(), name='address_list'),
    path('address/create/', views.AddressCreateView.as_view(), name='address_create'),
    path('address/<int:pk>/', views.AddressUpdateView.as_view(), name='address_update'),
    path('address/<int:pk>/delete/', views.AddressDeleteView.as_view(), name='address_delete'),

    # Authntication URLs
    path('accounts/register/', views.SignupView.as_view(), name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='main/auth/login.html', form_class=forms.AuthenticationForm), name='login'),
    path('accounts/logout/', LogoutView.as_view(), {'next_page': 'index'}, name='logout'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='main/auth/password_reset.html'), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='main/auth/password_reset_done.html'), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='main/auth/password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='main/auth/password_reset_complete.html'), name='password_reset_complete'),

    #basket
    path('add_to_basket', views.add_basket, name='add_to_basket'),
    path('basket/', views.manage_basket, name="basket"),
]