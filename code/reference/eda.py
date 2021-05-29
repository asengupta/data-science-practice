import unittest
from functools import reduce
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class PandasTest(unittest.TestCase):
    def test_numpy_arrays(self):
        df = pd.read_csv("~/Downloads/tendulkar_ODI.csv")
        print(df.columns)
        # print(df.isnull().sum())
        # print(df["Current Ver"])
        # print(df.isnull().sum())
        # df=df[~df["Rating"].isnull()]
        # print(df.isnull().sum().sum())
        # print(df["Android Ver"].value_counts())
        # df[df["Current Ver"]=="Varies with device"]="-1"
        # print(df["Current Ver"])

        # dfgtt4_1 = df[df["Android Ver"]=="4.1 and up"]
        # print(dfgtt4_1[dfgtt4_1["Price"]!="0"].Price)
        # print(dfgtt4_1[dfgtt4_1["Price"]=="0."])
        # sanitised_price_series = pd.to_numeric(dfgtt4_1.Price.str.extract(pat='(\d+(?:.\d)?)')[0])
        # print(sanitised_price_series)
        # print(sanitised_price_series.quantile(q=0.75)-sanitised_price_series.quantile(q=0.25))
        # x = pd.DataFrame(sanitised_price_series)
        # print(x)
        # p=x.boxplot(column=[0])
        # dfgtt4_1["reviews_as_number"]=pd.to_numeric(dfgtt4_1["Reviews"])
        # print(dfgtt4_1["reviews_as_number"])
        # unpopular_apps = dfgtt4_1[dfgtt4_1["reviews_as_number"]<=1000000]
        # y = pd.DataFrame(unpopular_apps)
        # q=y.hist(bins=10)

        # print(df.Installs.describe())
        # df=df[df.Installs!="Free"]
        # print(df.Installs.describe())
        # sanitised_installs = pd.to_numeric(df.Installs.str.replace(',', '').str.replace('+', ''))
        # sanitised_installs = sanitised_installs[sanitised_installs<=100000000]
        # # print(sanitised_installs.describe())
        # print(sanitised_installs.quantile(0.75)-sanitised_installs.quantile(0.25))
        # print(sanitised_installs.describe()["75%"]-sanitised_installs.describe()["25%"])
        # x=pd.DataFrame(sanitised_installs)
        # print(sanitised_installs.describe())
        # c=x.boxplot(column="Installs")
        # c=x.hist()

        # print(df.Size.dtype)
        # df.hist(column="Size")
        # df.boxplot(column="Size")
        # print(df.Size.describe())
        # print(pd.to_numeric(dfgtt4_1.Installs.str.replace(',', '').str.replace('+', '')).quantile())
        # print(df[df["Android Ver"]=="4.1 and up"].Price.mean())
        # plt.show()
        bad_run_columns=df[df["Runs"].apply(lambda x: not x.isnumeric())]

        df=df[df["Runs"].apply(lambda x: x.isnumeric())]
        df=df[df["4s"].apply(lambda x: x.isnumeric())]
        df["RunsAsNumeric"]=df["Runs"].astype(int)
        high_run_columns=df[df["RunsAsNumeric"]>200]
        print(high_run_columns["RunsAsNumeric"])
        df["4sAsNumeric"]=df["4s"].astype(int)
        fig = plt.figure()
        ax = fig.add_axes([0,0,1,1])
        # print(df.RunsAsNumeric.dtype)
        # print(df["RunsAsNumeric"])
        df.hist(column="RunsAsNumeric")
        df.hist(column="4sAsNumeric", bins=20)
        plt.show()
