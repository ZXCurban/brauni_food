from django.db import models
from django.urls import reverse
from apps.admin_utils import validate_image
from apps.mixins import ImageURLMixin


class Category(ImageURLMixin, models.Model):
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
        upload_to="categories/",
        blank=True,
        null=True,
        verbose_name="Изображение",
        validators=[validate_image],
    )

    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок",
        help_text="Чем меньше число, тем выше категория в списке.",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создана",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Обновлена",
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})
