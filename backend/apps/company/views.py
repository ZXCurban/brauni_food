from typing import Any, Dict

from django.db.models import Prefetch
from django.views.generic import TemplateView

from apps.categories.models import Category
from apps.products.models import Product
from apps.vacancies.models import Vacancy

from .models import (
    CompanySection,
    HeroSlide,
    HomeBlock,
)


class HomePageView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:

        context = super().get_context_data(**kwargs)

        categories = Category.objects.filter(is_active=True).prefetch_related(
            Prefetch(
                "products",
                queryset=Product.objects.order_by("sort_order")[:6],
                to_attr="featured_products",
            )
        )

        featured_category = categories.first()

        featured_products = (
            featured_category.featured_products if featured_category else []
        )

        context["categories"] = categories
        context["featured_category"] = featured_category
        context["featured_products"] = featured_products
        context["vacancies"] = Vacancy.objects.filter(is_active=True).order_by(
            "-created_at"
        )[:3]
        context["hero_slides"] = HeroSlide.objects.filter(is_active=True).order_by(
            "sort_order"
        )
        context["home_block"] = HomeBlock.objects.filter(is_active=True).first()

        return context


class CompanyPageView(TemplateView):
    template_name = "pages/company.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["sections"] = CompanySection.objects.filter(is_active=True).order_by(
            "order"
        )[:4]
        # company_info already provided by the global context processor
        return context
