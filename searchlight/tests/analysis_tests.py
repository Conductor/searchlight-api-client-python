import os
import pandas as pd
from pandas.util.testing import assert_frame_equal
import unittest

from ..analysis import search_volume, rank_data


class BasicAnalysisTest(unittest.TestCase):
    def test_search_volume(self):
        df = search_volume(10550, "10-03-2018")
        self.assertIsNotNone(df)
        data_path = os.path.join(os.path.dirname(__file__), "data/search_volume_sample.csv")
        df["deviceId"] = df["deviceId"].astype(int)
        df["rankSourceId"] = df["rankSourceId"].astype(int)
        df["locationId"] = df["locationId"].astype(int)
        assert_frame_equal(df, pd.read_csv(data_path))

    def test_ranks(self):
        df = rank_data(10550, "10-03-2018")
        self.assertIsNotNone(df)


if __name__ == "__main__":
    unittest.main()
