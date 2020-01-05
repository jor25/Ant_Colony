import numpy as np
# Select random coordinates https://docs.scipy.org/doc/numpy-1.15.1/reference/generated/numpy.random.randint.html
# Convert to list. https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.tolist.html
class Wall:
    def __init__(self):
        self.blocks = [[6, 6], [6, 7], [7, 6], [7,7], [6,8], [8,6], [6,5], [5,6]]
        print(self.blocks)
        self.blocks = np.random.randint(1, 7, size=(19, 2)).tolist()
        print(self.blocks)