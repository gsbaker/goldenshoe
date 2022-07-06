from django.contrib import admin

# Register your models here.
from shop.models import Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ]


admin.site.register(Product, ProductAdmin)
