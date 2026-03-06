from django.shortcuts import render, get_object_or_404
from .models import InfoPage, FAQ
from products.models import Product
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from products.models import Product, Category, HomePageBanner  # ✅ Правильный импорт
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
    return render(request, 'core/home.html', context)

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


def home(request):
    popular_products = Product.objects.all()[:6]  # или по флагу из админки
    return render(request, 'core/home.html', {'popular_products': popular_products})

def info_page(request, slug):
    page = get_object_or_404(InfoPage, slug=slug)
    return render(request, 'core/info_page.html', {'page': page})

def faq_list(request):
    faqs = FAQ.objects.all()
    return render(request, 'core/faq.html', {'faqs': faqs})