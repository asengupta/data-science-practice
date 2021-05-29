import unittest
from functools import reduce
import numpy as np
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
import scipy as scp
from scipy import stats

def fi(group):
    # print(group.name)
    return True

class PandasTest(unittest.TestCase):
    def test_numpy_arrays(self):
        df = pd.read_csv("~/Downloads/currencies.csv")
        print(df.columns)
        df=df[["Euro", "Japanese Yen", "U.K. Pound Sterling", "U.S. Dollar", "Australian Dollar", "Indian Rupee"]]
        currency_correlations = df.corr()
        print(currency_correlations)
        sn.heatmap(currency_correlations, annot=True)
        plt.show()
