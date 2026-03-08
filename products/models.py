from django.db import models

class Category(models.Model):
    TYPE_CHOICES = [
        ('medical', 'Медицинская одежда'),
        ('horeca', 'HoReCa'),
    ]
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(unique=True)
    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        verbose_name="Тип категории",
        blank=True
    )
    banner_image = models.ImageField(
        upload_to='banners/',
        verbose_name="Баннер категории",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


# === МОДЕЛЬ ДЛЯ БАННЕРА НА ГЛАВНОЙ СТРАНИЦЕ ===
class HomePageBanner(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название баннера")
    image = models.ImageField(upload_to='banners/', verbose_name="Изображение баннера")
    link = models.URLField(verbose_name="Ссылка", blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Баннер главной"
        verbose_name_plural = "Баннеры главной"


# === МОДЕЛЬ ДЛЯ БАННЕРА В КАТАЛОГЕ ===
class CatalogBanner(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    subtitle = models.CharField(max_length=300, verbose_name="Подзаголовок", blank=True)
    image = models.ImageField(upload_to='catalog_banners/', verbose_name="Изображение баннера")
    link = models.URLField(verbose_name="Ссылка", blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Баннер каталога"
        verbose_name_plural = "Баннеры каталога"
        ordering = ['order']


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    base_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Базовая цена"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория"
    )
    gender = models.CharField(
        max_length=10,
        choices=[
            ('unisex', 'Унисекс'),
            ('male', 'Мужской'),
            ('female', 'Женский'),
        ],
        blank=True,
        verbose_name="Пол (только для медицины)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='products/', verbose_name="Изображение")

    def __str__(self):
        return f"Изображение для {self.product.name}"

    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товаров"


class Color(models.Model):
    name = models.CharField(max_length=50, verbose_name="Цвет")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"


class Size(models.Model):
    name = models.CharField(max_length=20, verbose_name="Размер")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Размер"
        verbose_name_plural = "Размеры"


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='variants',
        on_delete=models.CASCADE
    )
    color = models.ForeignKey(Color, on_delete=models.CASCADE, verbose_name="Цвет")
    size = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name="Размер")
    stock = models.PositiveIntegerField(default=0, verbose_name="Остаток (опционально)")

    def __str__(self):
        return f"{self.product.name} - {self.color.name} / {self.size.name}"

    class Meta:
        verbose_name = "Вариант товара"
        verbose_name_plural = "Варианты товаров"
        unique_together = ('product', 'color', 'size')