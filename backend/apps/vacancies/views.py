from django.views.generic import TemplateView

from .models import Vacancy


class VacanciesPageView(TemplateView):
    template_name = "pages/vacancies.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vacancies"] = Vacancy.objects.filter(is_active=True).order_by(
            "-created_at"
        )
        return context
