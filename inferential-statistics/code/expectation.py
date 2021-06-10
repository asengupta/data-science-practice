import getopt
import logging
import math
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

EXPOSURE_AT_DEFAULT = "Exposure at Default (in lakh Rs.)"
RECOVERY_PERCENTAGE = "Recovery (%)"
PROBABILITY_OF_DEFAULT = "Probability of Default"

investments = pd.read_csv("../data/Inferential Statistics - Student Loan.csv")
print(investments.columns)


investments["LOSS_FRACTION"] = (100 - pd.to_numeric(investments[RECOVERY_PERCENTAGE].str.slice(0,-1)))/100
# print(investments["LOSS_FRACTION"])
investments["STUFF"] = investments[EXPOSURE_AT_DEFAULT]*investments["LOSS_FRACTION"]*investments[PROBABILITY_OF_DEFAULT]
print(investments["STUFF"].sum())


all = range(0,3)
p = 0.4
p_dash = 1 - p
total = 10

sum = 0
print(all)
for i in all:
    t = math.comb(total, i) * (p ** i) * ((1 - p) ** (total - i))
    # print(t)
    sum+= t

# print(sum)

def normal(mu, sigma):
    return lambda x: 1.0/(math.sqrt(2*math.pi)*sigma) * math.exp(-0.5*((x-mu)/sigma)**2)

n = normal(35, 5)
print(n(45))
# print(n(45) - n(25))
