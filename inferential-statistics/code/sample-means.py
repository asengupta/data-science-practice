import getopt
import logging
import math
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sample_means = pd.read_csv("../data/Inferential Statistics - UpGrad Samples.csv")
mean = sample_means["Sample Mean"].mean()
print(f"Mean={mean}")
sample_means["DEVIATION"] = np.power(sample_means["Sample Mean"] - mean, 2)

print(sample_means["Sample Mean"])
print(sample_means["DEVIATION"])

print(sample_means["DEVIATION"].describe())
print(sample_means["DEVIATION"].sum()/(sample_means["DEVIATION"].count()))
