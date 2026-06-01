from django.urls import path

from .views import VacanciesPageView


urlpatterns = [

    path(
        '',
        VacanciesPageView.as_view(),
        name='vacancies',
    ),
]