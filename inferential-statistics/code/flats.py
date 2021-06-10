import getopt
import logging
import math
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
pd.set_option('display.max_columns', 500)

rents = pd.read_csv("../data/Inferential Statistics - Powai Flats Rent.csv")
print(rents.columns)
print(rents.columns[0])
print(len(rents))

RENT = "Monthly Rent"
z90 = 1.65
z95 = 1.96
z99 = 2.58
print(rents[RENT].describe())
margin = z95*rents[RENT].std()/math.sqrt(rents[RENT].count())
mean = rents[RENT].mean()
print(f"({mean - margin}, {mean + margin})")
