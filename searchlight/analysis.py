import pandas as pd

from .client import AccountService


def search_volume(account, date="CURRENT", seasonal=False):
    ss = AccountService(account)
    web_properties = [wp for wp in ss.get_web_properties().json() if wp["isActive"]]
    df_list = []
    for wp in web_properties:
        wpid = wp["webPropertyId"]
        searches = ss.get_searches(wpid).json()
        if not searches:
            continue
        rank_sources = [rs["rankSourceId"] for rs in wp["rankSourceInfo"]]
        volumes = []
        for rsid in rank_sources:
            msv = ss.get_volume(wpid, rsid, date).json()
            if not msv:
                continue
            volumes.extend(msv)
        if not volumes:
            continue
        temp = pd.concat(volumes)
        df_list.append(pd.merge(temp, pd.DataFrame(searches), how="left", on="trackedSearchId"))
    if not df_list:
        raise RuntimeError("No volume data found for the given account and date")
    df = pd.concat(df_list)
    df["averageVolume"].fillna(0, inplace=True)
    if seasonal:
        return
    return df.drop("volumeItems", inplace=True, axis=1)


def rank_data(account, date="CURRENT"):
    ss = AccountService(account)
    web_properties = [wp for wp in ss.get_web_properties().json() if wp["isActive"]]
    df_list = []
    for wp in web_properties:
        wpid = wp["webPropertyId"]
        searches = ss.get_searches(wpid).json()
        if not searches:
            continue
        rank_sources = [rs["rankSourceId"] for rs in wp["rankSourceInfo"]]
        rankers = []
        for rsid in rank_sources:
            ranks = ss.get_ranks(wpid, rsid, date).json()
            if not ranks:
                continue
            rankers.extend(ranks)
        if not rankers:
            continue
        temp = pd.concat(rankers)
        df_list.append(pd.merge(temp, pd.DataFrame(searches), how="left", on="trackedSearchId"))
    if not df_list:
        raise RuntimeError("No rank data found for the given account and date")
    df = pd.concat(df_list)
    df[["trueRank", "classicRank"]] = pd.DataFrame(list(df["ranks"]))[["TRUE_RANK", "CLASSIC_RANK"]]
    df["trueRank"].fillna(101, inplace=True)
    df["classicRank"].fillna(101, inplace=True)
    return pd.concat(df_list)
