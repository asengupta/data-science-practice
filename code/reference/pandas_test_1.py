import unittest
from functools import reduce
import numpy as np
import pandas as pd

class PandasTest(unittest.TestCase):
    def test_numpy_arrays(self):
        print('Haha')
        x = pd.Series([6,7,8,9,2,3,4,5])
        y = x.apply(lambda x: x*x)
        # print(y)
        # print(y.describe())
        print(y.shape)
        # print(list(y.columns))
        n=4
        print(np.arange(1, n+1)**2)

        print(pd.Series(np.arange(1,n+1)**2, index=range(1,n+1)))
        gold = pd.DataFrame({'Country': ['USA', 'France', 'Russia'],
                             'Medals': [15, 13, 9]}
                            )
        silver = pd.DataFrame({'Country': ['USA', 'Germany', 'Russia'],
                               'Medals': [29, 20, 16]}
                              )
        bronze = pd.DataFrame({'Country': ['France', 'USA', 'UK'],
                               'Medals': [40, 28, 27]}
                              )

        all = gold.append(silver).append(bronze)
        all_by_country = all.groupby(["Country"]).sum().sort_values(by="Medals", ascending=False)
        print(all_by_country)
