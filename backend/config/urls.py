from django.conf import settings

from django.conf.urls.static import static

from django.contrib import admin

from django.urls import include, path

from apps.company.views import HomePageView


admin.site.site_header = 'Brauni Food'
admin.site.site_title = 'Brauni Admin'
admin.site.index_title = 'Панель управления'


urlpatterns = [

    path(
        'admin/',
        admin.site.urls,
    ),

    path(
        '',
        HomePageView.as_view(),
        name='home',
    ),

    path(
        'products/',
        include('apps.products.urls'),
    ),

    path(
        'vacancies/',
        include('apps.vacancies.urls'),
    ),

    path(
        'company/',
        include('apps.company.urls'),
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
