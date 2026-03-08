from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Product, Category, CatalogBanner

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    catalog_banner = CatalogBanner.objects.filter(is_active=True).order_by('order').first()

    # Фильтры
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    min_price = request.GET.get('min_price')
    if min_price:
        try:
            products = products.filter(base_price__gte=float(min_price))
        except ValueError:
            pass

    max_price = request.GET.get('max_price')
    if max_price:
        try:
            products = products.filter(base_price__lte=float(max_price))
        except ValueError:
            pass

    gender = request.GET.get('gender')
    if gender:
        products = products.filter(gender=gender)

    # Сортировка
    sort = request.GET.get('sort', '-created_at')
    valid_sorts = ['base_price', '-base_price', '-created_at']
    if sort in valid_sorts:
        products = products.order_by(sort)

    # Пагинация
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'categories': categories,
        'catalog_banner': catalog_banner,
        'selected_category': category_slug,
        'selected_gender': gender,
        'min_price': min_price,
        'max_price': max_price,
        'sort': sort,
        'page_obj': page_obj,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})