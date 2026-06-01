from django.views.generic import TemplateView


class VacanciesPageView(TemplateView):

    template_name = 'pages/vacancies.html'