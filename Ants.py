# Name: Jordan Le
# Date: 12/28/19
# Description: File containing the class for ants
# Note: Doing some verification and testing in this file
#       - Git push with Ctrl Shift k
# Resources:
#   Dynamic Matplotlib - https://block.arch.ethz.ch/blog/2016/08/dynamic-plotting-with-matplotlib/
#   Adding a grid - https://stackoverflow.com/questions/38973868/adjusting-gridlines-and-ticks-in-matplotlib-imshow
#   Multi charts - https://stackoverflow.com/questions/46615554/how-to-display-multiple-images-in-one-figure-correctly
#   Update pheromones with np where - https://stackoverflow.com/questions/44810755/subtracting-a-number-from-an-array-if-condition-is-met-python
#   Random weighted choice - https://pynative.com/python-random-choice/

import numpy as np
import random as rand
import matplotlib.pyplot as plt
import time

fig = plt.figure()


def display_env_ph(field_data, ph_data, length, width, food_col):  # Function that displays two charts.
    fig.add_subplot(1, 2, 1)                    # Place environment chart on left
    display_env(field_data, length, width, food_col)
    fig.add_subplot(1, 2, 2)                    # Place pheromones chart on right
    display_pheromones(ph_data, length, width)

    plt.draw()
    plt.pause(1e-19)
    time.sleep(0.1)


def display_pheromones(ph_data, length, width):
    im2 = plt.imshow(ph_data)
    im2.set_data(ph_data)
    ax2 = plt.gca()
    ax2.set_title("Pheromone Env")
    # Major ticks & labels
    ax2.set_xticks(np.arange(0, width, 1))
    ax2.set_yticks(np.arange(0, length, 1))

    # Minor ticks with no labels
    ax2.set_xticks(np.arange(-.5, width, 1), minor=True)
    ax2.set_yticks(np.arange(-.5, length, 1), minor=True)

    ax2.grid(which='minor', color='black', linewidth=2)


def display_env(field_data, length, width, food_col):
    img_obj = plt.imshow(field_data, cmap=plt.cm.bwr)
    img_obj.set_data(field_data)

    ax = plt.gca()      # Putting a grid on the board
    ax.set_title("ANT ENV\nFood Collected: {}".format(food_col))
    # Major ticks & labels
    ax.set_xticks(np.arange(0, width, 1))
    ax.set_yticks(np.arange(0, length, 1))

    # Minor ticks with no labels
    ax.set_xticks(np.arange(-.5, width, 1), minor=True)
    ax.set_yticks(np.arange(-.5, length, 1), minor=True)

    ax.grid(which='minor', color='black', linewidth=2)


class Ants:
    def __init__(self, ant_num, length, width):
        self.ant_num = ant_num
        self.lim_coord = [length-1, width-1]
        self.old_coord = [0, 0]
        self.new_coord = [0, 0]
        self.moves = ['N','E','S','W']
        self.pheromone_trail = []    # List of coordinates length 5
        self.pheromone_drop = int((length + width)*2)     # average of length and width
        self.has_food = False

    def look_ahead(self, ph_field):   # See where ant can go
        turn_moves = []     # List of valid moves
        weights = []        # Weights of valid moves
        ops = set()         # Set of valid moves
        if self.new_coord[0] + 1 <= self.lim_coord[0]:      # In bounds SOUTH
            turn_moves.append('S')
            ops.add('S')
            weights.append(self.follow_ph(self.new_coord[0] + 1, self.new_coord[1], ph_field, turn_moves, 'S'))
        if self.new_coord[0] - 1 >= 0:                      # In bounds NORTH
            turn_moves.append('N')
            ops.add('N')
            weights.append(self.follow_ph(self.new_coord[0] - 1, self.new_coord[1], ph_field, turn_moves, 'N'))
        if self.new_coord[1] + 1 <= self.lim_coord[1]:      # In bounds EAST
            turn_moves.append('E')
            ops.add('E')
            weights.append(self.follow_ph(self.new_coord[0], self.new_coord[1] + 1, ph_field, turn_moves, 'E'))
        if self.new_coord[1] - 1 >= 0:                      # In bounds WEST
            turn_moves.append('W')
            ops.add('W')
            weights.append(self.follow_ph(self.new_coord[0], self.new_coord[1] - 1, ph_field, turn_moves, 'W'))

        div = sum(weights)
        print(weights)
        weights = [weight / div for weight in weights]
        print("weights {}\t\tlen weights {}\nmoves: {}".format(weights, len(weights), turn_moves))
        return turn_moves, ops, weights   # Move options for specific grid


    def follow_ph(self, coord1, coord2, ph_field, turn_moves, move):
        ph_val = ph_field[coord1][coord2]
        return ph_val + 1
        '''
        if ph_val != 0:
            incr_prob = int(ph_val/2)    # Go towards the bigger pheromone

            for i in range(incr_prob):
                turn_moves.append(move)
        '''


    def get_distance(self, temp_coord, home_coord):
        x = abs(temp_coord[0] - home_coord[0])
        y = abs(temp_coord[1] - home_coord[1])
        return x, y

    def go_home(self, turn_moves):  # Heuristic to head back home
        home = [0, 0]
        temp = [0, 0]
        temp[0] = self.new_coord[0]
        temp[1] = self.new_coord[1]
        temp2 = [0, 0]
        homing_moves = []

        for move in turn_moves:
            if move == 'N':  # North
                temp2[0] = temp[0] - 1
                temp2[1] = temp[1]

                x, y = self.get_distance(temp, home)
                x2, y2 = self.get_distance(temp2, home)

                if x2 < x or y2 < y:
                   homing_moves.append(move)

                #self.new_coord[0] -= 1
            elif move == 'E':  # East
                temp2[0] = temp[0]
                temp2[1] = temp[1] + 1

                x, y = self.get_distance(temp, home)
                x2, y2 = self.get_distance(temp2, home)

                if x2 < x or y2 < y:
                    homing_moves.append(move)
                #self.new_coord[1] += 1
            elif move == 'S':  # South
                temp2[0] = temp[0] + 1
                temp2[1] = temp[1]

                x, y = self.get_distance(temp, home)
                x2, y2 = self.get_distance(temp2, home)

                if x2 < x or y2 < y:
                    homing_moves.append(move)
                    #self.new_coord[0] += 1
            else:  # West
                temp2[0] = temp[0]
                temp2[1] = temp[1] - 1

                x, y = self.get_distance(temp, home)
                x2, y2 = self.get_distance(temp2, home)

                if x2 < x or y2 < y:
                    homing_moves.append(move)
                    #self.new_coord[1] -= 1

        return homing_moves


    def make_move(self, ph_field):

        turn_moves, ops, weights = self.look_ahead(ph_field)
        print(turn_moves)
        move = rand.choices(turn_moves, weights, k=1)[0]

        if self.has_food:   # if ant has food, then head home. Need to pheromone_drop pheromones...
            print(turn_moves)
            turn_moves = self.go_home(ops)   # Adjust turn moves
            print(turn_moves)
            move = rand.choices(turn_moves, k=1)[0]
        #move_index = rand.randint(0, len(turn_moves)-1)
        #move = turn_moves[move_index]       # Move is chosen between valid option

        print("MY MOVE: ", move)
        if move == 'N':       # North
            self.new_coord[0] -= 1
        elif move == 'E':     # East
            self.new_coord[1] += 1
        elif move == 'S':     # South
            self.new_coord[0] += 1
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
        self.food_collected = 0                                 # Amount of food ants collect
        self.food_coord = [self.length - 1, self.width - 1]     # Bottom right corner for now
        self.ph_env = np.zeros((self.length, self.width))       # Pheromone environment
        self.env = np.zeros((self.length, self.width))          # Environment for ants and food
        self.env[self.food_coord[0]][self.food_coord[1]] = 4
        self.ant_colony = [Ants(ant_num, self.length, self.width) for ant_num in range(num_ants)]
        for ant in self.ant_colony:
            self.env[ant.new_coord[0]][ant.new_coord[1]] = 1
        display_env_ph(self.env, self.ph_env, self.length, self.width, self.food_collected)   # Show initial State

    def time(self):
        for ant in self.ant_colony:
            #print(len(self.ant_colony))
            ant.make_move(self.ph_env)

            self.env[ant.new_coord[0]][ant.new_coord[1]] += 1    # Ant moved to here
            #print(self.env)
            self.env[ant.old_coord[0]][ant.old_coord[1]] -= 1    # This ant is no longer here...
            #print(self.env)
            #print("old {},\t new {}".format(ant.old_coord, ant.new_coord))
            '''
            # Only pheromone_drop phermones if have food...
            if ant.has_food:
                self.ph_env[ant.new_coord[0]][ant.new_coord[1]] += ant.pheromone_drop   # pheromone_drop pheromone
            '''

            if ant.new_coord[0] == self.food_coord[0] and ant.new_coord[1] == self.food_coord[1]:   # Match food coords
                ant.has_food = True     # Let ant know it has food and to head home.
                print("\nANT HAS FOOD!!\n")
                #ant.pheromone_drop = ant.pheromone_drop*2   # Double ph drop
                self.ph_env[ant.new_coord[0]][ant.new_coord[1]] = ant.pheromone_drop

            if ant.has_food and ant.new_coord[0] == self.colony[0] and ant.new_coord[1] == self.colony[1]:  # Match colony coords with food
                if ant.pheromone_drop >= 2:  # and ant.pheromone_drop % 2 == 1:
                    ant.pheromone_drop -= 2     # Drop pheromones on home base too.
                    self.ph_env[ant.new_coord[0]][ant.new_coord[1]] = ant.pheromone_drop  # Drop pheromone
                ant.has_food = False    # Deposited the food. Head out again.
                ant.pheromone_drop = int((self.length + self.width)*2)  # The initial pheromone
                print("\nFOOD DEPOSITED!!\n")
                self.food_collected += 1
                #ant.pheromone_drop = ant.pheromone_drop / 2  # Return ph drop to normal

            # Only drop phermones if have food...
            if ant.has_food:
                # Decay pheromones on the way home
                if ant.pheromone_drop >= 2: # and ant.pheromone_drop % 2 == 1:
                    ant.pheromone_drop -= 2

                if self.ph_env[ant.new_coord[0]][ant.new_coord[1]] == 0:    # if zero
                    self.ph_env[ant.new_coord[0]][ant.new_coord[1]] = ant.pheromone_drop   # Drop pheromone
                else:
                    self.ph_env[ant.new_coord[0]][ant.new_coord[1]] = ant.pheromone_drop    # add minor chunk to it - loop elimination?

            # Need to manually update the old coordinates or else it just points to new coords
            ant.old_coord[0] = ant.new_coord[0]     # Update the old coordinates
            ant.old_coord[1] = ant.new_coord[1]     # Update the old coordinates

            if self.env[0][0] < 0:  # Prevent colony from being negative
                self.env[0][0] = 0

        # Reduce all pheromones by 1
        sub_ind = np.where(self.ph_env > 0)
        self.ph_env[sub_ind] -= 1     # Subtract 1 from each of these indexes
        #print(self.env, "\n*****************")     # Show env after the ants have moved.
        #print(self.ph_env, "\n", sub_ind, "\n-----------------------------")  # Show env after the ants have moved.
        display_env_ph(self.env, self.ph_env, self.length, self.width, self.food_collected)


if __name__ == "__main__":
    field = Field(5, 5, 5)        # Field of dimension y=12, x=10. Number of ants = 5
    print("The Environment:")
    #print(field.env)

    while True:             # Ants get to move 30 times
        field.time()

    plt.show()      # Keep the image around
