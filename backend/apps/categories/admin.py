from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html

from apps.admin_utils import boolean_badge, image_preview, make_unique_slug, message_for_update
from apps.products.models import Product

from .models import Category


class ProductInline(admin.TabularInline):
    model = Product
    fields = ("preview", "product_link", "price", "is_new", "is_popular")
    readonly_fields = fields
    extra = 0
    can_delete = False
    show_change_link = True
    verbose_name = "Товар"
    verbose_name_plural = "Товары в категории"

    @admin.display(description="Превью")
    def preview(self, obj):
        return image_preview(obj, width=72, height=54)

    @admin.display(description="Название")
    def product_link(self, obj):
        url = reverse("admin:products_product_change", args=(obj.pk,))
        return format_html('<a href="{}">{}</a>', url, obj.name)

    def has_add_permission(self, request, obj=None):
        return False


@admin.action(description="Включить выбранные категории")
def activate_categories(modeladmin, request, queryset):
    updated = queryset.update(is_active=True)
    message_for_update(modeladmin, request, updated, "категории включены")


@admin.action(description="Отключить выбранные категории")
def deactivate_categories(modeladmin, request, queryset):
    updated = queryset.update(is_active=False)
    message_for_update(modeladmin, request, updated, "категории отключены")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "preview",
        "name",
        "slug",
        "sort_order",
        "activity",
        "is_active",
        "products_count",
        "created_at",
    )
    list_display_links = ("preview", "name")
    list_editable = ("sort_order", "is_active")
    list_filter = ("is_active", "created_at", "updated_at")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("preview_large", "created_at", "updated_at")
    ordering = ("sort_order", "name")
    list_per_page = 25
    date_hierarchy = "created_at"
    actions = (activate_categories, deactivate_categories)
    save_on_top = True
    inlines = (ProductInline,)
    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "name",
                    "slug",
                    "sort_order",
                    "is_active",
                    "image",
                    "preview_large",
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

    @admin.display(description="Статус", ordering="is_active")
    def activity(self, obj):
        return boolean_badge(obj.is_active)

    @admin.display(description="Товаров", ordering="products_count")
    def products_count(self, obj):
        return obj.products_count

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(products_count=Count("products"))

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = make_unique_slug(Category, obj.name, obj.pk)
        super().save_model(request, obj, form, change)
