from django.contrib import admin

from apps.admin_utils import (
    ContentTextareaMixin,
    boolean_badge,
    image_preview,
    message_for_update,
)

from .models import (
    CompanyFeature,
    CompanyGalleryImage,
    CompanyInfo,
    CompanySection,
    HeroSlide,
    HomeBlock,
)


@admin.action(description="Включить выбранные записи")
def activate_items(modeladmin, request, queryset):
    updated = queryset.update(is_active=True)
    message_for_update(modeladmin, request, updated, "записи включены")


@admin.action(description="Отключить выбранные записи")
def deactivate_items(modeladmin, request, queryset):
    updated = queryset.update(is_active=False)
    message_for_update(modeladmin, request, updated, "записи отключены")


@admin.register(CompanyInfo)
class CompanyInfoAdmin(ContentTextareaMixin, admin.ModelAdmin):
    list_display = (
        "title",
        "phone",
        "email",
        "status_badge",
    )

    def has_add_permission(self, request):
        if CompanyInfo.objects.exists():
            return False
        return super().has_add_permission(request)

    search_fields = (
        "title",
        "legal_name",
        "short_description",
        "about_text",
        "phone",
        "email",
        "address",
        "inn",
        "ogrn",
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
            "Юридические реквизиты",
            {
                "fields": (
                    "legal_name",
                    "inn",
                    "kpp",
                    "ogrn",
                    "legal_address",
                    "director_name",
                    "director_position",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Банковские реквизиты",
            {
                "fields": (
                    "bank_name",
                    "bik",
                    "payment_account",
                    "correspondent_account",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    @admin.display(description="Главное изображение")
    def hero_preview(self, obj):
        return image_preview(obj, field_name="hero_image", width=360, height=230)

    @admin.display(description="Статус", ordering="is_active")
    def status_badge(self, obj):
        return boolean_badge(obj.is_active)


@admin.register(HomeBlock)
class HomeBlockAdmin(ContentTextareaMixin, admin.ModelAdmin):
    list_display = ("__str__", "status_badge")
    readonly_fields = ("straight_preview", "curve_preview")
    save_on_top = True
    fieldsets = (
        (
            "Прямая спираль (Brauni для бизнеса)",
            {
                "fields": (
                    "straight_title",
                    "straight_description",
                    "straight_button_text",
                    "straight_button_url",
                    "straight_image",
                    "straight_preview",
                )
            },
        ),
        (
            "Изогнутая спираль (Работа в Brauni)",
            {
                "fields": (
                    "curve_title",
                    "curve_description",
                    "curve_button_text",
                    "curve_button_url",
                    "curve_image",
                    "curve_preview",
                )
            },
        ),
        (
            "Настройки",
            {
                "fields": ("is_active",),
            },
        ),
    )

    @admin.display(description="Изображение (прямая)")
    def straight_preview(self, obj):
        return image_preview(obj, field_name="straight_image", width=320, height=220)

    @admin.display(description="Изображение (изогнутая)")
    def curve_preview(self, obj):
        return image_preview(obj, field_name="curve_image", width=320, height=220)

    @admin.display(description="Статус", ordering="is_active")
    def status_badge(self, obj):
        return boolean_badge(obj.is_active)

    def has_add_permission(self, request):
        if HomeBlock.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(HeroSlide)
class HeroSlideAdmin(ContentTextareaMixin, admin.ModelAdmin):
    list_display = (
        "preview",
        "title",
        "sort_order",
        "status_badge",
        "is_active",
    )
    list_display_links = ("preview", "title")
    list_editable = ("sort_order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "description", "button_text")
    readonly_fields = ("preview_large",)
    ordering = ("sort_order", "title")
    list_per_page = 25
    actions = (activate_items, deactivate_items)
    save_on_top = True
    autocomplete_fields = ("link_category",)
    fieldsets = (
        (
            "Слайд карусели",
            {
                "fields": (
                    "title",
                    "description",
                    "button_text",
                    "link_category",
                    "button_url",
                    "image",
                    "preview_large",
                    "sort_order",
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
        return image_preview(obj, width=360, height=240)

    @admin.display(description="Статус", ordering="is_active")
    def status_badge(self, obj):
        return boolean_badge(obj.is_active)


@admin.register(CompanyFeature)
class CompanyFeatureAdmin(ContentTextareaMixin, admin.ModelAdmin):
    list_display = (
        "title",
        "icon",
        "order",
        "status_badge",
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
    def status_badge(self, obj):
        return boolean_badge(obj.is_active)


@admin.register(CompanySection)
class CompanySectionAdmin(ContentTextareaMixin, admin.ModelAdmin):
    list_display = (
        "preview",
        "title",
        "order",
        "image_left",
        "status_badge",
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
    def status_badge(self, obj):
        return boolean_badge(obj.is_active)


@admin.register(CompanyGalleryImage)
class CompanyGalleryImageAdmin(admin.ModelAdmin):
    list_display = (
        "preview",
        "title",
        "order",
        "status_badge",
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
    def status_badge(self, obj):
        return boolean_badge(obj.is_active)
