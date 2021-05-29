import unittest
from functools import reduce
import numpy as np

class NumpyTest(unittest.TestCase):
    def test_numpy_arrays(self):
        print("Some Test")
        some_array = np.array([1,2,3])
        print(some_array.dtype)
        range_array = np.arange(5,10)
        print(range_array)
        print(np.linspace(0,1,5))
        twoDArray1 = np.array([[1,2,3], [4,5,6]])
        twoDArray2 = np.array([[1,2,3], [4,5,6]])
        array3x3 = np.array([[1,2,3], [4,5,6], [7,8,9]])
        print(twoDArray1)
        print(np.sin(twoDArray1[1]))
        print(twoDArray1-twoDArray2)
        print(twoDArray1*5)
        print(twoDArray1.transpose().dot(twoDArray1))
        print(twoDArray1[:2])
        print(np.ones([2,5,5])*30)
        print(np.identity(3))
        print(np.full([2,3,3], 3))
        print(np.random.random([4,4]))
        print(np.tile(np.full([2,2], 3), 3))
        n = 5
        row, col = np.indices([n,n])
        print((row+col)%2)
        print( [1, 2, 3, 5, 4, 6, 7, 8, 5, 3, 2][0::2])
        # print(np.arange(0, 5)%2)

        print('-------------------------------------------------------')
        input_list = [[11, 12, 13, 14],
         [21, 22, 23, 24],
         [31, 32, 33, 34]]

        array_2d =np.array(input_list)

        # Extract the first column, first row, last column and last row respectively using
        # appropriate indexing
        col_first = array_2d[:,0]
        row_first = array_2d[0,:]
        col_last = array_2d[:,-1]
        row_last = array_2d[-1,:]

        print(col_first)
        print(row_first)
        print(col_last)
        print(row_first)
