from django.urls import path

from .views import ProductsPageView


urlpatterns = [

    path(
        '',
        ProductsPageView.as_view(),
        name='products',
    ),
]