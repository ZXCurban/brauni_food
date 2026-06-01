from django.urls import path

from .views import CompanyPageView


urlpatterns = [

    path(
        '',
        CompanyPageView.as_view(),
        name='company',
    ),
]