import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.categories.models import Category

from .models import Product


TEST_MEDIA_ROOT = tempfile.mkdtemp()
TEST_IMAGE = (
    b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00"
    b"\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,\x00"
    b"\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
)


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class ProductCatalogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.categories = [
            Category.objects.create(
                name=f"Категория {index}",
                slug=f"category-{index}",
                sort_order=index,
            )
            for index in range(1, 7)
        ]
        cls.inactive_category = Category.objects.create(
            name="Скрытая категория",
            slug="inactive-category",
            sort_order=0,
            is_active=False,
        )
        cls.product = Product.objects.create(
            category=cls.categories[0],
            name="Тестовый продукт",
            slug="test-product",
            image=SimpleUploadedFile("test-product.gif", TEST_IMAGE),
            description="Описание продукта",
            ingredients="Состав продукта",
            price="250.00",
            weight="180 г",
            shelf_life="72 часа",
            storage_temperature="от +2 до +4 °C",
            is_new=True,
            is_popular=True,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEST_MEDIA_ROOT, ignore_errors=True)

    def test_catalog_splits_active_categories_after_first_four(self):
        response = self.client.get(reverse("products"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["featured_categories"]),
            self.categories[:4],
        )
        self.assertEqual(
            list(response.context["remaining_categories"]),
            self.categories[4:],
        )
        self.assertNotContains(response, self.inactive_category.name)
        self.assertTemplateUsed(response, "sections/spiral_curve.html")

    def test_category_page_uses_product_card_and_product_link(self):
        response = self.client.get(
            reverse("category_detail", args=[self.categories[0].slug]),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
        self.assertContains(
            response,
            reverse("product_detail", args=[self.product.slug]),
        )
        self.assertTemplateUsed(response, "components/product_card.html")

    def test_inactive_category_and_its_product_are_not_public(self):
        hidden_product = Product.objects.create(
            category=self.inactive_category,
            name="Скрытый продукт",
            slug="hidden-product",
            image=SimpleUploadedFile("hidden-product.gif", TEST_IMAGE),
            price="100.00",
        )

        category_response = self.client.get(
            reverse("category_detail", args=[self.inactive_category.slug]),
        )
        product_response = self.client.get(
            reverse("product_detail", args=[hidden_product.slug]),
        )

        self.assertEqual(category_response.status_code, 404)
        self.assertEqual(product_response.status_code, 404)

    def test_product_page_shows_real_product_fields(self):
        response = self.client.get(
            reverse("product_detail", args=[self.product.slug]),
        )

        self.assertEqual(response.status_code, 200)
        for value in (
            self.product.name,
            self.product.description,
            self.product.ingredients,
            self.product.weight,
            self.product.shelf_life,
            self.product.storage_temperature,
            self.product.category.name,
            "Новинка",
            "Популярный товар",
        ):
            self.assertContains(response, value)

    def test_home_featured_product_card_links_to_product_page(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            reverse("product_detail", args=[self.product.slug]),
        )
        self.assertTemplateUsed(response, "components/product_card.html")
        self.assertTemplateUsed(response, "sections/spiral_curve.html")
