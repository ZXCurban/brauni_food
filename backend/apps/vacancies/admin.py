from django.contrib import admin
from django.db import models
from django.forms import Textarea

from apps.admin_utils import boolean_badge, image_preview, make_unique_slug, message_for_update

from .models import Vacancy


@admin.action(description="Опубликовать выбранные вакансии")
def activate_vacancies(modeladmin, request, queryset):
    updated = queryset.update(is_active=True)
    message_for_update(modeladmin, request, updated, "вакансии опубликованы")


@admin.action(description="Снять выбранные вакансии с публикации")
def deactivate_vacancies(modeladmin, request, queryset):
    updated = queryset.update(is_active=False)
    message_for_update(modeladmin, request, updated, "вакансии сняты с публикации")


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = (
        "preview",
        "title",
        "employment_type",
        "salary_type",
        "salary",
        "activity",
        "is_active",
        "updated_at",
    )
    list_display_links = ("preview", "title")
    list_editable = ("is_active",)
    list_filter = (
        "employment_type",
        "salary_type",
        "is_active",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "title",
        "slug",
        "short_description",
        "requirements",
        "schedule",
        "salary",
    )
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("preview_large", "created_at", "updated_at")
    ordering = ("-created_at", "title")
    list_per_page = 25
    date_hierarchy = "created_at"
    actions = (activate_vacancies, deactivate_vacancies)
    save_on_top = True
    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "title",
                    "slug",
                    "short_description",
                    "image",
                    "preview_large",
                    "is_active",
                )
            },
        ),
        (
            "Работа и зарплата",
            {
                "fields": (
                    "employment_type",
                    "salary_type",
                    "salary",
                    "schedule",
                )
            },
        ),
        (
            "Условия и обязанности",
            {
                "fields": ("requirements",),
            },
        ),
        (
            "Служебная информация",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )
    formfield_overrides = {
        models.TextField: {
            "widget": Textarea(attrs={"rows": 5}),
        },
    }

    @admin.display(description="Превью")
    def preview(self, obj):
        return image_preview(obj)

    @admin.display(description="Изображение")
    def preview_large(self, obj):
        return image_preview(obj, width=320, height=220)

    @admin.display(description="Статус", ordering="is_active")
    def activity(self, obj):
        return boolean_badge(obj.is_active, yes="Опубликована", no="Скрыта")

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = make_unique_slug(Vacancy, obj.title, obj.pk)
        super().save_model(request, obj, form, change)
