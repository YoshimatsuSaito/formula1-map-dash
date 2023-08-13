import datetime
from collections import defaultdict

import numpy as np
import pandas as pd
from ergast_py import Ergast
from tqdm import tqdm


LIST_COL_X = [
    "recent_position",
    "recent_race_diff_sec",
    "recent_q1_percent",
    "recent_q2_percent",
    "recent_q3_percent",
    "recent_position_std",
    "recent_race_diff_sec_std",
    "recent_q1_percent_std",
    "recent_q2_percent_std",
    "recent_q3_percent_std",
    "season_position",
    "season_race_diff_sec",
    "season_q1_percent",
    "season_q2_percent",
    "season_q3_percent",
    "recent_position_constructor",
    "recent_race_diff_sec_constructor",
    "recent_q1_percent_constructor",
    "recent_q2_percent_constructor",
    "recent_q3_percent_constructor",
    "recent_position_std_constructor",
    "recent_race_diff_sec_std_constructor",
    "recent_q1_percent_std_constructor",
    "recent_q2_percent_std_constructor",
    "recent_q3_percent_std_constructor",
    "season_position_constructor",
    "season_race_diff_sec_constructor",
    "season_q1_percent_constructor",
    "season_q2_percent_constructor",
    "season_q3_percent_constructor",
    "prev_position",
    "round",
]
LIST_COL_y = ["y"]
LIST_COL_IDENTIFIER = ["year", "driver", "constructor", "grandprix"]


def cvt_datetime_to_sec(datetime):
    """Convert datetime to sec"""
    if datetime is None:
        return datetime
    return (
        datetime.hour * 3600
        + datetime.minute * 60
        + datetime.second
        + datetime.microsecond * 1e-6
    )


def retrieve_data_to_bypass_error(
    dict_res_race, dict_res_quali, season, n_round, grandprix
):
    """Get result by an inefficient way to bypass error of ergast"""
    list_driver = [
        x.driver_id for x in Ergast().season(season).round(n_round).get_drivers()
    ]

    # Loop for driver
    for driver in list_driver:
        # Basic info
        dict_res_race["year"].append(season)
        dict_res_race["grandprix"].append(grandprix)
        dict_res_race["driver"].append(driver)
        dict_res_race["round"].append(n_round)

        dict_res_quali["year"].append(season)
        dict_res_quali["grandprix"].append(grandprix)
        dict_res_quali["driver"].append(driver)
        dict_res_quali["round"].append(n_round)

        # Quali
        res_quali = (
            Ergast()
            .season(season)
            .round(n_round)
            .driver(driver)
            .get_qualifying()
            .qualifying_results[0]
        )
        dict_res_quali["q1_sec"].append(cvt_datetime_to_sec(res_quali.qual_1))
        dict_res_quali["q2_sec"].append(cvt_datetime_to_sec(res_quali.qual_2))
        dict_res_quali["q3_sec"].append(cvt_datetime_to_sec(res_quali.qual_3))
        dict_res_quali["constructor"].append(res_quali.constructor.constructor_id)

        # Race
        if Ergast().season(season).round(n_round).driver(
            driver
        ).get_status().status in ["Finished"] + [f"+{x} Lap" for x in range(1, 10)]:
            res_race = (
                Ergast()
                .season(season)
                .round(n_round)
                .driver(driver)
                .get_result()
                .results[0]
            )
            dict_res_race["race_sec"].append(cvt_datetime_to_sec(res_race.time))
            dict_res_race["position"].append(res_race.position)
            dict_res_race["constructor"].append(res_race.constructor.constructor_id)
        else:
            dict_res_race["race_sec"].append(None)
            dict_res_race["position"].append(len(list_driver))
            dict_res_race["constructor"].append(res_quali.constructor.constructor_id)
    return dict_res_race, dict_res_quali


def retrieve_data_for_inference(current_season):
    """Get result of target season and previous season of that"""
    # dict to store data
    dict_res_race = {
        "position": [],
        "year": [],
        "round": [],
        "grandprix": [],
        "driver": [],
        "constructor": [],
        "race_sec": [],
    }

    dict_res_quali = {
        "year": [],
        "round": [],
        "grandprix": [],
        "driver": [],
        "constructor": [],
        "q1_sec": [],
        "q2_sec": [],
        "q3_sec": [],
    }

    # Use data of this year and previous year
    list_season = [current_season - 1, current_season]

    # Loop for season
    for season in list_season:
        list_races = Ergast().season(season).get_races()

        list_driver = [x.driver_id for x in Ergast().season(season).get_drivers()]
        list_constructor = [
            Ergast().season(season).driver(x).get_constructor().constructor_id
            for x in list_driver
        ]

        # Loop for race
        for race in tqdm(list_races):
            grandprix = race.race_name
            n_round = race.round_no
            print(f"Collect data of round {n_round}: {grandprix} of {season}")

            # If the race is future, store dummy data in dict
            if race.date > datetime.datetime.now(datetime.timezone.utc):
                dict_res_race["year"] += [season] * len(list_driver)
                dict_res_race["grandprix"] += [grandprix] * len(list_driver)
                dict_res_race["round"] += [n_round] * len(list_driver)
                dict_res_race["driver"] += list_driver
                dict_res_race["constructor"] += list_constructor
                dict_res_race["race_sec"] += [None] * len(list_driver)
                dict_res_race["position"] += [None] * len(list_driver)

                dict_res_quali["year"] += [season] * len(list_driver)
                dict_res_quali["grandprix"] += [grandprix] * len(list_driver)
                dict_res_quali["round"] += [n_round] * len(list_driver)
                dict_res_quali["driver"] += list_driver
                dict_res_quali["constructor"] += list_constructor
                dict_res_quali["q1_sec"] += [None] * len(list_driver)
                dict_res_quali["q2_sec"] += [None] * len(list_driver)
                dict_res_quali["q3_sec"] += [None] * len(list_driver)

            else:
                try:
                    list_res_race = (
                        Ergast().season(season).round(n_round).get_results()[0].results
                    )
                    list_res_quali = (
                        Ergast()
                        .season(season)
                        .round(n_round)
                        .get_qualifyings()[0]
                        .qualifying_results
                    )

                    # Loop for race result for each driver
                    for res_race in list_res_race:
                        # Basic info
                        dict_res_race["year"].append(season)
                        dict_res_race["grandprix"].append(grandprix)
                        dict_res_race["round"].append(n_round)
                        dict_res_race["driver"].append(res_race.driver.driver_id)
                        dict_res_race["constructor"].append(
                            res_race.constructor.constructor_id
                        )
                        # Result
                        dict_res_race["race_sec"].append(
                            cvt_datetime_to_sec(res_race.time)
                        )
                        dict_res_race["position"].append(res_race.position)

                    # Loop for quali result for each driver
                    for res_quali in list_res_quali:
                        # Basic info
                        dict_res_quali["year"].append(season)
                        dict_res_quali["grandprix"].append(grandprix)
                        dict_res_quali["round"].append(n_round)
                        dict_res_quali["driver"].append(res_quali.driver.driver_id)
                        dict_res_quali["constructor"].append(
                            res_quali.constructor.constructor_id
                        )
                        # Result
                        dict_res_quali["q1_sec"].append(
                            cvt_datetime_to_sec(res_quali.qual_1)
                        )
                        dict_res_quali["q2_sec"].append(
                            cvt_datetime_to_sec(res_quali.qual_2)
                        )
                        dict_res_quali["q3_sec"].append(
                            cvt_datetime_to_sec(res_quali.qual_3)
                        )
                except:
                    dict_res_race, dict_res_quali = retrieve_data_to_bypass_error(
                        dict_res_race, dict_res_quali, season, n_round, grandprix
                    )

    df_res_race = pd.DataFrame(dict_res_race)
    df_res_quali = pd.DataFrame(dict_res_quali)

    df = pd.merge(
        df_res_race,
        df_res_quali,
        on=["year", "round", "driver", "constructor", "grandprix"],
        how="left",
    )
    df = df.sort_values(by=["year", "round", "driver"]).reset_index(drop=True)
    return df


def transform_data(df):
    """Create processed data"""
    list_df = []
    for year in tqdm(df["year"].unique()):
        df_season = df.loc[df["year"] == year].copy()
        for round in df_season["round"].unique():
            df_round = df_season.loc[df_season["round"] == round].copy()

            list_prev_position = []
            for driver, gp in zip(df_round["driver"], df_round["grandprix"]):
                df_round_driver_prev = df.loc[
                    (df["year"] == year - 1)
                    & (df["driver"] == driver)
                    & (df["grandprix"] == gp)
                ]
                if len(df_round_driver_prev) > 0:
                    prev_position = df_round_driver_prev["position"].values[0]
                else:
                    prev_position = np.nan
                list_prev_position.append(prev_position)
            df_round["prev_position"] = list_prev_position

            slowest_q1 = df_round["q1_sec"].dropna().max()
            slowest_q2 = df_round["q2_sec"].dropna().max()
            slowest_q3 = df_round["q3_sec"].dropna().max()
            fillvalue_q1 = slowest_q1 * 1.08
            fillvalue_q2 = slowest_q2 * 1.08
            fillvalue_q3 = slowest_q3 * 1.08
            df_round["q1_sec"].fillna(fillvalue_q1, inplace=True)
            df_round["q2_sec"].fillna(fillvalue_q2, inplace=True)
            df_round["q3_sec"].fillna(fillvalue_q3, inplace=True)

            fastest_q1 = df_round["q1_sec"].min()
            fastest_q2 = df_round["q2_sec"].min()
            fastest_q3 = df_round["q3_sec"].min()
            fastest_race = df_round["race_sec"].min()

            df_round["q1_percent"] = (
                (df_round["q1_sec"] - fastest_q1) / fastest_q1
            ) * 100
            df_round["q2_percent"] = (
                (df_round["q2_sec"] - fastest_q2) / fastest_q2
            ) * 100
            df_round["q3_percent"] = (
                (df_round["q3_sec"] - fastest_q3) / fastest_q3
            ) * 100
            df_round["race_diff_sec"] = df_round["race_sec"] - fastest_race
            df_round_constructor = (
                df_round.groupby("constructor")[
                    [
                        "position",
                        "q1_percent",
                        "q2_percent",
                        "q3_percent",
                        "race_diff_sec",
                    ]
                ]
                .mean()
                .reset_index()
            )
            df_round = pd.merge(
                df_round,
                df_round_constructor,
                on="constructor",
                how="left",
                suffixes=["", "_constructor"],
            )

            list_df.append(df_round)

    df_processed = pd.concat(list_df)
    df_processed.drop(columns=["q1_sec", "q2_sec", "q3_sec", "race_sec"], inplace=True)
    df_processed = df_processed.sort_values(by=["year", "round", "driver"]).reset_index(
        drop=True
    )

    return df_processed


def generate_features(df):
    """Create features"""
    dict_features = {x: [] for x in LIST_COL_X + LIST_COL_y + LIST_COL_IDENTIFIER}

    for year in tqdm(df["year"].unique()):
        df_season = df.loc[df["year"] == year].copy()
        for driver in df_season["driver"].unique():
            df_driver = (
                df_season.loc[df_season["driver"] == driver]
                .copy()
                .sort_values(by="round")
                .reset_index(drop=True)
            )
            df_driver.set_index("round", inplace=True)

            dict_features["recent_position"] += list(
                df_driver["position"]
                .shift()
                .rolling(window=3, min_periods=1)
                .apply(np.nanmean, raw=True)
            )
            dict_features["recent_race_diff_sec"] += list(
                df_driver["race_diff_sec"]
                .shift()
                .rolling(window=3, min_periods=1)
                .apply(np.nanmean, raw=True)
            )
            dict_features["recent_q1_percent"] += list(
                df_driver["q1_percent"]
                .shift()
                .rolling(window=3, min_periods=1)
                .apply(np.nanmean, raw=True)
            )
            dict_features["recent_q2_percent"] += list(
                df_driver["q2_percent"]
                .shift()
                .rolling(window=3, min_periods=1)
                .apply(np.nanmean, raw=True)
            )
            dict_features["recent_q3_percent"] += list(
                df_driver["q3_percent"]
                .shift()
                .rolling(window=3, min_periods=1)
                .apply(np.nanmean, raw=True)
            )
            dict_features["recent_position_std"] += list(
                df_driver["position"]
                .shift()
                .rolling(window=3, min_periods=1)
                .apply(np.nanstd, raw=True)
            )
            dict_features["recent_race_diff_sec_std"] += list(
                df_driver["race_diff_sec"]
                .shift()
                .rolling(window=3, min_periods=1)
                .apply(np.nanstd, raw=True)
            )
            dict_features["recent_q1_percent_std"] += list(
                df_driver["q1_percent"]
                .shift()
                .rolling(window=3, min_periods=1)
                .apply(np.nanstd, raw=True)
            )
            dict_features["recent_q2_percent_std"] += list(
                df_driver["q2_percent"]
                .shift()
                .rolling(window=3, min_periods=1)
                .apply(np.nanstd, raw=True)
            )
            dict_features["recent_q3_percent_std"] += list(
                df_driver["q3_percent"]
                .shift()
                .rolling(window=3, min_periods=1)
                .apply(np.nanstd, raw=True)
            )
            dict_features["season_position"] += list(
                df_driver["position"]
                .shift()
                .rolling(window=df_season["round"].max(), min_periods=1)
                .apply(np.nanmean, raw=True)
            )
            dict_features["season_race_diff_sec"] += list(
                df_driver["race_diff_sec"]
                .shift()
                .rolling(window=df_season["round"].max(), min_periods=1)
                .apply(np.nanmean, raw=True)
            )
            dict_features["season_q1_percent"] += list(
                df_driver["q1_percent"]
                .shift()
                .rolling(window=df_season["round"].max(), min_periods=1)
                .apply(np.nanmean, raw=True)
            )
            dict_features["season_q2_percent"] += list(
                df_driver["q2_percent"]
                .shift()
                .rolling(window=df_season["round"].max(), min_periods=1)
                .apply(np.nanmean, raw=True)
            )
            dict_features["season_q3_percent"] += list(
                df_driver["q3_percent"]
                .shift()
                .rolling(window=df_season["round"].max(), min_periods=1)
                .apply(np.nanmean, raw=True)
            )

            dict_features["recent_position_constructor"] += list(
                df_driver["position_constructor"]
                .shift()
                .rolling(window=3, min_periods=1)
                .apply(np.nanmean, raw=True)
            )
            dict_features["recent_race_diff_sec_constructor"] += list(
                df_driver["race_diff_sec_constructor"]
                .shift()
                .rolling(window=3, min_periods=1)
                .apply(np.nanmean, raw=True)
            )
            dict_features["recent_q1_percent_constructor"] += list(
                df_driver["q1_percent_constructor"]
                .shift()
                .rolling(window=3, min_periods=1)
                .apply(np.nanmean, raw=True)
            )
            dict_features["recent_q2_percent_constructor"] += list(
                df_driver["q2_percent_constructor"]
                .shift()
                .rolling(window=3, min_periods=1)
                .apply(np.nanmean, raw=True)
            )
            dict_features["recent_q3_percent_constructor"] += list(
                df_driver["q3_percent_constructor"]
                .shift()
                .rolling(window=3, min_periods=1)
                .apply(np.nanmean, raw=True)
            )
            dict_features["recent_position_std_constructor"] += list(
                df_driver["position_constructor"]
                .shift()
                .rolling(window=3, min_periods=1)
                .apply(np.nanstd, raw=True)
            )
            dict_features["recent_race_diff_sec_std_constructor"] += list(
                df_driver["race_diff_sec_constructor"]
                .shift()
                .rolling(window=3, min_periods=1)
                .apply(np.nanstd, raw=True)
            )
            dict_features["recent_q1_percent_std_constructor"] += list(
                df_driver["q1_percent_constructor"]
                .shift()
                .rolling(window=3, min_periods=1)
                .apply(np.nanstd, raw=True)
            )
            dict_features["recent_q2_percent_std_constructor"] += list(
                df_driver["q2_percent_constructor"]
                .shift()
                .rolling(window=3, min_periods=1)
                .apply(np.nanstd, raw=True)
            )
            dict_features["recent_q3_percent_std_constructor"] += list(
                df_driver["q3_percent_constructor"]
                .shift()
                .rolling(window=3, min_periods=1)
                .apply(np.nanstd, raw=True)
            )
            dict_features["season_position_constructor"] += list(
                df_driver["position_constructor"]
                .shift()
                .rolling(window=df_season["round"].max(), min_periods=1)
                .apply(np.nanmean, raw=True)
            )
            dict_features["season_race_diff_sec_constructor"] += list(
                df_driver["race_diff_sec_constructor"]
                .shift()
                .rolling(window=df_season["round"].max(), min_periods=1)
                .apply(np.nanmean, raw=True)
            )
            dict_features["season_q1_percent_constructor"] += list(
                df_driver["q1_percent_constructor"]
                .shift()
                .rolling(window=df_season["round"].max(), min_periods=1)
                .apply(np.nanmean, raw=True)
            )
            dict_features["season_q2_percent_constructor"] += list(
                df_driver["q2_percent_constructor"]
                .shift()
                .rolling(window=df_season["round"].max(), min_periods=1)
                .apply(np.nanmean, raw=True)
            )
            dict_features["season_q3_percent_constructor"] += list(
                df_driver["q3_percent_constructor"]
                .shift()
                .rolling(window=df_season["round"].max(), min_periods=1)
                .apply(np.nanmean, raw=True)
            )

            dict_features["prev_position"] += list(df_driver["prev_position"])
            dict_features["year"] += list(df_driver["year"])
            dict_features["round"] += list(df_driver.index)
            dict_features["driver"] += list(df_driver["driver"])
            dict_features["constructor"] += list(df_driver["constructor"])
            dict_features["grandprix"] += list(df_driver["grandprix"])
            dict_features["y"] += list(df_driver["position"])

    df_features = pd.DataFrame(dict_features)
    df_features_prev = df_features.loc[
        df_features["year"] != df_features["year"].max()
    ].copy()
    df_features_current = df_features.loc[
        df_features["year"] == df_features["year"].max()
    ].copy()

    # Replace recent related features
    list_df = []
    list_col_recent_related = df_features_current.columns[
        df_features_current.columns.str.contains("recent_")
    ]
    for driver in df_features_current["driver"].unique():
        df_driver = df_features_current.loc[df_features_current["driver"] == driver]
        next_round = df_driver[df_driver["y"].isnull()]["round"].min()
        most_recent_round = df_driver.loc[
            df_driver["round"] < next_round, "round"
        ].max()
        df_driver.loc[
            df_driver["round"] >= next_round, list_col_recent_related
        ] = df_driver.loc[
            df_driver["round"] == most_recent_round, list_col_recent_related
        ].values
        list_df.append(df_driver)
    df_features_current = pd.concat(list_df)

    df_features = (
        pd.concat([df_features_prev, df_features_current])
        .sort_values(by=["year", "round", "driver"])
        .reset_index(drop=True)
    )
    return df_features
