# Name: Jordan Le
# Date: 1/5/2020
# Description: The wall class which creates obstacles on the field for ants to navigate around.
# Resources:
#   Select random coordinates https://docs.scipy.org/doc/numpy-1.15.1/reference/generated/numpy.random.randint.html
#   Convert to list. https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.tolist.html

import numpy as np

class Wall:
    def __init__(self, length, width, pt_obs=0):
        """
        Initialize random wall block options.
        :param length: Integer height of the plot.
        :param width: Integer width of the plot.
        :param pt_obs: Integer number of potential objects.
        """
        # Initialize potential objects number
        self.pt_obs = pt_obs

        # Take the smaller of the 2, sub 2
        if length > width:
            self.cap = width - 1
        else:
            self.cap = length - 1

        # Check to see how many potential obstacles to include
        # Only collect the unique numbers
        if self.pt_obs > 0:
            self.blocks = np.random.randint(1, self.cap, size=(self.pt_obs, 2)).tolist()
            arr, uniq_cnt = np.unique(self.blocks, axis=0, return_counts=True)
            uniq_arr = arr[uniq_cnt == 1]
            self.blocks = uniq_arr.tolist()
            #print(uniq_arr)
            #print(self.blocks)
        else:
            self.blocks = []