# Name: Jordan Le
# Date: 12/28/19
# Description: File containing the class for ants
# Note: Doing some verification and testing in this file
import numpy as np
import random as rand


class Ants:
    def __init__(self):
        self.coord = [0, 0]
        self.moves = [1, 0, 0, 0]
        self.phermones = 5
        self.has_food = False

    def make_move(self):
        move = rand.randint(0,4)
        print(move)


if __name__ == "__main__":
    print("Hello\n{}".format(np.zeros((5,5))))
    move = rand.randint(0, 3)   # Later one hot this
    print(move)