
from django import template
from django.utils.unittest import skip, TestCase

from animal3.templatetags import google


class GoogleAnalyticsTest(TestCase):
    def test_google_analytics(self):
        "Tag should expand into correct JavaScript snippet"
        text = (
            '{% load google %}'
            '{% google_analytics "XXXX" %}'
        )
        t = template.Template(text)
        output = t.render(template.Context())
        self.assertIn("_gaq.push(['_setAccount', 'XXXX']);", output)


class SnippetTest(TestCase):
    def test_context(self):
        "Snippet should update context"
        text = (
            "{% load animal3_builtins %}"
            "{% snippet %}"
            "Hairy MacClary"
            "{% endsnippet %}"
        )
        t = template.Template(text)
        c = template.Context()

        self.assertFalse('snippet' in c)
        output = t.render(c)

        self.assertEqual(output, '')
        self.assertTrue('snippet' in c)
        self.assertEqual(c['snippet'], 'Hairy MacClary')

    def test_rename_context(self):
        "Snippet context variable can be renamed"
        text = (
            "{% load animal3_builtins %}"
            "{% snippet as copy_me %}"
            "Hairy MacClary"
            "{% endsnippet %}"
        )
        t = template.Template(text)
        c = template.Context()

        self.assertFalse('copy_me' in c)
        output = t.render(c)

        self.assertEqual(output, '')
        self.assertTrue('copy_me' in c)
        self.assertEqual(c['copy_me'], 'Hairy MacClary')

    def test_bad_syntax(self):
        text = (
            "{% load animal3_builtins %}"
            "{% snippet apple apple apple %}"
            "Hairy MacClary"
            "{% endsnippet %}"
        )
        with self.assertRaisesRegexp(
            template.TemplateSyntaxError, 'snippet tag has invalid arguments'):
            t = template.Template(text)
