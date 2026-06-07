from django.contrib import admin

from apps.admin_utils import (
    ContentTextareaMixin,
    badge,
    image_preview,
    make_unique_slug,
    message_for_update,
)
from .models import Vacancy


@admin.action(description="Активировать выбранные вакансии")
def make_active(modeladmin, request, queryset):
    updated = queryset.update(is_active=True)
    message_for_update(
        modeladmin, request, updated, "вакансии переведены в статус активных"
    )


@admin.action(description="Деактивировать выбранные вакансии")
def make_inactive(modeladmin, request, queryset):
    updated = queryset.update(is_active=False)
    message_for_update(modeladmin, request, updated, "вакансии скрыты с сайта")


@admin.register(Vacancy)
class VacancyAdmin(ContentTextareaMixin, admin.ModelAdmin):
    list_display = (
        "preview",
        "title",
        "salary",
        "schedule",
        "employment_type_badge",
        "status_badge",
        "created_at",
    )
    list_display_links = ("preview", "title")
    list_editable = ("salary", "schedule")
    list_filter = ("is_active", "employment_type", "salary_type", "created_at")
    search_fields = ("title", "slug", "short_description", "requirements")
    readonly_fields = ("preview_large", "created_at", "updated_at")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-created_at", "title")
    list_per_page = 20
    actions = (make_active, make_inactive)
    save_on_top = True

    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "title",
                    "slug",
                    "image",
                    "preview_large",
                    "is_active",
                )
            },
        ),
        (
            "Условия и оплата",
            {
                "fields": (
                    "salary",
                    "salary_type",
                    "employment_type",
                    "schedule",
                )
            },
        ),
        (
            "Контент",
            {
                "fields": (
                    "short_description",
                    "requirements",
                )
            },
        ),
        (
            "Даты",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    @admin.display(description="Превью")
    def preview(self, obj):
        return image_preview(obj)

    @admin.display(description="Изображение")
    def preview_large(self, obj):
        return image_preview(obj, width=320, height=200)

    @admin.display(description="Занятость")
    def employment_type_badge(self, obj):
        # Превращаем full/part/flex в красивые текстовые бейджи
        return badge(obj.get_employment_type_display(), "info")

    @admin.display(description="Статус")
    def status_badge(self, obj):
        if obj.is_active:
            return badge("Активна", "success")
        return badge("Архив", "neutral")

    # Безопасная генерация уникального слага на бэкенде
    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = make_unique_slug(Vacancy, obj.title, obj.pk)
        super().save_model(request, obj, form, change)
