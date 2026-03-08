from django.contrib import admin
from .models import Category, CatalogBanner, Product, ProductImage, Color, Size, ProductVariant

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

@admin.register(CatalogBanner)
class CatalogBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'is_active', 'order', 'image')
    list_filter = ('is_active',)  # ✅ УБРАЛИ 'category__type' — его нет в модели
    search_fields = ('title', 'subtitle')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'gender', 'base_price', 'created_at')
    list_filter = ('category', 'gender', 'created_at')
    search_fields = ('name', 'description')
    inlines = [ProductImageInline, ProductVariantInline]

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