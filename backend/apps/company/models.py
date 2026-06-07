from django.db import models
from apps.admin_utils import validate_image
from apps.mixins import ImageURLMixin


class CompanyInfo(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название компании")

    short_description = models.TextField(blank=True, verbose_name="Краткое описание")

    about_text = models.TextField(blank=True, verbose_name="Текст о компании")

    mission_text = models.TextField(blank=True, verbose_name="Миссия компании")

    work_text = models.TextField(blank=True, verbose_name="Как мы работаем")

    hero_image = models.ImageField(
        upload_to="company/hero/",
        blank=True,
        null=True,
        verbose_name="Главное изображение",
    )

    phone = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Телефон",
    )

    email = models.EmailField(
        blank=True,
        verbose_name="Email",
    )

    address = models.TextField(
        blank=True,
        verbose_name="Адрес",
    )

    inn = models.CharField(max_length=32, blank=True, verbose_name="ИНН")

    ogrn = models.CharField(max_length=32, blank=True, verbose_name="ОГРН")

    whatsapp_url = models.URLField(
        blank=True,
        verbose_name="Ссылка WhatsApp",
    )

    telegram_url = models.URLField(
        blank=True,
        verbose_name="Ссылка Telegram",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна",
    )

    class Meta:
        verbose_name = "Информация о компании"
        verbose_name_plural = "Информация о компании"

    def __str__(self):
        return self.title


class CompanyFeature(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Заголовок",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Описание",
    )

    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Название Material Icon",
        verbose_name="Иконка",
    )

    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активно",
    )

    class Meta:
        ordering = ["order"]
        verbose_name = "Преимущество"
        verbose_name_plural = "Преимущества"

    def __str__(self):
        return self.title


class CompanySection(ImageURLMixin, models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Заголовок",
    )

    text = models.TextField(
        verbose_name="Текст",
    )

    image = models.ImageField(
        upload_to="company/sections/",
        blank=True,
        null=True,
        verbose_name="Изображение",
        validators=[validate_image],
    )

    image_left = models.BooleanField(default=True, verbose_name="Изображение слева")

    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна",
    )

    class Meta:
        ordering = ["order"]
        verbose_name = "Секция"
        verbose_name_plural = "Секции"

    def __str__(self):
        return self.title


class CompanyGalleryImage(ImageURLMixin, models.Model):
    image = models.ImageField(
        upload_to="company/gallery/",
        verbose_name="Изображение",
        validators=[validate_image],
    )

    title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Название",
    )

    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активно",
    )

    class Meta:
        ordering = ["order"]
        verbose_name = "Фото галереи"
        verbose_name_plural = "Галерея"


class HeroSlide(ImageURLMixin, models.Model):
    image = models.ImageField(
        upload_to="hero/slides/",
        verbose_name="Изображение слайда",
        validators=[validate_image],
    )

    title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Заголовок",
    )

    description = models.TextField(
        max_length=500,
        blank=True,
        verbose_name="Текст",
    )

    button_text = models.CharField(
        max_length=100,
        blank=True,
        default="Подробнее",
        verbose_name="Текст кнопки",
    )

    button_url = models.CharField(
        max_length=500,
        blank=True,
        default="/products/",
        verbose_name="Ссылка кнопки",
    )

    link_category = models.ForeignKey(
        "categories.Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Категория для перехода",
        help_text="Если выбрана категория — кнопка будет вести на её страницу.",
    )

    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
    )

    class Meta:
        ordering = ["sort_order"]
        verbose_name = "Слайд карусели"
        verbose_name_plural = "Слайды карусели"

    def __str__(self):
        return self.title or f"Слайд {self.pk}"

    def save(self, *args, **kwargs):
        # Auto-generate button_url from linked category
        if self.link_category and (
            not self.button_url or self.button_url == "/products/"
        ):
            from django.urls import reverse

            self.button_url = reverse(
                "category_detail",
                kwargs={"slug": self.link_category.slug},
            )
        super().save(*args, **kwargs)


class HomeBlock(ImageURLMixin, models.Model):
    """Singleton – контент двух спиральных блоков на главной."""

    image_field_name: str = "straight_image"

    # --- Spiral Straight ---
    straight_title = models.CharField(
        max_length=200,
        blank=True,
        default="Brauni для бизнеса",
        verbose_name="Заголовок (прямая спираль)",
    )
    straight_description = models.TextField(
        max_length=500,
        blank=True,
        default="Готовый ассортимент для витрин и кофеен. Собираем стабильную линейку десертов, сэндвичей и гастрономии под ежедневные продажи.",
        verbose_name="Описание (прямая спираль)",
    )
    straight_button_text = models.CharField(
        max_length=100,
        blank=True,
        default="Смотреть каталог",
        verbose_name="Текст кнопки (прямая спираль)",
    )
    straight_button_url = models.CharField(
        max_length=500,
        blank=True,
        default="/products/",
        verbose_name="Ссылка кнопки (прямая спираль)",
    )
    straight_image = models.ImageField(
        upload_to="home/blocks/",
        blank=True,
        null=True,
        validators=[validate_image],
        verbose_name="Изображение (прямая спираль)",
    )

    # --- Spiral Curve ---
    curve_title = models.CharField(
        max_length=200,
        blank=True,
        default="Работа в Brauni",
        verbose_name="Заголовок (изогнутая спираль)",
    )
    curve_description = models.TextField(
        max_length=500,
        blank=True,
        default="Собираем аккуратную команду для производства, кухни и ежедневной работы с продуктом.",
        verbose_name="Описание (изогнутая спираль)",
    )
    curve_button_text = models.CharField(
        max_length=100,
        blank=True,
        default="Смотреть вакансии",
        verbose_name="Текст кнопки (изогнутая спираль)",
    )
    curve_button_url = models.CharField(
        max_length=500,
        blank=True,
        default="/vacancies/",
        verbose_name="Ссылка кнопки (изогнутая спираль)",
    )
    curve_image = models.ImageField(
        upload_to="home/blocks/",
        blank=True,
        null=True,
        validators=[validate_image],
        verbose_name="Изображение (изогнутая спираль)",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
    )

    def save(self, *args, **kwargs):
        self._compress_image_field("straight_image")
        self._compress_image_field("curve_image")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Блоки главной страницы"
        verbose_name_plural = "Блоки главной страницы"

    def __str__(self):
        return "Контент спиральных блоков"
