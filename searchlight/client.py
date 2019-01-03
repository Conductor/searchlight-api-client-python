import hashlib
import os
import requests
import sys
import time
from .utils import week_number


class SearchlightService(object):
    def __init__(self, account_id, **kwargs):
        self.account_id = account_id
        self._api_key = kwargs.get("api_key", os.environ.get("SEARCHLIGHT_API_KEY"))
        assert self._api_key, "Searchlight API key required"
        self._api_secret = kwargs.get("api_secret", os.environ.get("SEARCHLIGHT_SHARED_SECRET"))
        assert self._api_secret, "Searchlight API Secret required"
        self._session = requests.Session()
        self._base_url = "https://searchlight.conductor.com"
        self._api_url = "{base_url}/api".format(base_url=self._base_url)
        self._v3_url = "{base_url}/v3".format(base_url=self._base_url)

    def _generate_signature(self):
        return hashlib.md5("{key}{secret}{epoch}".format(key=self._api_key, secret=self._api_secret,
                                                         epoch=int(time.time()))).hexdigest()

    def _make_request(self, url, retry=True, verify=True, allow_redirects=True):
        time.sleep(0.501)
        url += "?apiKey={key}}&sig={sig}".format(key=self._api_key, sig=self._generate_signature())
        try:
            res = self._session.get(url, verify=verify, allow_redirects=allow_redirects)
        except (ConnectionRefusedError, ConnectionResetError, ConnectionAbortedError) as e:
            print("Error connecting to Searchlight : {error}".format(error=e))
            return
        except requests.exceptions.ChunkedEncodingError:
            print("Searchlight response delayed, skipping retrieval..: {info}".format(info=sys.exc_info()[0]))
            return
        if res.raise_for_status():
            if retry:
                print("Status Code: {status}. Retrying", res.status_code)
                return self._make_request(url, retry=False)
            else:
                print("{url} failed to respond".format(url=url))
                return
        return res

    # Configuration Data

    def get_account_overview(self):
        """Retrieves account metadata"""
        return self._make_request("{api_url}/accounts/{acct}".format(api_url=self._api_url,
                                                                     acct=self.account_id))

    def get_web_properties(self):
        """Retrieves account web properties"""
        return self._make_request("{v3_url}/accounts/{acct}/web-properties".format(v3_url=self._v3_url,
                                                                                   acct=self.account_id))

    def get_domain_name(self, wpid):
        """Retrieves the domain name for a given web property"""
        return next(wp["name"] for wp in self.get_web_properties().json() if wp["webPropertyId"] == wpid)

    def get_web_properties_for_domain(self, domain):
        """Retrieves the web property IDs associated with a given domain"""
        return [wp["webPropertyId"] for wp in self.get_web_properties().json() if wp["domain"] == domain]

    def get_searches(self, wpid):
        """Gets all searches for a given web property"""
        return self._make_request("{v3_url}/accounts/{account}/web-properties/{wpid}/tracked-searches".format(
            v3_url=self._v3_url, account=self.account_id, wpid=wpid))

    def get_categories(self):
        """Returns an account's categories and their rules"""
        return self._make_request("{api_url}/{acct}/categories".format(api_url=self._api_url,
                                                                       acct=self.account_id))

    def get_keywords_by_category(self):
        """Returns categories and their tracked searches"""
        return self._make_request("{v3_url}/accounts/{acct}/categories".format(v3_url=self._v3_url,
                                                                                  acct=self.account_id))

    def get_segments(self, wpid, rsid):
        """Returns the content segments and their rules for a given web property and search engine"""
        return self._make_request("{v3_url}/accounts/{acct}/web-properties/{wpid}/rank-source/{rsid}/"
                                  "content-segments".format(v3_url=self._v3_url, acct=self.account_id, wpid=wpid,
                                                            rsid=rsid))

    def get_analytics_segments(self, wpid, rsid):
        """Returns segment IDs for analytics"""
        return self._make_request("{v3_url}/accounts/{acct}/web-properties/{wpid}/rank-source/{rsid}/segments".format(
            v3_url=self._v3_url, acct=self.account_id, wpid=wpid, rsid=rsid))

    # Collection Data

    def get_ranks(self, wpid, rsid, date="CURRENT"):
        """Gets ranks for searches tracked in a given web property and search engine on a given date"""
        tp = week_number(date) if date != "CURRENT" else date
        return self._make_request("{v3_url}/{acct}/web-properties/{wpid}/rank-source/{rsid}/tp/{tp}/"
                                  "serp-items".format(v3_url=self._v3_url, acct=self.account_id, wpid=wpid, rsid=rsid,
                                                      tp=tp))

    def get_volume(self, wpid, rsid, date="CURRENT"):
        """Gets volume for searches tracked in a given web property and search engine on the given date"""
        tp = week_number(date) if date != "CURRENT" else date
        return self._make_request("{v3_url}/{acct}/web-properties/{wpid}/rank-source/{rsid}/tp/{tp}/"
                                  "search-volume".format(v3_url=self._v3_url, acct=self.account_id, wpid=wpid,
                                                         rsid=rsid, tp=tp))

    def get_analytics(self, wpid, rsid, date="CURRENT"):
        """Gets volume for searches tracked in a given web property and search engine on the given date"""
        tp = week_number(date) if date != "CURRENT" else date
        return self._make_request("{v3_url}/{acct}/web-properties/{wpid}/rank-source/{rsid}/tp/{tp}/"
                                  "analytics-urls".format(v3_url=self._v3_url, acct=self.account_id, wpid=wpid,
                                                          rsid=rsid, tp=tp))
