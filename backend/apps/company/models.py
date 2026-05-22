from django.db import models
from apps.admin_utils import validate_image

class CompanyInfo(models.Model):

    title = models.CharField(
        max_length=255,
        verbose_name="Название компании"
    )

    short_description = models.TextField(
        verbose_name="Краткое описание"
    )

    about_text = models.TextField(
        verbose_name="Текст о компании"
    )

    mission_text = models.TextField(
        blank=True,
        verbose_name="Миссия компании"
    )

    work_text = models.TextField(
        blank=True,
        verbose_name="Как мы работаем"
    )

    hero_image = models.ImageField(
        upload_to="company/hero/",
        verbose_name="Главное изображение"
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

    inn = models.CharField(
        max_length=32,
        blank=True,
        verbose_name="ИНН"
    )

    ogrn = models.CharField(
        max_length=32,
        blank=True,
        verbose_name="ОГРН"
    )

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
    

class CompanySection(models.Model):

    title = models.CharField(
        max_length=255,
        verbose_name="Заголовок",
    )

    text = models.TextField(
        verbose_name="Текст",
    )

    image = models.ImageField(
        upload_to="company/sections/",
        verbose_name="Изображение",
        validators=[validate_image]
    )

    image_left = models.BooleanField(
        default=True,
        verbose_name="Изображение слева"
    )

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
    
    @property
    def image_url(self):

        if self.image:
            return self.image.url

        return '/static/images/placeholders/placeholder.png'

    

class CompanyGalleryImage(models.Model):

    image = models.ImageField(
        upload_to="company/gallery/",
        verbose_name="Изображение",
        validators=[validate_image]
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


    @property
    def image_url(self):

        if self.image:
            return self.image.url

        return '/static/images/placeholders/placeholder.png'


