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
import pandas as pd

from .client import AccountService


def tracked_search_df(ss, wpid):
    """Build a data frame from the Tracked Searches endpoint"""
    tracked_searches = ss.get_tracked_searches(wpid).json()
    if not tracked_searches:
        return
    tracked_searches = pd.DataFrame(tracked_searches)
    tracked_searches["trackedSearchId"] = tracked_searches["trackedSearchId"].astype(int)
    return tracked_searches


def monthly_search_volume(msv_df):
    """Change the standard search volume data frame with average search volume to have one row for each month"""
    return pd.concat([pd.DataFrame([dict(item, **{'trackedSearchId': msv_df.trackedSearchId.iloc[i],
                                                  'averageVolume': msv_df.averageVolume.iloc[i]}) for item in
                                    msv_df.volumeItems.iloc[i]]) for i in range(len(msv_df))])


def search_volume(account_id, date="CURRENT", seasonal=False):
    """Build a search volume data frame for a given date for all tracked searches
    in an account across rank sources and web properties"""
    ss = AccountService(account_id)
    web_properties = [wp for wp in ss.get_web_properties().json()]
    df_list = []
    for wp in web_properties:
        wpid = wp["webPropertyId"]
        tracked_searches = tracked_search_df(ss, wpid)
        rank_sources = [rs["rankSourceId"] for rs in wp["rankSourceInfo"]]
        volumes = []
        for rsid in rank_sources:
            msv = ss.get_volume(wpid, rsid, date).json()
            if not msv:
                continue
            volumes.extend(msv)
        if not volumes:
            continue
        temp = pd.DataFrame(volumes)
        if seasonal:
            temp = monthly_search_volume(temp)
        df_list.append(pd.merge(temp, pd.DataFrame(tracked_searches), how="left", on="trackedSearchId"))
    if not df_list:
        raise RuntimeError("No volume data found for the given account and date")
    df = pd.concat(df_list, sort=False)  # type: pd.DataFrame
    df["averageVolume"].fillna(0, inplace=True)
    if "volumeItems" in df.columns:
        df.drop("volumeItems", axis=1, inplace=True)
    return df


def rank_data(account_id, date="CURRENT"):
    """Build a data frame for all ranks in a given date for all tracked searches
    in an account across rank sources and web properties"""
    ss = AccountService(account_id)
    web_properties = [wp for wp in ss.get_web_properties().json()]
    df_list = []
    for wp in web_properties:
        wpid = wp["webPropertyId"]
        tracked_searches = tracked_search_df(ss, wpid)
        rank_sources = [rs["rankSourceId"] for rs in wp["rankSourceInfo"]]
        rankers = []
        for rsid in rank_sources:
            ranks = ss.get_ranks(wpid, rsid, date).json()
            if not ranks:
                continue
            rankers.extend(ranks)
        if not rankers:
            continue
        temp = pd.DataFrame(rankers)
        df_list.append(pd.merge(temp, tracked_searches, how="left", on="trackedSearchId"))
    if not df_list:
        raise RuntimeError("No rank data found for the given account and date")
    df = pd.concat(df_list, sort=False)  # type: pd.DataFrame
    df[["trueRank", "classicRank"]] = pd.DataFrame(list(df["ranks"]))[["TRUE_RANK", "CLASSIC_RANK"]]
    df["trueRank"].fillna(101, inplace=True)
    df["classicRank"].fillna(101, inplace=True)
    return df.drop('ranks', axis=1)
