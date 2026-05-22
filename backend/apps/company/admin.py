from django.contrib import admin
from django.db import models
from django.forms import Textarea

from apps.admin_utils import boolean_badge, image_preview, message_for_update

from .models import (
    CompanyFeature,
    CompanyGalleryImage,
    CompanyInfo,
    CompanySection,
)


@admin.action(description="Включить выбранные записи")
def activate_items(modeladmin, request, queryset):
    updated = queryset.update(is_active=True)
    message_for_update(modeladmin, request, updated, "записи включены")


@admin.action(description="Отключить выбранные записи")
def deactivate_items(modeladmin, request, queryset):
    updated = queryset.update(is_active=False)
    message_for_update(modeladmin, request, updated, "записи отключены")


class ContentTextareaMixin:
    formfield_overrides = {
        models.TextField: {
            "widget": Textarea(attrs={"rows": 5}),
        },
    }


@admin.register(CompanyInfo)
class CompanyInfoAdmin(ContentTextareaMixin, admin.ModelAdmin):
    list_display = (
        "title",
        "phone",
        "email",
        "activity",
    )
    search_fields = (
        "title",
        "short_description",
        "about_text",
        "phone",
        "email",
        "address",
    )
    readonly_fields = ("hero_preview",)
    save_on_top = True
    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "title",
                    "short_description",
                    "about_text",
                    "mission_text",
                    "work_text",
                    "hero_image",
                    "hero_preview",
                    "is_active",
                )
            },
        ),
        (
            "Контакты",
            {
                "fields": (
                    "phone",
                    "email",
                    "address",
                    "whatsapp_url",
                    "telegram_url",
                )
            },
        ),
        (
            "Реквизиты",
            {
                "fields": (
                    "inn",
                    "ogrn",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    @admin.display(description="Главное изображение")
    def hero_preview(self, obj):
        return image_preview(obj, field_name="hero_image", width=360, height=230)

    @admin.display(description="Статус", ordering="is_active")
    def activity(self, obj):
        return boolean_badge(obj.is_active)

    def has_add_permission(self, request):
        if CompanyInfo.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(CompanyFeature)
class CompanyFeatureAdmin(ContentTextareaMixin, admin.ModelAdmin):
    list_display = (
        "title",
        "icon",
        "order",
        "activity",
        "is_active",
    )
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "description", "icon")
    ordering = ("order", "title")
    list_per_page = 25
    actions = (activate_items, deactivate_items)
    save_on_top = True
    fieldsets = (
        (
            "Преимущество",
            {
                "fields": (
                    "title",
                    "description",
                    "icon",
                    "order",
                    "is_active",
                )
            },
        ),
    )

    @admin.display(description="Статус", ordering="is_active")
    def activity(self, obj):
        return boolean_badge(obj.is_active)


@admin.register(CompanySection)
class CompanySectionAdmin(ContentTextareaMixin, admin.ModelAdmin):
    list_display = (
        "preview",
        "title",
        "order",
        "image_left",
        "activity",
        "is_active",
    )
    list_display_links = ("preview", "title")
    list_editable = ("order", "image_left", "is_active")
    list_filter = ("is_active", "image_left")
    search_fields = ("title", "text")
    readonly_fields = ("preview_large",)
    ordering = ("order", "title")
    list_per_page = 25
    actions = (activate_items, deactivate_items)
    save_on_top = True
    fieldsets = (
        (
            "Секция страницы",
            {
                "fields": (
                    "title",
                    "text",
                    "image",
                    "preview_large",
                    "image_left",
                    "order",
                    "is_active",
                )
            },
        ),
    )

    @admin.display(description="Превью")
    def preview(self, obj):
        return image_preview(obj)

    @admin.display(description="Изображение")
    def preview_large(self, obj):
        return image_preview(obj, width=320, height=220)

    @admin.display(description="Статус", ordering="is_active")
    def activity(self, obj):
        return boolean_badge(obj.is_active)


@admin.register(CompanyGalleryImage)
class CompanyGalleryImageAdmin(admin.ModelAdmin):
    list_display = (
        "preview",
        "title",
        "order",
        "activity",
        "is_active",
    )
    list_display_links = ("preview", "title")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title",)
    readonly_fields = ("preview_large",)
    ordering = ("order", "title")
    list_per_page = 25
    actions = (activate_items, deactivate_items)
    save_on_top = True
    fieldsets = (
        (
            "Изображение галереи",
            {
                "fields": (
                    "title",
                    "image",
                    "preview_large",
                    "order",
                    "is_active",
                )
            },
        ),
    )

    @admin.display(description="Превью")
    def preview(self, obj):
        return image_preview(obj)

    @admin.display(description="Изображение")
    def preview_large(self, obj):
        return image_preview(obj, width=320, height=220)

    @admin.display(description="Статус", ordering="is_active")
    def activity(self, obj):
        return boolean_badge(obj.is_active)
