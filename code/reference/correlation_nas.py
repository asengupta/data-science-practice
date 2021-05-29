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
        df = pd.read_csv("~/Downloads/nas.csv")
        print(df.columns)
        mother_education_vs_siblings = df[['Mother.edu', 'Siblings']]
        pivoted_mother_education = mother_education_vs_siblings.pivot_table(index="Mother.edu", columns="Siblings", aggfunc=len)
        # print(pivoted_mother_education)
        # print(pd.factorize(df["Father.edu"]))
        # father_education_avg_science_marks = df[['Father.edu', 'Science..']]
        # pivoted_father_education_avg_science_marks = father_education_avg_science_marks.pivot_table(index="Father.edu", "")
        father_education_degree = df[df["Father.edu"] == "Degree & above"]
        print(science_across_age_groups(father_education_degree))
        print(science_across_age_groups(df))
        lol = df[["Father.edu", "Age", "Science.."]]
        pivoted_father_education_age = lol.pivot_table(index="Father.edu", columns="Age", aggfunc=np.mean)
        print(pivoted_father_education_age.to_string())
        # plt.show()


def science_across_age_groups(data):
    print(len(data))
    age_and_science = data[["Age", "Science.."]]
    return age_and_science.groupby(by="Age").mean()
