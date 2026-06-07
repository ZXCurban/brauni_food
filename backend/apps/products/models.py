from django.db import models
from django.urls import reverse
from apps.admin_utils import validate_image
from apps.mixins import ImageURLMixin

from apps.categories.models import Category


class Product(ImageURLMixin, models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория",
    )

    name = models.CharField(
        max_length=255,
        verbose_name="Название",
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
        verbose_name="Slug",
        help_text="Заполняется автоматически из названия. Можно изменить вручную.",
    )

    image = models.ImageField(
        upload_to="products/", verbose_name="Изображение", validators=[validate_image]
    )

    description = models.TextField(
        blank=True,
        verbose_name="Описание",
    )

    ingredients = models.TextField(
        blank=True,
        verbose_name="Состав",
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
    )

    weight = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Вес",
    )

    shelf_life = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Срок годности",
    )

    storage_temperature = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Температура хранения",
    )

    is_new = models.BooleanField(
        default=False,
        verbose_name="Новинка",
    )

    is_popular = models.BooleanField(
        default=False,
        verbose_name="Популярный",
    )

    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок",
        help_text="Чем меньше число, тем выше товар в списке.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создан",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Обновлён",
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})
