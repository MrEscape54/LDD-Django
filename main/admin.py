from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import (UserAdmin as DjangoUserAdmin)
from main import models


admin.AdminSite.site_header = 'LDD - Administración del Sitio'
admin.AdminSite.site_title = 'LDD'
admin.AdminSite.index_title = 'Administración'

@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_filter = ('active',)
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name',)}

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'slug', 'in_stock', 'formated_price')
    list_filter = ('active', 'in_stock', 'date_updated')
    list_editable = ('in_stock', )
    search_fields = ('name', )  
    autocomplete_fields = ('tags',)
    prepopulated_fields = {'slug': ('name',)}
    fields = ('name', 'brand', ('price', 'active', 'in_stock'),'description', 'tags', 'slug')

    def formated_price(self, obj):
        return '$ {:20,.2f}'.format(obj.price)

        '{:,.2f}'.format(num)

    formated_price.short_description = 'precio'

@admin.register(models.ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_filter = ('active',)
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name',)}


@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_tag', 'product_name')
    exclude = ('thumbnail',)
    search_fields = ('product__name',)

    def thumbnail_tag(self, obj):
        if obj.thumbnail:
            return format_html('<img src="%s" height="30px"/>' % obj.thumbnail.url)
        return "-"

    thumbnail_tag.short_description = 'miniatura'

    def product_name(self, obj):
        return obj.product.name
    
    product_name.short_description = 'producto'

@admin.register(models.User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Important dates",
            {"fields": ("last_login", "date_joined")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "first_name", "password1", "password2"),
            },
        ),
    )
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)