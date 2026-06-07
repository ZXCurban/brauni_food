from typing import Any, Dict

from django.db.models import Prefetch
from django.views.generic import DetailView, TemplateView

from apps.categories.models import Category
from apps.company.models import HomeBlock
from apps.vacancies.models import Vacancy

from .models import Product


class ProductsPageView(TemplateView):
    template_name = "pages/products.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        categories = list(
            Category.objects.filter(is_active=True).order_by("sort_order", "name")
        )

        context["featured_categories"] = categories[:4]
        context["remaining_categories"] = categories[4:]
        context["home_block"] = HomeBlock.objects.filter(is_active=True).first()
        context["vacancies"] = Vacancy.objects.filter(is_active=True).order_by(
            "-created_at"
        )[:3]

        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = "pages/category_detail.html"
    context_object_name = "category"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        products = Product.objects.select_related("category").order_by(
            "sort_order",
            "name",
        )

        return Category.objects.filter(is_active=True).prefetch_related(
            Prefetch("products", queryset=products)
        )


class ProductDetailView(DetailView):
    model = Product
    template_name = "pages/product_detail.html"
    context_object_name = "product"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):

        return Product.objects.select_related("category").filter(
            category__is_active=True
        )
