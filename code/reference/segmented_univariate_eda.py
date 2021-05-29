import unittest
from functools import reduce
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy as scp
from scipy import stats

class PandasTest(unittest.TestCase):
    def test_numpy_arrays(self):
        df = pd.read_csv("~/Downloads/EDA_nas.csv")
        print(df.columns)
        print(df["Watch.TV"])
        print(df.groupby(by="Watch.TV").median())
        print(df.groupby(by="Father.edu")["Maths.."].mean())
        print(df.groupby(by="Play.games")["Reading.."].mean())
        print(df.groupby(by="Solve.Maths")["Maths.."].mean())
        agree = df.groupby(by="Solve.Maths").get_group("Agree")
        disagree = df.groupby(by="Solve.Maths").get_group("Agree")
        agree.hist(column="Maths..")
        disagree.hist(column="Maths..")
        # print(df[" num_keywords"].mode())
        # print(df[" shares"].mean())
        # print(df[" shares"].median())
        # # df.boxplot(column=" shares")
        # # df.hist(column=" shares", bins=100)
        # print(df[" shares"].describe())
        # print(df[" shares"].quantile(q=0.7))
        # print(df[" shares"].quantile(q=0.8))
        # mean = np.mean(df[" shares"])
        # sd = np.std(df[" shares"])
        # quantile05 = df[" shares"].quantile(q=0.05)
        # quantile95 = df[" shares"].quantile(q=0.95)
        # print(f'05 quantile={quantile05} and 95 quantile={quantile95}')
        # print(f'thresholds are = {mean+2*sd} and {mean-2*sd}')
        # df["shares_zscore"]=np.abs(stats.zscore(df[" shares"]))
        # # x=df[(df[" shares"].astype(float)>quantile05) | (df[" shares"].astype(float)<quantile95)]
        # x=df[df[" shares"]<=quantile95]
        # # x=df[df[" shares"].apply(lambda s: s<mean+2*sd or s>mean-2*sd)]
        # # x=df[df["shares_zscore"].apply(lambda s: s<0.18)]
        # x.boxplot(column=" shares")
        # print("AFTER==============================================")
        # print(x[" shares"].describe())
        # print(x[" shares"].mean())
        # print(x[" shares"].std())
        # print(f'Percentage of data removed = {(df[" shares"].count()-x[" shares"].count())/df[" shares"].count()}')
        plt.show()
