from django.views.generic import TemplateView

from apps.categories.models import Category
from apps.products.models import Product


class HomePageView(TemplateView):

    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        categories = Category.objects.filter(
            is_active=True
        ).prefetch_related('products')

        featured_category = categories.first()

        featured_products = Product.objects.filter(
            category=featured_category
        ).order_by(
            'sort_order'
        )[:6]

        context['categories'] = categories
        context['featured_category'] = featured_category
        context['featured_products'] = featured_products

        return context


class CompanyPageView(TemplateView):

    template_name = 'pages/company.html'