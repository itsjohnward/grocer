from unittest import TestCase


# Confirm that tox and pytest are running tests as expected
class TestingSuiteTest(TestCase):
    def test_pytest_config(self):
        self.assertTrue(True)
