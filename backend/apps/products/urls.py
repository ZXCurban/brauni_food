from django.urls import path

from .views import CategoryDetailView, ProductDetailView, ProductsPageView


urlpatterns = [
    path(
        "",
        ProductsPageView.as_view(),
        name="products",
    ),
    path(
        "category/<slug:slug>/",
        CategoryDetailView.as_view(),
        name="category_detail",
    ),
    path(
        "<slug:slug>/",
        ProductDetailView.as_view(),
        name="product_detail",
    ),
]
