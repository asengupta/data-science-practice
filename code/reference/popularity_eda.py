import unittest
from functools import reduce
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy as scp
from scipy import stats

class PandasTest(unittest.TestCase):
    def test_numpy_arrays(self):
        df = pd.read_csv("~/Downloads/popularity.csv")
        print(df.columns)
        print(df[" num_keywords"].mode())
        print(df[" shares"].mean())
        print(df[" shares"].median())
        # df.boxplot(column=" shares")
        # df.hist(column=" shares", bins=100)
        print(df[" shares"].describe())
        print(df[" shares"].quantile(q=0.7))
        print(df[" shares"].quantile(q=0.8))
        mean = np.mean(df[" shares"])
        sd = np.std(df[" shares"])
        quantile05 = df[" shares"].quantile(q=0.05)
        quantile95 = df[" shares"].quantile(q=0.95)
        print(f'05 quantile={quantile05} and 95 quantile={quantile95}')
        print(f'thresholds are = {mean+2*sd} and {mean-2*sd}')
        df["shares_zscore"]=np.abs(stats.zscore(df[" shares"]))
        # x=df[(df[" shares"].astype(float)>quantile05) | (df[" shares"].astype(float)<quantile95)]
        x=df[df[" shares"]<=quantile95]
        # x=df[df[" shares"].apply(lambda s: s<mean+2*sd or s>mean-2*sd)]
        # x=df[df["shares_zscore"].apply(lambda s: s<0.18)]
        x.boxplot(column=" shares")
        print("AFTER==============================================")
        print(x[" shares"].describe())
        print(x[" shares"].mean())
        print(x[" shares"].std())
        print(f'Percentage of data removed = {(df[" shares"].count()-x[" shares"].count())/df[" shares"].count()}')
        # bad_run_columns=df[df["Runs"].apply(lambda x: not x.isnumeric())]
        #
        # df=df[df["Runs"].apply(lambda x: x.isnumeric())]
        # df=df[df["4s"].apply(lambda x: x.isnumeric())]
        # df["RunsAsNumeric"]=df["Runs"].astype(int)
        # high_run_columns=df[df["RunsAsNumeric"]>200]
        # print(high_run_columns["RunsAsNumeric"])
        # df["4sAsNumeric"]=df["4s"].astype(int)
        # fig = plt.figure()
        # ax = fig.add_axes([0,0,1,1])
        # # print(df.RunsAsNumeric.dtype)
        # # print(df["RunsAsNumeric"])
        # df.hist(column="RunsAsNumeric")
        # df.hist(column="4sAsNumeric", bins=20)
        plt.show()
