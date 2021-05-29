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
        df = pd.read_csv("~/Downloads/csv_EDA_census.xlsx - C-08.csv")
        print(df.columns)
        df["Literacy_Rate"]=df["Literate_Persons"]/df["Total_Persons"]
        df["Female_Literacy_Rate"]=df["Literate_Females"]/df["Total_Females"]
        country_wide_states = df[(df["Area_Name"]=="INDIA") & (df["Demographic"]=="Total") & (df["Age_Group"]!="All ages") & (df["Age_Group"]!="Age not stated")]
        literacy_rates = country_wide_states[["Age_Group", "Literate_Persons", "Literacy_Rate"]]
        # literacy_rates_by_age_group = literacy_rates.groupby(by="Age_Group")
        # # x=x.filter(lambda g: g.name=="All ages")
        # literacy_rates.apply(print)
        print(literacy_rates)
        # plt.barh(literacy_rates["Age_Group"], literacy_rates["Literacy_Rate"])
        # literacy_rates_by_age_group.hist(by="Age_Group")
        # y=literacy_rates_by_age_group.filter(fi)

        state_wide_stats = df[(df["Area_Name"]!="INDIA") & (df["Demographic"]=="Total") & (df["Age_Group"]=="All ages")]
        state_wide_female_literacy = state_wide_stats[["Area_Name", "Female_Literacy_Rate"]]
        print(state_wide_female_literacy)
        # plt.barh(state_wide_female_literacy["Area_Name"], state_wide_female_literacy["Female_Literacy_Rate"])

        state_wide_literacy = state_wide_stats[["Area_Name", "Literacy_Rate"]]
        print(state_wide_literacy)
        plt.barh(state_wide_literacy["Area_Name"], state_wide_literacy["Literacy_Rate"])
        plt.show()
