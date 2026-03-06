from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Sum, Q
from django.utils.safestring import mark_safe
from django.core.mail import send_mail
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('price_at_order', 'get_product_name')
    
    def get_product_name(self, obj):
        return obj.variant.product.name
    get_product_name.short_description = "Товар"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone', 'email', 'status', 'calculated_price', 'final_price', 'is_wholesale', 'created_at')
    list_filter = ('status', 'is_wholesale', 'created_at')
    search_fields = ('full_name', 'phone', 'email', 'address')
    readonly_fields = ('calculated_price', 'customer_order_history')
    inlines = [OrderItemInline]
    fieldsets = (
        ('Данные клиента', {
            'fields': ('full_name', 'phone', 'email', 'address', 'comment')
        }),
        ('Финансы', {
            'fields': ('calculated_price', 'discount_amount', 'final_price', 'is_wholesale')
        }),
        ('Статус', {
            'fields': ('status',)
        }),
        ('История заказов клиента', {
            'fields': ('customer_order_history',),
            'classes': ('collapse',)
        }),
    )
    actions = ['mark_as_processing', 'mark_as_paid', 'mark_as_delivered', 'mark_as_cancelled', 'send_confirmation_email']

    def customer_order_history(self, obj):
        if not obj.phone and not obj.email:
            return "Нет данных для поиска истории"
        
        query = Q()
        if obj.phone:
            query |= Q(phone=obj.phone)
        if obj.email:
            query |= Q(email=obj.email)
        
        other_orders = Order.objects.filter(query).exclude(id=obj.id).order_by('-created_at')
        count = other_orders.count()
        
        if count == 0:
            return "Первый заказ клиента"
        
        total_sum = other_orders.aggregate(total=Sum('calculated_price'))['total'] or 0
        
        html = f"<div style='padding: 10px; background: #f8f9fa; border-radius: 8px;'>"
        html += f"<strong>Ранее заказов:</strong> {count}<br>"
        html += f"<strong>Общая сумма:</strong> {total_sum:.2f} ₽<br><br>"
        html += f"<strong>Последние заказы:</strong><br>"
        
        for order in other_orders[:5]:
            status_color = {
                'new': '#6c757d',
                'processing': '#17a2b8',
                'awaiting_payment': '#ffc107',
                'paid': '#28a745',
                'delivered': '#20c997',
                'cancelled': '#dc3545',
            }.get(order.status, '#6c757d')
            
            status_badge = f"<span style='display: inline-block; padding: 2px 8px; background: {status_color}; color: white; border-radius: 12px; font-size: 0.85em;'>{order.get_status_display()}</span>"
            
            html += f"• Заказ #{order.id} от {order.created_at.strftime('%d.%m.%Y %H:%M')} — {order.calculated_price:.2f} ₽ — {status_badge}<br>"
        
        if count > 5:
            html += f"<br><small>+ ещё {count - 5} заказов</small>"
        
        html += "</div>"
        
        return mark_safe(html)
    
    customer_order_history.short_description = "История заказов клиента"

    def mark_as_processing(self, request, queryset):
        updated = queryset.update(status='processing')
        self.message_user(request, f"Обновлено {updated} заказов")
    mark_as_processing.short_description = "Отметить как 'В обработке'"

    def mark_as_paid(self, request, queryset):
        updated = queryset.update(status='paid')
        self.message_user(request, f"Обновлено {updated} заказов")
    mark_as_paid.short_description = "Отметить как 'Оплачен'"

    def mark_as_delivered(self, request, queryset):
        updated = queryset.update(status='delivered')
        self.message_user(request, f"Обновлено {updated} заказов")
    mark_as_delivered.short_description = "Отметить как 'Доставлен'"

    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f"Обновлено {updated} заказов")
    mark_as_cancelled.short_description = "Отметить как 'Отменен'"

    def send_confirmation_email(self, request, queryset):
        from django.conf import settings
        success_count = 0
        fail_count = 0
        
        for order in queryset:
            try:
                subject = f'Подтверждение заказа #{order.id} — Gandas Uniforms'
                
                message = f"""
Уважаемый(ая) {order.full_name}!

Ваш заказ #{order.id} успешно оформлен.

Статус: {order.get_status_display()}
Сумма заказа: {order.final_price or order.calculated_price} ₽

Детали заказа:
"""
                for item in order.items.all():
                    message += f"- {item.variant.product.name} ({item.variant.color.name}, {item.variant.size.name}) x{item.quantity} — {item.price_at_order} ₽\n"
                
                message += f"""
                
Адрес доставки: {order.address}

С вами свяжется наш менеджер для подтверждения заказа.

С уважением,
Команда Gandas Uniforms
"""
                
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[order.email],
                    fail_silently=False,
                )
                success_count += 1
            except Exception as e:
                print(f"Ошибка отправки на {order.email}: {e}")
                fail_count += 1
        
        if success_count > 0:
            self.message_user(request, f"Успешно отправлено {success_count} писем")
        if fail_count > 0:
            self.message_user(request, f"Не удалось отправить {fail_count} писем", level='ERROR')
    
    send_confirmation_email.short_description = "Отправить подтверждение на email"