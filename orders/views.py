from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Order, OrderItem
from products.models import ProductVariant
from decimal import Decimal

# Вспомогательные функции
def get_cart(request):
    return request.session.get('cart', {})

def save_cart(request, cart):
    request.session['cart'] = cart

# --- VIEW: Просмотр корзины ---
def cart_view(request):
    cart = get_cart(request)
    cart_items = []
    total_price = Decimal('0.00')
    total_quantity = 0 # Считаем общее кол-во товаров
    updated = False

    variant_ids = list(cart.keys())

    for variant_id_str in variant_ids:
        try:
            variant_id = int(variant_id_str)
            variant = ProductVariant.objects.select_related('product', 'color', 'size').get(id=variant_id)
        except (ValueError, ProductVariant.DoesNotExist):
            del cart[variant_id_str]
            updated = True
            continue

        item = cart[variant_id_str]
        quantity = item.get('quantity', 1)
        price = variant.product.base_price
        line_total = price * quantity
        
        total_price += line_total
        total_quantity += quantity # Суммируем штуки

        cart_items.append({
            'variant': variant,
            'quantity': quantity,
            'line_total': line_total,
        })

    if updated:
        save_cart(request, cart)

    # Логика опта: если товаров > 10
    is_wholesale = total_quantity > 10

    context = {
        'cart_items': cart_items,
        'total': total_price,
        'total_quantity': total_quantity,
        'is_wholesale': is_wholesale,
    }
    return render(request, 'orders/cart.html', context)

# --- VIEW: Добавление в корзину ---
def add_to_cart(request, variant_id):
    variant = get_object_or_404(ProductVariant, id=variant_id)
    cart = get_cart(request)
    vid = str(variant_id)
    
    # Можно добавить логику получения кол-ва из POST, если нужно добавлять сразу много
    # quantity = int(request.POST.get('quantity', 1))
    
    if vid in cart:
        cart[vid]['quantity'] += 1
    else:
        cart[vid] = {'quantity': 1}
    
    save_cart(request, cart)
    messages.success(request, f"{variant.product.name} добавлен в корзину")
    
    # Возвращаемся туда, откуда пришли (или в корзину)
    return redirect('product_detail', pk=variant.product.pk)

# --- VIEW: Обновление количества (НОВОЕ) ---
@require_POST
def update_cart_item(request, variant_id):
    cart = get_cart(request)
    vid = str(variant_id)
    
    if vid in cart:
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity > 0:
                cart[vid]['quantity'] = quantity
            else:
                del cart[vid] # Если 0, удаляем
            save_cart(request, cart)
        except ValueError:
            pass
            
    return redirect('cart_view')

# --- VIEW: Удаление из корзины ---
def remove_from_cart(request, item_id):
    cart = get_cart(request)
    vid = str(item_id)
    if vid in cart:
        del cart[vid]
        save_cart(request, cart)
    return redirect('cart_view')

# --- VIEW: Оформление заказа ---
def checkout(request):
    cart = get_cart(request)
    if not cart:
        messages.error(request, "Корзина пуста")
        return redirect('cart_view')

    # Считаем итоги для отображения и логики опта
    total_quantity = 0
    calculated_price = Decimal('0.00')
    
    # Предварительный подсчет (без удаления "битых" товаров, так как это делает cart_view)
    # Но для надежности можно повторить логику валидации
    for vid_str, item in cart.items():
        try:
            variant = ProductVariant.objects.get(id=int(vid_str))
            qty = item.get('quantity', 1)
            total_quantity += qty
            calculated_price += variant.product.base_price * qty
        except:
            continue

    is_wholesale = total_quantity > 10

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()
        comment = request.POST.get('comment', '').strip()

        if not all([full_name, phone, email, address]):
            messages.error(request, "Заполните все обязательные поля")
            return render(request, 'orders/checkout.html', {'total': calculated_price, 'is_wholesale': is_wholesale})

        # Создаём заказ
        order = Order.objects.create(
            full_name=full_name,
            phone=phone,
            email=email,
            address=address,
            comment=comment,
            calculated_price=calculated_price,
            final_price=calculated_price, # Менеджер может изменить потом
            is_wholesale=is_wholesale,    # Записываем флаг опта
        )

        # Переносим товары из корзины в заказ
        for vid_str, item in cart.items():
            try:
                variant = ProductVariant.objects.get(id=int(vid_str))
                OrderItem.objects.create(
                    order=order,
                    variant=variant,
                    quantity=item['quantity'],
                    price_at_order=variant.product.base_price
                )
            except ProductVariant.DoesNotExist:
                continue

        # Очищаем корзину
        request.session['cart'] = {}

        messages.success(request, "Ваш заказ успешно оформлен! Мы свяжемся с вами для подтверждения.")
        return redirect('home')

    return render(request, 'orders/checkout.html', {
        'total': calculated_price,
        'is_wholesale': is_wholesale,
        'total_quantity': total_quantity
    })