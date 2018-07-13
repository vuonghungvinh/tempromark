
import io
import os

from django.utils.unittest import TestCase

from animal3 import iso_3166


class TestISO_3166(TestCase):
    """
    Country lists match data file, and are internally consistent.
    """

    # Read in the only freely available source file from ISO for validation:
    # [['AFGHANISTAN', 'AF'], ['ALBANIA', 'AL'], ['ALGERIA', 'DZ'], ...
    iso_3166_alpha2 = [
        line.split(';') for line in [line.strip() for line in
            io.open(os.path.join(os.path.dirname(__file__),
                'iso_3166_alpha2.txt'), 'rt', encoding='utf-8')]
        if line and not line.startswith('#')
    ]
    num_countries = len(iso_3166_alpha2)

    def test_number_of_countries(self):
        "Correct number of countries in all lists"
        self.assertEqual(self.num_countries, len(iso_3166.ALPHA_2))
        self.assertEqual(self.num_countries, len(iso_3166.ALPHA_3))
        self.assertEqual(self.num_countries, len(iso_3166.NUMERIC))

    def test_alpha2_codes(self):
        "Our alpha2 code list should match the official ISO provided one"
        our_codes = [x[0] for x in iso_3166.ALPHA_2]
        iso_codes = [x[1] for x in self.iso_3166_alpha2]
        self.assertEqual(our_codes, iso_codes)

    def test_alpha2_names(self):
        "Our alpha2 code list should match the official ISO provided one"
        our_names = [x[1].lower() for x in iso_3166.ALPHA_2]
        iso_names = [x[0].lower() for x in self.iso_3166_alpha2]
        self.assertEqual(our_names, iso_names)

    def test_keys_unique(self):
        "Keys are unique"
        alpha2 = set(k for (k,v) in iso_3166.ALPHA_2)
        alpha3 = set(k for (k,v) in iso_3166.ALPHA_3)
        numeric = set(k for (k,v) in iso_3166.NUMERIC)
        self.assertEqual(self.num_countries, len(alpha2))
        self.assertEqual(self.num_countries, len(alpha3))
        self.assertEqual(self.num_countries, len(numeric))

    def test_country_names(self):
        "Identical names across all three lists"
        alpha2 = set(v for (k,v) in iso_3166.ALPHA_2)
        alpha3 = set(v for (k,v) in iso_3166.ALPHA_3)
        numeric = set(v for (k,v) in iso_3166.NUMERIC)
        self.assertEqual(alpha2, alpha3)
        self.assertEqual(alpha2, numeric)
        self.assertEqual(alpha3, numeric)

    def test_ordering(self):
        "Ordering is identical across all three lists"
        alpha2 = [v for (k,v) in iso_3166.ALPHA_2]
        alpha3 = [v for (k,v) in iso_3166.ALPHA_3]
        numeric = [v for (k,v) in iso_3166.NUMERIC]
        self.assertEqual(alpha2, alpha3)
        self.assertEqual(alpha2, numeric)
        self.assertEqual(alpha3, numeric)

