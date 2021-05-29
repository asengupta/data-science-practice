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
        df = pd.read_csv("~/Downloads/grades.csv")
        print(df.columns)
        zip_submissions = df[df.submission.str.contains(".zip")]
        print(len(zip_submissions)/len(df))
        first_deadline = pd.to_datetime("03-01-2017 11:59:59 PM", dayfirst=True)
        second_deadline = pd.to_datetime("09-01-2017 11:59:00    PM", dayfirst=True)
        df["submit_time2"] = pd.to_datetime(df["submit_time"])
        df["submit_date"] = df["submit_time2"].dt.date
        df["submit_hour"] = df["submit_time2"].dt.hour
        submissions_by_date = df.groupby(by="submit_date").apply(len)
        submissions_by_hour = df.groupby(by="submit_hour").apply(len)
        print(submissions_by_hour)
        print(submissions_by_date)
        submissions_after_first_deadline = df[df["submit_time2"]>first_deadline]
        print(f'submissions_after_first_deadline={len(submissions_after_first_deadline)}')
        print(first_deadline)
        print(second_deadline)
        print(df.to_string())
        print(submissions_after_first_deadline.to_string())
        df["submit_hour"].hist()
        plt.show()
