from django.contrib import admin
from product.models import Product, AccessModel


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner',)


@admin.register(AccessModel)
class AccessAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'value')
