import unittest
from ..analysis import search_volume, rank_data

class BasicAnalysisTest(unittest.TestCase):
    def test_search_volume(self):

        self.assertEqual(self._ss.get_locations().status_code, 200)
        self.assertEqual(self._ss.get_engines().status_code, 200)
        self.assertEqual(self._ss.get_devices().status_code, 200)


if __name__ == "__main__":
    unittest.main()