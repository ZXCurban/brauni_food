import re

from django.test import TestCase
from django.urls import reverse

from .models import CompanyInfo, CompanySection


class CompanyPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company_info = CompanyInfo.objects.create(
            title="ООО Брауни Фуд",
            phone="+7 999 000-00-00",
            email="info@example.com",
            address="Москва",
            inn="1234567890",
            ogrn="1234567890123",
        )
        cls.sections = [
            CompanySection.objects.create(
                title=f"Секция {index}",
                text=f"Текст секции {index}",
                image_left=index % 2 == 0,
                order=index,
            )
            for index in range(1, 6)
        ]

    def test_company_page_uses_first_four_active_sections_in_order(self):
        response = self.client.get(reverse("company"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["sections"]),
            self.sections[:4],
        )
        for section in self.sections[:4]:
            self.assertContains(response, section.title)
            self.assertContains(response, section.text)
        self.assertNotContains(response, self.sections[4].title)

    def test_company_page_shows_existing_spiral_assets_and_labels(self):
        response = self.client.get(reverse("company"))

        for value in (
            "images/backgrounds/spiral_curve.svg",
            "icons/halal.svg",
            "icons/quality.svg",
            "icons/cooperation.svg",
            "Халяль продукция",
            "Высокое качество",
            "Выгодное сотрудничество",
        ):
            self.assertContains(response, value)

    def test_company_page_shows_legal_information_from_database(self):
        response = self.client.get(reverse("company"))

        for value in (
            self.company_info.title,
            self.company_info.phone,
            self.company_info.email,
            self.company_info.address,
            self.company_info.inn,
            self.company_info.ogrn,
        ):
            self.assertContains(response, value)

    def test_company_content_contains_no_links_buttons_or_carousels(self):
        response = self.client.get(reverse("company"))
        html = response.content.decode()
        main = re.search(r"<main>(.*?)</main>", html, re.DOTALL).group(1)

        self.assertNotRegex(main, r"<a(?:\s|>)")
        self.assertNotRegex(main, r"<button(?:\s|>)")
        self.assertNotIn("carousel", main.lower())
