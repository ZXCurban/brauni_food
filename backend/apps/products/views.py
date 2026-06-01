from django.views.generic import TemplateView

from apps.categories.models import Category

from .models import Product


class ProductsPageView(TemplateView):

    template_name = 'pages/products.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        categories = (
            Category.objects
            .filter(is_active=True)
            .prefetch_related('products')
            .order_by('sort_order')
        )

        context['categories'] = categories

        context['products'] = (
            Product.objects
            .select_related('category')
            .order_by('sort_order')
        )

        return context