# Name: Jordan Le
# Date: 12/28/19
# Description: File containing the class for ants
# Note: Doing some verification and testing in this file
#       - Git push with Ctrl Shift k
# Resources:
#   Dynamic Matplotlib - https://block.arch.ethz.ch/blog/2016/08/dynamic-plotting-with-matplotlib/
#   Adding a grid - https://stackoverflow.com/questions/38973868/adjusting-gridlines-and-ticks-in-matplotlib-imshow
#   Multi charts - https://stackoverflow.com/questions/46615554/how-to-display-multiple-images-in-one-figure-correctly


import numpy as np
import random as rand
import matplotlib.pyplot as plt
import time

fig = plt.figure()


def display_env_ph(field_data, length, width):  # Function that displays two charts.
    fig.add_subplot(1, 2, 1)                    # Place environment chart on left
    display_env(field_data, length, width)
    fig.add_subplot(1, 2, 2)                    # Place pheromones chart on right
    display_pheromones(field_data, length, width)

    plt.draw()
    plt.pause(1e-19)
    time.sleep(0.1)


def display_pheromones(ph_data, length, width):
    im2 = plt.imshow(ph_data)
    im2.set_data(ph_data)
    ax2 = plt.gca()
    # Major ticks & labels
    ax2.set_xticks(np.arange(0, width, 1))
    ax2.set_yticks(np.arange(0, length, 1))

    # Minor ticks with no labels
    ax2.set_xticks(np.arange(-.5, width, 1), minor=True)
    ax2.set_yticks(np.arange(-.5, length, 1), minor=True)

    ax2.grid(which='minor', color='black', linewidth=2)
    '''
    plt.draw()
    plt.pause(1e-19)
    time.sleep(0.1)
    '''

def display_env(field_data, length, width):
    img_obj = plt.imshow(field_data, cmap=plt.cm.bwr)
    img_obj.set_data(field_data)

    ax = plt.gca()      # Putting a grid on the board

    # Major ticks & labels
    ax.set_xticks(np.arange(0, width, 1))
    ax.set_yticks(np.arange(0, length, 1))

    # Minor ticks with no labels
    ax.set_xticks(np.arange(-.5, width, 1), minor=True)
    ax.set_yticks(np.arange(-.5, length, 1), minor=True)

    ax.grid(which='minor', color='black', linewidth=2)
    '''
    plt.draw()
    plt.pause(1e-19)
    time.sleep(0.1)
    '''

class Ants:
    def __init__(self, ant_num, length, width):
        self.ant_num = ant_num
        self.lim_coord = [length-1, width-1]
        self.old_coord = [0, 0]
        self.new_coord = [0, 0]
        self.moves = [1, 0, 0, 0]
        self.pheromone_trail = []    # List of coordinates length 5
        self.pheromone_lim = 5       # Limit of 5 for trail length
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
        if move == 0:       # North
            self.new_coord[0] += 1
        elif move == 1:     # East
            self.new_coord[1] += 1
        elif move == 2:     # South
            self.new_coord[0] -= 1
        else:               # West
            self.new_coord[1] -= 1

        # Verify that ant is in bounds:
        if self.new_coord[0] < 0 or self.new_coord[0] > self.lim_coord[0]\
                or self.new_coord[1] < 0 or self.new_coord[1] > self.lim_coord[1]:
            print("{} Out of bounds!".format(self.new_coord))
            self.new_coord[0] = self.old_coord[0]       # Reset coordinates
            self.new_coord[1] = self.old_coord[1]


        #print("Ant Move Old: {} \t New: {}".format(self.old_coord, self.new_coord))


class Field: # This may be a maze later on.
    def __init__(self, length=5, width=5, num_ants=1):          # Generic set to 5x5
        self.length = length                                    # Length of field
        self.width = width                                      # Width of field
        self.colony = [0, 0]                                    # Top left corner
        self.food_coord = [self.length - 1, self.width - 1]     # Bottom right corner for now
        self.env = np.zeros((self.length, self.width))          # Environment for ants and food
        self.env[self.food_coord[0]][self.food_coord[1]] = 4
        self.ant_colony = [Ants(ant_num, self.length, self.width) for ant_num in range(num_ants)]
        for ant in self.ant_colony:
            self.env[ant.new_coord[0]][ant.new_coord[1]] = 1
        display_env_ph(self.env, self.length, self.width)   # Show initial State

    def time(self):
        for ant in self.ant_colony:
            #print(len(self.ant_colony))
            ant.make_move()

            self.env[ant.new_coord[0]][ant.new_coord[1]] += 1    # Ant moved to here
            #print(self.env)
            self.env[ant.old_coord[0]][ant.old_coord[1]] -= 1    # This ant is no longer here...
            #print(self.env)
            #print("old {},\t new {}".format(ant.old_coord, ant.new_coord))

            # Need to manually update the old coordinates or else it just points to new coords
            ant.old_coord[0] = ant.new_coord[0]     # Update the old coordinates
            ant.old_coord[1] = ant.new_coord[1]     # Update the old coordinates

            if self.env[0][0] < 0:  # Prevent colony from being negative
                self.env[0][0] = 0

        print(self.env, "\n*****************")     # Show env after the ants have moved.
        display_env_ph(self.env, self.length, self.width)


if __name__ == "__main__":
    field = Field(12, 10, 5)        # Field of dimension y=12, x=10. Number of ants = 5
    print("The Environment:")
    print(field.env)

    for i in range(50):             # Ants get to move 30 times
        field.time()

    plt.show()      # Keep the image around
