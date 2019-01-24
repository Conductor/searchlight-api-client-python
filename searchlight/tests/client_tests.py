from unittest import TestCase, main
from unittest.mock import Mock, patch

from searchlight.client import AccountService


class BasicClientTest(TestCase):
    
    @patch("searchlight.client.requests.get")
    def test_get_locations(self, mock_get):
        self._ss = AccountService(10550)
        mock_get.return_value.ok = True
        res = self._ss.get_locations()
        self.assertIsNotNone(res)
    # def test_searchlight_config(self):
    #     self._ss = AccountService(10550)
    #     self.assertEqual(self._ss.get_locations().status_code, 200)
    #     self.assertEqual(self._ss.get_engines().status_code, 200)
    #     self.assertEqual(self._ss.get_devices().status_code, 200)
    #
    # def test_account_config(self):
    #     self._ss = AccountService(10550)
    #     self.assertEqual(self._ss.get_domain_name(43162), "samash.com")
    #     res = self._ss.get_tracked_searches(43162)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertNotEquals(len(res.json()), 0)
    #     res = self._ss.get_categories()
    #     self.assertEqual(res.status_code, 200)
    #     self.assertNotEquals(len(res.json()), 0)
    #
    # def test_data(self):
    #     self._ss = AccountService(10550)
    #     res = self._ss.get_volume(43162, 1)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertNotEquals(len(res.json()), 0)
    #     res = self._ss.get_ranks(43162, 1)
    #     self.assertEqual(res.status_code, 200)
    #     self.assertNotEquals(len(res.json()), 0)


if __name__ == "__main__":
    main()
