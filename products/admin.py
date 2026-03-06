from django.contrib import admin
from .models import Category, Product, ProductImage, Color, Size, ProductVariant, HomePageBanner

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'slug', 'banner_image')
    list_filter = ('type',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(HomePageBanner)
class HomePageBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'image')
    list_filter = ('is_active',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'base_price', 'created_at')
    list_filter = ('category', 'created_at')
    inlines = [ProductImageInline, ProductVariantInline]
    search_fields = ('name',)

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'size', 'stock')
    list_filter = ('color', 'size', 'product__category')