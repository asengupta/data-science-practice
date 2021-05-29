import math
import unittest
from functools import reduce
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def as_degrees(radians):
    return radians*180/math.pi
    # return radians

class PandasTest(unittest.TestCase):
    def test_numpy_arrays(self):
        v1 = [2,1,0,0]
        v4 = [1,1,1,0]
        v3 = [1,1,0,0]
        dot14 = np.dot(v1, v4)
        ab14=math.sqrt(5)*math.sqrt(3)
        print(dot14)
        print(as_degrees(np.arccos(dot14/ab14)))

        dot34 = np.dot(v3, v4)
        print(dot34)
        print(as_degrees(np.arccos(dot34/(math.sqrt(3)*math.sqrt(2)))))

        mat=[[4,9],
             [7,6]
             ]
        c, v = np.linalg.eig(mat)
        print(c)
        print(v)
