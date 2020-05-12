from unittest import TestCase

from .utils import str_utils


# Confirm that tox and pytest are running tests as expected
class TestingSuiteTest(TestCase):
    def test_pytest_config(self):
        self.assertTrue(True)


class StringUtilsTests(TestCase):
    def test_is_date(self):
        self.assertTrue(str_utils.is_date("Monday"))
        self.assertTrue(str_utils.is_date("Tuesday"))
        self.assertTrue(str_utils.is_date("Wednesday"))
        self.assertFalse(str_utils.is_date("February"))
        self.assertFalse(str_utils.is_date(1))
        self.assertFalse(str_utils.is_date(None))
        self.assertFalse(str_utils.is_date(True))

    def test_is_time(self):
        self.assertTrue(str_utils.is_time("12am - 4pm"))
        self.assertTrue(str_utils.is_time("12am - 2am"))
        self.assertTrue(str_utils.is_time("12pm - 2pm"))
        self.assertFalse(str_utils.is_time("12am"))
        self.assertFalse(str_utils.is_time(11))
        self.assertFalse(str_utils.is_time(False))
        self.assertFalse(str_utils.is_time(None))

    def test_is_money(self):
        self.assertTrue(str_utils.is_money("$14"))
        self.assertTrue(str_utils.is_money("$14.00"))
        self.assertFalse(str_utils.is_money("14"))
        self.assertFalse(str_utils.is_money(14))
        self.assertFalse(str_utils.is_money(False))
        self.assertFalse(str_utils.is_money(None))
