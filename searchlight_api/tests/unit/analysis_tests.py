import pandas as pd
from unittest import TestCase, main
from unittest.mock import patch


class BasicAnalysisTest(TestCase):
    @patch("searchlight_api.analysis.tracked_search_df")
    def test_tracked_search_df(self, mock_tracked_search_df):
        mock_tracked_search_df.return_value = pd.DataFrame(
            data={"deviceId": [1, 1], "isActive": [True, True], "locationId": [1, 1,], "preferredUrl": [None, None],
                  "queryPhrase": ["sam ash", "music stores"], "rankSourceId": [1, 1],
                  "trackedSearchId": [7188291, 7188297]}
        )
        df = mock_tracked_search_df()
        self.assertIsNotNone(df)
        self.assertIsInstance(df, pd.DataFrame)

    @patch("searchlight_api.analysis.search_volume")
    def test_search_volume(self, mock_search_volume):
        mock_search_volume.return_value = pd.DataFrame(
            data={"deviceId": [1, 1], "isActive": [True, True], "locationId": [1, 1,], "preferredUrl": [None, None],
                  "queryPhrase": ["sam ash", "music stores"], "rankSourceId": [1, 1],
                  "trackedSearchId": [7188291, 7188297], "averageVolume": [0, 1000]}
        )
        df = mock_search_volume(10550, date="CURRENT", seasonal=False)
        self.assertIsNotNone(df)
        self.assertIsInstance(df, pd.DataFrame)

    @patch("searchlight_api.analysis.rank_data")
    def test_rank_data(self, mock_search_volume):
        mock_search_volume.return_value = pd.DataFrame(
            data={"deviceId": [1, 1], "isActive": [True, True], "locationId": [1, 1, ], "preferredUrl": [None, None],
                  "queryPhrase": ["sam ash", "music stores"], "webPropertyId": [43162, None], "target": [None, None],
                  "targetDomainName": ["samash.com", "samash.com"], "trueRank": [1, 7], "classicRank": [1, None],
                  "targetUrl": ["https://www.samash.com", "https://www.samash.com"],
                  "itemType": ["STANDARD_LINK", "IMAGE_RESULT"]}
        )
        df = mock_search_volume(10550, date="CURRENT")
        self.assertIsNotNone(df)
        self.assertIsInstance(df, pd.DataFrame)


if __name__ == "__main__":
    main()
