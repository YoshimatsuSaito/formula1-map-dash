import itertools

import pandas as pd
from scipy.optimize import minimize


def calc_degradation(laps, degradation):
    laps_degradation = laps - 1  # no degradation at the first lap of the tyre
    cumulative_laps = (laps_degradation * (1 + laps_degradation)) / 2  #
    time_degradation = cumulative_laps * degradation
    return time_degradation


def calc_track_improvement(laps, track_improvement):
    laps_track_improvement = laps - 1  # no improvement at the first lap
    cumulative_laps = (laps_track_improvement * (1 + laps_track_improvement)) / 2
    time_track_improvement = cumulative_laps * track_improvement
    return time_track_improvement


def calc_fuel_effect(laps, fuel_effect):
    laps_fuel_effect = laps - 1  # no improvement at the first lap
    cumulative_laps = (laps_fuel_effect * (1 + laps_fuel_effect)) / 2  #
    time_fuel_effect = cumulative_laps * fuel_effect
    return time_fuel_effect


def create_tyre_combination(
    stops_to_consider=[1, 2, 3], tyres=["Soft", "Medium", "Hard"]
):
    # combination between tyres
    dict_tyre_combi = dict()
    for n_stop in stops_to_consider:
        list_tyre_combi = list(
            itertools.combinations_with_replacement(tyres, n_stop + 1)
        )
        list_tyre_combi = [
            x for x in list_tyre_combi if len(set(x)) > 1
        ]  # remove combinations which use same tyre only
        dict_tyre_combi[n_stop] = list_tyre_combi
    return dict_tyre_combi


class Strategy:
    def __init__(
        self,
        n_stop,
        pitloss,
        total_lap,
        dict_degradation,
        dict_pace,
        fuel_effect=0,
        track_improvement=0,
    ):
        self.n_stop = n_stop
        self.pitloss = pitloss
        self.total_lap = total_lap
        self.dict_degradation = dict_degradation
        self.dict_pace = dict_pace
        self.fuel_effect = fuel_effect
        self.track_improvement = track_improvement
        # must complete at least 1 lap by a tyre and also must not complete every lap by a tyre
        self.bounds = tuple([(1, total_lap - n_stop) for _ in range(n_stop + 1)])
        # sum of laps completed by all tyres must be same as total lap
        self.constraints = {"type": "eq", "fun": lambda x: sum(x) - self.total_lap}
        # initial value
        self.x0 = [self.total_lap // (self.n_stop + 1) for _ in range(self.n_stop)]
        self.x0.append(self.total_lap - sum(self.x0))

    # function to get total lap time
    def get_lap_time(self, params, *combi):
        total_pitloss = self.pitloss * self.n_stop
        total_pace = sum(
            params[x] * self.dict_pace[combi[x]] for x in range(self.n_stop + 1)
        )
        total_degradation = sum(
            calc_degradation(params[x], self.dict_degradation[combi[x]])
            for x in range(self.n_stop + 1)
        )
        total_track_improvement = calc_track_improvement(
            self.total_lap, self.track_improvement
        )
        total_fuel_effect = calc_fuel_effect(self.total_lap, self.fuel_effect)
        total_lap_times = (
            total_pace
            + total_degradation
            + total_pitloss
            - total_fuel_effect
            - total_track_improvement
        )
        return total_lap_times

    # function to calculate optimal strategy based on given information
    def optimize(self, combi):
        res = minimize(
            self.get_lap_time,
            x0=self.x0,
            args=combi,
            constraints=self.constraints,
            bounds=self.bounds,
            method="SLSQP",
        )
        return res


def optimize_strategy(
    pitloss, total_lap, dict_degradation, dict_pace, fuel_effect=0, track_improvement=0
):
    """Optimize strategy given information"""
    dict_tyre_combi = create_tyre_combination()

    list_all_result = list()
    for n_stop in dict_tyre_combi.keys():
        list_combi = dict_tyre_combi[n_stop]
        strat = Strategy(
            n_stop=n_stop,
            pitloss=pitloss,
            total_lap=total_lap,
            dict_degradation=dict_degradation,
            dict_pace=dict_pace,
            fuel_effect=fuel_effect,
            track_improvement=track_improvement,
        )
        for combi in list_combi:
            res = strat.optimize(combi)
            list_res = list()

            list_stint_tyre = [x for x in combi]
            list_stint_tyre += [None] * (
                max(dict_tyre_combi.keys()) + 1 - len(list_stint_tyre)
            )
            list_stint_laps = [int(x) for x in res.x]
            list_stint_laps[-1] += total_lap - sum(
                list_stint_laps
            )  # convert float to int
            list_stint_laps += [0] * (
                max(dict_tyre_combi.keys()) + 1 - len(list_stint_laps)
            )

            list_res += list_stint_tyre
            list_res += list_stint_laps
            list_res.append(n_stop)
            list_res.append(pitloss)
            list_res.append(total_lap)
            list_res.append(track_improvement)
            list_res.append(fuel_effect)
            list_res += list(dict_degradation.values())
            list_res += list(dict_pace.values())
            list_res.append(res.success)
            list_res.append(res.fun)

            list_all_result.append(list_res)
    df_res = pd.DataFrame(
        list_all_result,
        columns=[
            "tyre_1",
            "tyre_2",
            "tyre_3",
            "tyre_4",
            "laps_1",
            "laps_2",
            "laps_3",
            "laps_4",
            "n_stop",
            "pitloss",
            "total_lap",
            "track_improvement",
            "fuel_effect",
            "degradation_Soft",
            "degradation_Medium",
            "degradation_Hard",
            "pace_Soft",
            "pace_Medium",
            "pace_Hard",
            "status",
            "total_lap_time",
        ],
    )
    df_res = df_res.sort_values(by="total_lap_time").reset_index(drop=True)
    return df_res
