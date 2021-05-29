import unittest
from functools import reduce
import numpy as np
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
import scipy as scp
from scipy import stats


class PandasTest(unittest.TestCase):
    def test_numpy_arrays(self):
        df = pd.read_csv("~/Downloads/odi-batting.csv")
        print(df.columns)
        only_runs = df[["Player", "Runs"]]
        only_centuries = only_runs[only_runs["Runs"]>=100]
        only_players = only_centuries[["Player"]]
        centuries_by_player = only_players.groupby(by="Player").apply(len)
        # print(centuries_by_player.to_string())
        centuries_with_strike_rates = df[df["Runs"]>=100]
        centuries_with_strike_rates["StrikeRate"]=100.0*centuries_with_strike_rates["Runs"]/centuries_with_strike_rates["Balls"]
        sorted = centuries_with_strike_rates.sort_values(by=["StrikeRate"])
        # print(sorted.to_string())

        centuries_by_indian_players = df[(df["Runs"]>=100) & (df["Country"]=="India")]
        centuries_by_indian_players["Year"] = centuries_by_indian_players["MatchDate"].str[-4:]
        num_centuries_by_indians_by_year = centuries_by_indian_players.groupby(by=["Year"]).apply(len)
        print(num_centuries_by_indians_by_year)
        plt.show()
