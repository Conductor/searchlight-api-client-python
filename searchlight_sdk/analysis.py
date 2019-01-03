import datetime

import dateutil
import pandas as pd
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


def get_search_df(ss, wpid):
    """Transforms search response into dataframe"""
    searches = ss.get_searches(wpid).json()
    if not searches:
        return
    searches = pd.DataFrame(searches)
    searches["trackedSearchId"] = searches["trackedSearchId"].astype(int)
    return searches


def get_seasonal_volume(volume_items):
    """Used to get seasonal data from search volume response"""
    month = volume_items.loc[0][0]["month"]
    year = volume_items.loc[0][0]["year"]
    date = datetime.datetime(year, month, 1)
    seasonal_df = volume_items.apply(lambda x: pd.Series([y["volume"] for y in x]))
    seasonal_df.columns = [(date - dateutil.relativedelta(month=i)).strftime("%m-%Y") for i in range(12)]
    return seasonal_df


def search_volume(account, date="CURRENT", seasonal=False):
    """Gets search volume for all the keywords tracked in a given account for a given date"""
    ss = AccountService(account)
    web_properties = [wp for wp in ss.get_web_properties().json()]
    df_list = []
    for wp in web_properties:
        wpid = wp["webPropertyId"]
        searches = get_search_df(ss, wpid)
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
        df_list.append(pd.merge(temp, pd.DataFrame(searches), how="left", on="trackedSearchId"))
    if not df_list:
        raise RuntimeError("No volume data found for the given account and date")
    df = pd.concat(df_list)
    df["averageVolume"].fillna(0, inplace=True)
    if seasonal:
        df = pd.concat([df, get_seasonal_volume(df["volumeItems"])], axis=1)
    return df.drop("volumeItems", axis=1)


def rank_data(account, date="CURRENT"):
    """Gets owned ranks for keywords tracked in a given account for a given date"""
    ss = AccountService(account)
    web_properties = [wp for wp in ss.get_web_properties().json()]
    df_list = []
    for wp in web_properties:
        wpid = wp["webPropertyId"]
        searches = get_search_df(ss, wpid)
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
        df_list.append(pd.merge(temp, searches, how="left", on="trackedSearchId"))
    if not df_list:
        raise RuntimeError("No rank data found for the given account and date")
    df = pd.concat(df_list)
    df[["trueRank", "classicRank"]] = pd.DataFrame(list(df["ranks"]))[["TRUE_RANK", "CLASSIC_RANK"]]
    df["trueRank"].fillna(101, inplace=True)
    df["classicRank"].fillna(101, inplace=True)
    return pd.concat(df_list)
