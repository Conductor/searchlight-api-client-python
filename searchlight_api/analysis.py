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
from .client import AccountService


def search_volume(account_id, date="CURRENT"):
    """Build a search volume data frame for a given date for all tracked searches
    in an account across rank sources and web properties"""
    ss = AccountService(account_id)
    web_properties = [wp for wp in ss.get_web_properties()]
    volumes_list = []
    for wp in web_properties:
        wpid = wp["webPropertyId"]
        rank_sources = [rs["rankSourceId"] for rs in wp["rankSourceInfo"]]
        for rsid in rank_sources:
            msv = ss.get_volume(wpid, rsid, date)
            if not msv:
                continue
            for m in msv:
                m.update({"webPropertyId": wpid, "rankSourceId": rsid})
            volumes_list.extend(msv)
    return volumes_list


def rank_data(account_id, date="CURRENT"):
    """Build a data frame for all ranks in a given date for all tracked searches
    in an account across rank sources and web properties"""
    ss = AccountService(account_id)
    web_properties = [wp for wp in ss.get_web_properties()]
    ranks_list = []
    for wp in web_properties:
        wpid = wp["webPropertyId"]
        rank_sources = [rs["rankSourceId"] for rs in wp["rankSourceInfo"]]
        for rsid in rank_sources:
            ranks = ss.get_ranks(wpid, rsid, date)
            if not ranks:
                continue
            for r in ranks:
                r.update({"rankSourceId": rsid,
                          "standardRank": r["ranks"]["CLASSIC_RANK"],
                          "trueRank": r["ranks"]["TRUE_RANK"]})
                r.pop("ranks", None)
            ranks_list.extend(ranks)
    return ranks_list
