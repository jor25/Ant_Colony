# Name: Jordan Le
# Date: 12/28/19
# Description: File containing the class for ants
# Note: Doing some verification and testing in this file
#       - Git push with Ctrl Shift k
import numpy as np
import random as rand


class Ants:
    def __init__(self, ant_num):
        self.ant_num = ant_num
        self.old_coord = [0, 0]
        self.new_coord = [0, 0]
        self.moves = [1, 0, 0, 0]
        self.phermones = 5
        self.has_food = False

    def make_move(self):
        '''
        0 = North
        1 = East
        2 = South
        3 = West
        :return: coordinates
        '''
        move = rand.randint(0, 3)
        if move == 0:   # North
            self.new_coord[0] += 1
        elif move == 1:   # East
            self.new_coord[1] += 1
        elif move == 2:   # South
            self.new_coord[0] -= 1
        else:           # West
            self.new_coord[1] -= 1

        #print("Ant Move Old: {} \t New: {}".format(self.old_coord, self.new_coord))


class Field: # This may be a maze later on.
    def __init__(self, length=5, width=5, num_ants=1):          # Generic set to 5x5
        self.length = length                                    # Length of field
        self.width = width                                      # Width of field
        self.colony = [0, 0]                                    # Top left corner
        self.food_coord = [self.length - 1, self.width - 1]     # Bottom right corner for now
        self.env = np.zeros((self.length, self.width))          # Environment for ants and food
        self.ant_colony = [Ants(ant_num) for ant_num in range(num_ants)]
        for ant in self.ant_colony:
            self.env[ant.new_coord[0]][ant.new_coord[1]] = 1

    def time(self):
        for ant in self.ant_colony:
            #print(len(self.ant_colony))
            ant.make_move()
            self.env[ant.new_coord[0]][ant.new_coord[1]] = 1    # Ant moved to here
            #print(self.env)
            self.env[ant.old_coord[0]][ant.old_coord[1]] = 0    # This ant is no longer here...
            #print(self.env)
            #print("old {},\t new {}".format(ant.old_coord, ant.new_coord))

            # Need to manually update the old coordinates or else it just points to new coords
            ant.old_coord[0] = ant.new_coord[0]     # Update the old coordinates
            ant.old_coord[1] = ant.new_coord[1]     # Update the old coordinates

        print(self.env, "\n*****************")     # Show env after the ants have moved.


if __name__ == "__main__":
    field = Field()
    print("The Environment:")
    print(field.env)

    for i in range(10):
        field.time()