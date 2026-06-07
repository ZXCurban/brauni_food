from django.conf import settings

from django.conf.urls.static import static

from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap, Sitemap
from django.contrib.sitemaps.views import sitemap

from django.urls import include, path
from django.views.generic import TemplateView

from apps.company.views import HomePageView
from apps.products.models import Product
from apps.categories.models import Category


# ---- Sitemaps ----
class BrauniStaticSitemap(Sitemap):
    priority = 1.0
    changefreq = "weekly"

    def items(self):
        return ["home", "products", "company", "vacancies"]

    def location(self, item):
        from django.urls import reverse

        return reverse(item)


product_sitemap_dict = {
    "queryset": Product.objects.select_related("category").filter(
        category__is_active=True,
    ),
}

category_sitemap_dict = {
    "queryset": Category.objects.filter(is_active=True),
}

sitemaps = {
    "static": BrauniStaticSitemap,
    "products": GenericSitemap(product_sitemap_dict, priority=0.8, changefreq="weekly"),
    "categories": GenericSitemap(
        category_sitemap_dict, priority=0.9, changefreq="weekly"
    ),
}


admin.site.site_header = "Brauni Food"
admin.site.site_title = "Brauni Admin"
admin.site.index_title = "Панель управления"


urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),
    path(
        "",
        HomePageView.as_view(),
        name="home",
    ),
    path(
        "products/",
        include("apps.products.urls"),
    ),
    path(
        "vacancies/",
        include("apps.vacancies.urls"),
    ),
    path(
        "company/",
        include("apps.company.urls"),
    ),
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="robots.txt",
            content_type="text/plain",
        ),
    ),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
