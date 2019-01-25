from unittest import TestCase

from searchlight_sdk.utils import week_number


class BasicAnalysisTest(TestCase):
    def test_week_number(self):
        number = week_number("2018-04-12")
        self.assertEqual(number, 455)
