from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Product, Category
# products/views.py

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Product, Category, HomePageBanner  # Убедитесь, что HomePageBanner импортирован
from decimal import Decimal

def home(request):
    # Баннеры для главной
    main_banner = HomePageBanner.objects.filter(is_active=True, title__icontains='main').first()
    medical_banner = HomePageBanner.objects.filter(is_active=True, title__icontains='medical').first()
    horeca_banner = HomePageBanner.objects.filter(is_active=True, title__icontains='horeca').first()
    ad_banners = HomePageBanner.objects.filter(is_active=True, title__icontains='ad')[:3]

    # Информация
    categories = Category.objects.all()

    context = {
        'main_banner': main_banner,
        'medical_banner': medical_banner,
        'horeca_banner': horeca_banner,
        'ad_banners': ad_banners,
        'categories': categories,
    }
    return render(request, 'core/home.html', context) # Убедитесь, что шаблон указан правильно


def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # Фильтрация по типу (medical/horeca)
    main_category = request.GET.get('main_category')
    if main_category:
        products = products.filter(category__type=main_category)
        categories = categories.filter(type=main_category)

    paginator = Paginator(products, 9)  # 9 товаров на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'categories': categories,
        'selected_category': category_slug,
        'main_category': main_category,
        'page_obj': page_obj,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})


# --- Остальные ваши функции из старого views.py ---
# Например:
# def add_to_cart(request, variant_id):
#     ...
# def cart_view(request):
#     ...
# def checkout(request):
#     ...

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    paginator = Paginator(products, 9)  # 9 товаров на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'categories': categories,
        'selected_category': category_slug,
        'page_obj': page_obj,
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})