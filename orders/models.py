from django.db import models

ORDER_STATUS_CHOICES = [
    ('new', 'Новый'),
    ('processing', 'В обработке'),
    ('awaiting_payment', 'Ожидает оплаты'),
    ('paid', 'Оплачен'),
    ('delivered', 'Доставлен'),
    ('cancelled', 'Отменен'),
]

class Order(models.Model):
    full_name = models.CharField(max_length=200, verbose_name="ФИО")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")
    address = models.TextField(verbose_name="Адрес доставки")
    comment = models.TextField(blank=True, verbose_name="Комментарий к заказу")
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='new', verbose_name="Статус")
    calculated_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Рассчитанная сумма",
        default=0.00  # ← КЛЮЧЕВОЕ ИСПРАВЛЕНИЕ
    )
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Скидка")
    final_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Итоговая цена"
    )
    is_wholesale = models.BooleanField(default=False, verbose_name="Оптовый заказ")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заказ #{self.id} от {self.full_name}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    variant = models.ForeignKey('products.ProductVariant', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена на момент заказа")

    def __str__(self):
        return f"{self.variant.product.name} x{self.quantity}"

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказов"