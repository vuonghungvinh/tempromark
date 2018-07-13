
import textwrap

from django import template
from django.utils import safestring
from django.utils.unittest import skip, TestCase

from animal3.templatetags.animal3_builtins import currency, email, entities


def render(t, c):
    "Utility function to render given string with dictionary context"
    t = template.Template(t)
    c = template.Context(c)
    output = t.render(c)
    return output.strip()


class TestCurrencyFilter(TestCase):
    def test_currency(self):
        "Currency filter works in isolation"
        # Numeric argument, note rounding
        self.assertEqual(currency(.125), '$0.12')
        self.assertEqual(currency(.126), '$0.13')
        self.assertEqual(currency(1.5), '$1.50')
        self.assertEqual(currency(10), '$10.00')
        self.assertEqual(currency(1e9), '$1,000,000,000.00')

        # Override prefix
        self.assertEqual(currency(15, 'NZD$'), 'NZD$15.00')
        self.assertEqual(currency(1500, ''), '1,500.00')

        # Invalid input
        self.assertEqual(currency('sausage'), '')
        self.assertEqual(currency(None), '')
        self.assertEqual(currency(dict()), '')

        # Boolean suprise!  Recall than boolean types are subclass of int
        self.assertEqual(currency(False), '$0.00')
        self.assertEqual(currency(True), '$1.00')

    def test_currency_integration(self):
        "Currency filter work correctly when integrated into templates"
        c = {
            'coffee': 3.5,
            'house': 550e3,
            'weekday': 'Wednesday',
        }
        t = textwrap.dedent("""
            {% load animal3_builtins %}
            {{ coffee|currency }}
            {{ weekday|currency }}
            {{ house|currency }}
        """).strip()

        expected = textwrap.dedent("""
            $3.50

            $550,000.00
        """).strip()

        output = render(t, c)
        self.assertMultiLineEqual(output, expected)


class TestEmailFilter(TestCase):
    def test_email(self):
        self.assertEqual(email('leon@example.net'),
            '<a href="&#x6d;&#x61;&#x69;&#x6c;&#x74;&#x6f;&#x3a;&#x6c;'
            '&#x65;&#x6f;&#x6e;&#x40;&#x65;&#x78;&#x61;&#x6d;&#x70;&#x6c;'
            '&#x65;&#x2e;&#x6e;&#x65;&#x74;">&#x6c;&#x65;&#x6f;&#x6e;&#x40;'
            '&#x65;&#x78;&#x61;&#x6d;&#x70;&#x6c;&#x65;&#x2e;&#x6e;'
            '&#x65;&#x74;</a>')

    def test_email_integration(self):
        c = {
            'address': 'leon@example.net',
            'unsafe': '<script>',
        }
        t = textwrap.dedent("""
            {% load animal3_builtins %}

            {{ address }}
            {{ address|email }}

            {{ unsafe }}
            {{ unsafe|email }}

            {% autoescape off %}
            {{ address }}
            {{ address|email }}

            {{ unsafe }}
            {% endautoescape %}
            """).strip()
        expected = textwrap.dedent("""
            leon@example.net
            <a href="&#x6d;&#x61;&#x69;&#x6c;&#x74;&#x6f;&#x3a;&#x6c;&#x65;&#x6f;&#x6e;&#x40;&#x65;&#x78;&#x61;&#x6d;&#x70;&#x6c;&#x65;&#x2e;&#x6e;&#x65;&#x74;">&#x6c;&#x65;&#x6f;&#x6e;&#x40;&#x65;&#x78;&#x61;&#x6d;&#x70;&#x6c;&#x65;&#x2e;&#x6e;&#x65;&#x74;</a>

            &lt;script&gt;
            <a href="&#x6d;&#x61;&#x69;&#x6c;&#x74;&#x6f;&#x3a;&#x26;&#x6c;&#x74;&#x3b;&#x73;&#x63;&#x72;&#x69;&#x70;&#x74;&#x26;&#x67;&#x74;&#x3b;">&#x26;&#x6c;&#x74;&#x3b;&#x73;&#x63;&#x72;&#x69;&#x70;&#x74;&#x26;&#x67;&#x74;&#x3b;</a>


            leon@example.net
            <a href="&#x6d;&#x61;&#x69;&#x6c;&#x74;&#x6f;&#x3a;&#x6c;&#x65;&#x6f;&#x6e;&#x40;&#x65;&#x78;&#x61;&#x6d;&#x70;&#x6c;&#x65;&#x2e;&#x6e;&#x65;&#x74;">&#x6c;&#x65;&#x6f;&#x6e;&#x40;&#x65;&#x78;&#x61;&#x6d;&#x70;&#x6c;&#x65;&#x2e;&#x6e;&#x65;&#x74;</a>

            <script>
            """).strip()
        output = render(t, c)
        self.maxDiff = None
        self.assertMultiLineEqual(output, expected)


class TestEntitiesFilter(TestCase):
    def test_entities(self):
        self.assertEqual(entities('Leon'), '&#x4c;&#x65;&#x6f;&#x6e;')
        self.assertEqual(entities(42), '&#x34;&#x32;')                  # '42'
        self.assertEqual(entities(1.7), '&#x31;&#x2e;&#x37;')           # '1.7'
        self.assertEqual(entities(None), '&#x4e;&#x6f;&#x6e;&#x65;')    # 'None'
        self.assertEqual(entities(True), '&#x54;&#x72;&#x75;&#x65;')    # 'True'
        self.assertEqual(entities(False), '&#x46;&#x61;&#x6c;&#x73;&#x65;')
        self.assertEqual(entities(dict()), '&#x7b;&#x7d;')
        self.assertEqual(entities(list()), '&#x5b;&#x5d;')
        self.assertEqual(entities(tuple()), '&#x28;&#x29;')

    def test_entities_integration(self):
        "Entities filter work correctly when integrated into templates"
        c = {
            'name': 'Leon',
            'unsafe': '<script>',
        }
        t = textwrap.dedent("""
            {% load animal3_builtins %}

            {{ name }}
            {{ name|entities }}

            {{ unsafe }}
            {{ unsafe|entities }}

            {% autoescape off %}
            {{ name }}
            {{ name|entities }}

            {{ unsafe }}
            {{ unsafe|entities }}
            {% endautoescape %}
        """).strip()

        expected = textwrap.dedent("""
            Leon
            &#x4c;&#x65;&#x6f;&#x6e;

            &lt;script&gt;
            &#x26;&#x6c;&#x74;&#x3b;&#x73;&#x63;&#x72;&#x69;&#x70;&#x74;&#x26;&#x67;&#x74;&#x3b;


            Leon
            &#x4c;&#x65;&#x6f;&#x6e;

            <script>
            &#x3c;&#x73;&#x63;&#x72;&#x69;&#x70;&#x74;&#x3e;
        """).strip()
        output = render(t, c)
        self.assertMultiLineEqual(output, expected)
