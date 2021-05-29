import unittest
from functools import reduce
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy as scp
from scipy import stats

def fi(group):
    # print(group.name)
    return True

class PandasTest(unittest.TestCase):
    def test_numpy_arrays(self):
        df = pd.read_csv("~/Downloads/EDA_Gold_Silver_prices.csv")
        print(df.columns)
        df["Year"] = df["Month"].str[-2:]
        grouped_by_year=df.groupby(["Year"])
        df=df[df["Month"].str.contains("-08")]
        print(df)
        print(df.corr())
        # grouped_by_year.apply(print)
        correlations = grouped_by_year.apply(lambda g: g["GoldPrice"].corr(g["SilverPrice"]))
        print("=========================================")
        print(correlations)
        plt.hist(correlations)
        # print(correlations.dtype)
        plt.show()
