from __future__ import unicode_literals

import unittest

from decimal import Decimal

from djmoney_rates.backends import BaseRateBackend
from djmoney_rates.exceptions import CurrencyConversionException
from djmoney_rates.models import RateSource, Rate
from djmoney_rates.settings import money_rates_settings
from djmoney_rates.utils import convert_money


class TestMoneyConverter(unittest.TestCase):
    def setUp(self):
        class RateBackend(BaseRateBackend):
            source_name = "fake-backend"
            base_currency = "USD"

        money_rates_settings.DEFAULT_BACKEND = RateBackend

    def tearDown(self):
        RateSource.objects.all().delete()
        Rate.objects.all().delete()

    def test_conversion_fail_when_source_does_not_exist(self):
        with self.assertRaises(CurrencyConversionException) as cm:
            convert_money(10.0, "PLN", "EUR")

        self.assertIn("Rate for fake-backend source do not exists", str(cm.exception))

    def test_conversion_fail_when_currency_from_does_not_exist(self):
        RateSource.objects.create(name="fake-backend")

        with self.assertRaises(CurrencyConversionException) as cm:
            convert_money(10.0, "PLN", "EUR")

        self.assertIn("Rate for PLN in fake-backend do not exists", str(cm.exception))

    def test_conversion_fail_when_currency_to_does_not_exist(self):
        source = RateSource.objects.create(name="fake-backend")
        Rate.objects.create(source=source, currency="PLN", value=0.99999)

        with self.assertRaises(CurrencyConversionException) as cm:
            convert_money(10.0, "PLN", "EUR")

        self.assertIn("Rate for EUR in fake-backend do not exists", str(cm.exception))

    def test_conversion_works_from_base_currency(self):
        source = RateSource.objects.create(name="fake-backend", base_currency="USD")
        Rate.objects.create(source=source, currency="USD", value=1)
        Rate.objects.create(source=source, currency="EUR", value=0.74)

        amount = convert_money(1, "USD", "EUR")
        self.assertEqual(amount, Decimal("0.74"))

    def test_conversion_is_working_from_other_currency(self):
        source = RateSource.objects.create(name="fake-backend", base_currency="USD")
        Rate.objects.create(source=source, currency="PLN", value=3.07)
        Rate.objects.create(source=source, currency="EUR", value=0.74)

        amount = convert_money(10.0, "PLN", "EUR")
        self.assertEqual(amount, Decimal("2.41"))

    def test_conversion_fail_when_source_does_not_exist(self):
        with self.assertRaises(CurrencyConversionException) as cm:
            convert_money(10.0, "PLN", "EUR")

        self.assertIn("Rate for fake-backend source do not exists", str(cm.exception))

    def test_conversion_fail_when_currency_from_does_not_exist(self):
        RateSource.objects.create(name="fake-backend")

        with self.assertRaises(CurrencyConversionException) as cm:
            convert_money(10.0, "PLN", "EUR")

        self.assertIn("Rate for PLN in fake-backend do not exists", str(cm.exception))

    def test_conversion_fail_when_currency_to_does_not_exist(self):
        source = RateSource.objects.create(name="fake-backend")
        Rate.objects.create(source=source, currency="PLN", value=0.99999)

        with self.assertRaises(CurrencyConversionException) as cm:
            convert_money(10.0, "PLN", "EUR")

        self.assertIn("Rate for EUR in fake-backend do not exists", str(cm.exception))
