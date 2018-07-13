
import datetime

from django.test import TestCase

from catalogue.models import Category, Group, Product, SubCategory


class TestCaseCatalogueData(TestCase):
    """
    Django TestCase that provides a custom setUp() that creates test data.
    """

    def setUp(self):
        # Deal to any data loaded by an initial data fixture
        Category.objects.all().delete()
        SubCategory.objects.all().delete()

        # Categories
        category_books = Category.objects.create(
            name='Books', slug='books')

        # Sub Categories
        sub_category_fiction = SubCategory.objects.create(
            name='Fiction',
            slug='fiction',
            category=category_books)
        sub_category_non_fiction = SubCategory.objects.create(
            name='Non-Fiction',
            slug='non-fiction',
            category=category_books)

        # Product Groups
        group_tolkien = Group.objects.create(
            name="J. R. R. Tolkien",
            slug="tolkien",
            sub_category=sub_category_fiction)

        group_martin = Group.objects.create(
            name="George R. R. Martin",
            slug="martin",
            sub_category=sub_category_fiction)

        # Products
        game_of_thrones = Product.objects.create(
            name='A Game of Thrones',
            slug='a-game-of-thrones',
            sub_category=sub_category_fiction)
        game_of_thrones.group.add(group_martin)

        clash_of_kings = Product.objects.create(
            name='A Clash of Kings',
            slug='a-clash-of-kings',
            sub_category=sub_category_fiction)
        clash_of_kings.group.add(group_martin)

        the_hobbit = Product.objects.create(
            name='The Hobbit',
            slug='the-hobbit',
            sub_category=sub_category_fiction)
        the_hobbit.group.add(group_tolkien)

        the_lotr = Product.objects.create(
            name='The Lord of the Rings',
            slug='the-lord-of-the-rings',
            sub_category=sub_category_fiction)
        the_lotr.group.add(group_tolkien)

        # Add Product Relationships
        the_hobbit.related_products.add(the_lotr)
        the_lotr.related_products.add(the_hobbit)
        the_lotr.related_products.add(game_of_thrones)

        game_of_thrones.related_products.add(clash_of_kings)
        game_of_thrones.related_products.add(the_lotr)
        clash_of_kings.related_products.add(game_of_thrones)

