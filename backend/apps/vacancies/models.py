from django.db import models
from apps.admin_utils import validate_image


class Vacancy(models.Model):

    class SalaryType(models.TextChoices):
        FIXED = "fixed", "Фиксированная"
        PERCENT = "percent", "Сдельная"

    class EmploymentType(models.TextChoices):
        FULL = "full", "Полная занятость"
        PART = "part", "Неполная занятость"
        FLEX = "flex", "Свободный график"

    title = models.CharField(
        max_length=255,
        verbose_name="Название вакансии"
    )

    slug = models.SlugField(
        unique=True,
        blank=True,
        verbose_name="Slug",
        help_text="Заполняется автоматически из названия. Можно изменить вручную.",
    )

    short_description = models.TextField(
        verbose_name="Краткое описание"
    )

    requirements = models.TextField(
        verbose_name="Условия и обязанности"
    )

    schedule = models.CharField(
        max_length=255,
        verbose_name="График работы"
    )

    salary_type = models.CharField(
        max_length=20,
        choices=SalaryType.choices,
        default=SalaryType.FIXED,
        verbose_name="Тип зарплаты"
    )

    employment_type = models.CharField(
        max_length=20,
        choices=EmploymentType.choices,
        default=EmploymentType.FULL,
        verbose_name="Тип занятости"
    )

    salary = models.CharField(
        max_length=255,
        verbose_name="Зарплата"
    )

    image = models.ImageField(
        upload_to="vacancies/",
        verbose_name="Изображение",
        validators=[validate_image]
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна"
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
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def image_url(self):

        if self.image:
            return self.image.url

        return '/static/images/placeholders/placeholder.png'