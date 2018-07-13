
from django.test import TestCase


class StaticPagesTest(TestCase):
    """
    Ensure that our projects static URLs contain the content we expect.
    """

    def test_404(self):
        response = self.client.get('/no-such-page/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')
