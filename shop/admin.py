from django.contrib import admin

# Register your models here.
from shop.models import Product, ProductImage, ProductSize, BasketItem, PromoCode


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 4


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductSizeInline]


class PromoCodeAdmin(admin.ModelAdmin):
    model = PromoCode


admin.site.register(Product, ProductAdmin)
admin.site.register(PromoCode)
