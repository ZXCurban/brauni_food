from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.admin_utils import (
    ContentTextareaMixin,
    badge,
    image_preview,
    make_unique_slug,
    message_for_update,
)

from .models import Product


@admin.action(description="Отметить выбранные товары как новинки")
def mark_as_new(modeladmin, request, queryset):
    updated = queryset.update(is_new=True)
    message_for_update(modeladmin, request, updated, "товары отмечены как новинки")


@admin.action(description="Снять отметку «Новинка»")
def unmark_as_new(modeladmin, request, queryset):
    updated = queryset.update(is_new=False)
    message_for_update(modeladmin, request, updated, "отметка «Новинка» снята")


@admin.action(description="Отметить выбранные товары как популярные")
def mark_as_popular(modeladmin, request, queryset):
    updated = queryset.update(is_popular=True)
    message_for_update(modeladmin, request, updated, "товары отмечены как популярные")


@admin.action(description="Снять отметку «Популярный»")
def unmark_as_popular(modeladmin, request, queryset):
    updated = queryset.update(is_popular=False)
    message_for_update(modeladmin, request, updated, "отметка «Популярный» снята")


@admin.register(Product)
class ProductAdmin(ContentTextareaMixin, admin.ModelAdmin):
    list_display = (
        "preview",
        "name",
        "category",
        "price",
        "weight",
        "sort_order",
        "status_badge",
        "is_new",
        "is_popular",
        "updated_at",
    )
    list_display_links = ("preview", "name")
    list_editable = ("price", "sort_order", "is_new", "is_popular")
    list_filter = (
        "category",
        "is_new",
        "is_popular",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "name",
        "slug",
        "ingredients",
        "description",
        "category__name",
    )
    autocomplete_fields = ("category",)
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("preview_large", "created_at", "updated_at")
    ordering = ("sort_order", "name")
    list_per_page = 25
    date_hierarchy = "created_at"
    actions = (mark_as_new, unmark_as_new, mark_as_popular, unmark_as_popular)
    save_on_top = True
    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "name",
                    "slug",
                    "category",
                    "price",
                    "sort_order",
                    "image",
                    "preview_large",
                )
            },
        ),
        (
            "Описание товара",
            {
                "fields": (
                    "description",
                    "ingredients",
                )
            },
        ),
        (
            "Характеристики",
            {
                "fields": (
                    "weight",
                    "shelf_life",
                    "storage_temperature",
                )
            },
        ),
        (
            "Продвижение на сайте",
            {
                "fields": (
                    "is_new",
                    "is_popular",
                )
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

    @admin.display(description="Превью")
    def preview(self, obj):
        return image_preview(obj)

    @admin.display(description="Изображение")
    def preview_large(self, obj):
        return image_preview(obj, width=320, height=220)

    @admin.display(description="Статус")
    def status_badge(self, obj):
        labels = []
        if obj.is_new:
            labels.append(badge("Новинка", "info"))
        if obj.is_popular:
            labels.append(badge("Популярный", "success"))

        return (
            mark_safe(" ".join(str(label) for label in labels))
            if labels
            else badge("Обычный", "neutral")
        )

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = make_unique_slug(Product, obj.name, obj.pk)
        super().save_model(request, obj, form, change)
