"""
Copyright 2019 Conductor, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import hashlib
import os
import sys
import time

import requests

from .utils import week_number


class SearchlightService(object):
    def __init__(self, **kwargs):
        self._api_key = kwargs.get("api_key", os.environ.get("SEARCHLIGHT_API_KEY"))
        assert self._api_key, "Searchlight API key required"
        self._api_secret = kwargs.get("api_secret", os.environ.get("SEARCHLIGHT_SHARED_SECRET"))
        assert self._api_secret, "Searchlight API Secret required"
        self._session = requests.Session()
        self._base_url = "https://searchlight.conductor.com"
        self._v3_url = "{base_url}/v3".format(base_url=self._base_url)

    def _generate_signature(self):
        return hashlib.md5("{key}{secret}{epoch}".format(key=self._api_key, secret=self._api_secret,
                                                         epoch=int(time.time())).encode()).hexdigest()

    def _make_request(self, url, retry=True, verify=True, allow_redirects=True):
        url += "?apiKey={key}&sig={sig}".format(key=self._api_key, sig=self._generate_signature())
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
                print("Status Code: {status_code}. Retrying".format(status_code=res.status_code))
                return self._make_request(url, retry=False)
            else:
                print("{url} failed to respond".format(url=url))
                return
        return res

    # Searchlight Configuration Data

    def get_locations(self):
        """All locations supported by Searchlight"""
        return self._make_request("{v3_url}/locations".format(v3_url=self._v3_url))

    def get_engines(self):
        """Returns all supported engines"""
        return self._make_request("{v3_url}/rank-sources".format(v3_url=self._v3_url))

    def get_devices(self):
        """Returns all supported devices"""
        return self._make_request("{v3_url}/devices".format(v3_url=self._v3_url))

    # Searchlight Account Data

    def get_accounts(self):
        """Returns all available Searchlight accounts"""
        return self._make_request("{v3_url}/accounts".format(v3_url=self._v3_url))

class AccountService(SearchlightService):
    def __init__(self, account_id, **kwargs):
        SearchlightService.__init__(self, **kwargs)
        self.account_id = account_id
    # Account Configuration Data

    def get_web_properties(self):
        """Retrieves account web properties"""
        return self._make_request("{v3_url}/accounts/{acct}/web-properties".format(v3_url=self._v3_url,
                                                                                   acct=self.account_id))

    def get_domain_name(self, wpid):
        """Retrieves the domain name for a given web property"""
        try:
            return next(wp["name"] for wp in self.get_web_properties().json() if wp["webPropertyId"] == str(wpid))
        except StopIteration:
            raise StopIteration("Unable to find web property {wpid}".format(wpid=wpid))

    def get_web_properties_for_domain(self, domain):
        """Retrieves the web property IDs associated with a given domain"""
        wps = [wp["webPropertyId"] for wp in self.get_web_properties().json() if wp["domain"] == domain]
        if not wps:
            raise StopIteration("Unable to find any web properties with domain {domain}".format(domain=domain))
        return wps

    def get_tracked_searches(self, wpid):
        """Gets all searches for a given web property"""
        return self._make_request("{v3_url}/accounts/{account}/web-properties/{wpid}/tracked-searches".format(
            v3_url=self._v3_url, account=self.account_id, wpid=wpid))

    def get_categories(self):
        """Returns categories and their tracked searches"""
        return self._make_request("{v3_url}/accounts/{acct}/categories".format(v3_url=self._v3_url,
                                                                               acct=self.account_id))

    # Collection Data

    def get_ranks(self, wpid, rsid, date="CURRENT"):
        """Gets ranks for searches tracked in a given web property and search engine on a given date"""
        tp = week_number(date) if date != "CURRENT" else date
        return self._make_request("{v3_url}/{acct}/web-properties/{wpid}/rank-sources/{rsid}/tp/{tp}/"
                                  "serp-items".format(v3_url=self._v3_url, acct=self.account_id, wpid=wpid, rsid=rsid,
                                                      tp=tp))

    def get_volume(self, wpid, rsid, date="CURRENT"):
        """Gets volume for searches tracked in a given web property and search engine on the given date"""
        tp = week_number(date) if date != "CURRENT" else date
        return self._make_request("{v3_url}/{acct}/web-properties/{wpid}/rank-sources/{rsid}/tp/{tp}/"
                                  "search-volumes".format(v3_url=self._v3_url, acct=self.account_id, wpid=wpid,
                                                          rsid=rsid, tp=tp))
