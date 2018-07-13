
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import unittest

from .common import TestCaseCatalogueData
from catalogue.models import Category, SubCategory


class TestViewsWithoutData(TestCase):
    def setUp(self):
        """
        Delete to any data loaded by an initial data fixture.
        """
        Category.objects.all().delete()
        SubCategory.objects.all().delete()

    def test_index(self):
        url = reverse('catalogue-index')
        response = self.client.get(url)
        self._check_response(response)
        self.assertContains(response, 'No Categories.')

    def _check_response(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalogue/layout/base.html')
        self.assertTemplateUsed(response, 'common/base.html')


class TestViewsWithData(TestCaseCatalogueData):
    def test_category_detail(self):
        url = reverse('catalogue-category-detail',
            kwargs={'slug': 'books', 'pk': 1})
        response = self.client.get(url)
        self._check_response(response)
        self.assertTemplateUsed(response, 'catalogue/category-detail.html')
        self.assertContains(response, 'Books')
        self.assertContains(response, 'Fiction')
        self.assertContains(response, 'Non-Fiction')

    def test_sub_category_detail(self):
        url = reverse('catalogue-sub-category-detail',
            kwargs={'category_slug': 'books', 'slug': 'fiction', 'pk': 1,})
        response = self.client.get(url)
        self._check_response(response)
        self.assertContains(response, 'George R. R. Martin')
        self.assertContains(response, 'A Game of Thrones')
        self.assertContains(response, 'A Clash of Kings')
        self.assertContains(response, 'J. R. R. Tolkien')
        self.assertContains(response, 'The Hobbit')
        self.assertContains(response, 'The Lord of the Rings')

    def test_product_detail(self):
        url = reverse('catalogue-product-detail',
            kwargs={'slug': 'a-game-of-thrones', 'pk': 1})
        response = self.client.get(url)
        self._check_response(response)
        self.assertContains(response, 'A Game of Thrones')


    def _check_response(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalogue/layout/base.html')
        self.assertTemplateUsed(response, 'common/base.html')
