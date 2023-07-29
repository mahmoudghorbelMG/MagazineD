from django.contrib import admin
from .models import Product, ProductSeries

class ProductAdmin(admin.ModelAdmin):
    list_display = ('Product_name', 'owner', 'price', 'series','product_slug', 'quantity_in_stock')

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductSeries)
