from datetime import timedelta

from django import template
from django.contrib.admin.models import LogEntry
from django.db import DatabaseError, ProgrammingError
from django.utils import timezone

from apps.categories.models import Category
from apps.company.models import CompanyFeature, CompanyGalleryImage, CompanySection
from apps.products.models import Product
from apps.vacancies.models import Vacancy

register = template.Library()


def safe_count(queryset):
    try:
        return queryset.count()
    except (DatabaseError, ProgrammingError):
        return None


@register.simple_tag
def brauni_admin_metrics():
    week_ago = timezone.now() - timedelta(days=7)

    company_blocks = (
        safe_count(CompanyFeature.objects.filter(is_active=True)),
        safe_count(CompanySection.objects.filter(is_active=True)),
        safe_count(CompanyGalleryImage.objects.filter(is_active=True)),
    )
    company_blocks_count = None if any(value is None for value in company_blocks) else sum(company_blocks)

    return [
        {
            "label": "Товары",
            "value": safe_count(Product.objects.all()),
            "hint": "Всего позиций в каталоге",
        },
        {
            "label": "Активные категории",
            "value": safe_count(Category.objects.filter(is_active=True)),
            "hint": "Доступны для витрины",
        },
        {
            "label": "Вакансии",
            "value": safe_count(Vacancy.objects.filter(is_active=True)),
            "hint": "Опубликованы на сайте",
        },
        {
            "label": "Блоки компании",
            "value": company_blocks_count,
            "hint": "Преимущества, секции и галерея",
        },
        {
            "label": "Действия за 7 дней",
            "value": safe_count(LogEntry.objects.filter(action_time__gte=week_ago)),
            "hint": "Активность сотрудников в админке",
        },
    ]
