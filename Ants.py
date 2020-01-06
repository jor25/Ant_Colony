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
#   Vectorized add 4 to all walls - https://stackoverflow.com/questions/55176269/list-of-xy-coordinates-to-matrix
#                                 - https://docs.scipy.org/doc/numpy/reference/generated/numpy.ufunc.at.html

import numpy as np
import random as rand
import matplotlib.pyplot as plt
import time
import Walls as w

# Convert these globals to system arguments later on
LENGTH = 10
WIDTH = 10
NUM_ANTS = 65
PT_OBS = 20


# Initialize the wall class and the matplotlib figure
walls = w.Wall(LENGTH, WIDTH, PT_OBS)
fig = plt.figure()


def display_env_ph(field_data, ph_data, length, width, food_col, num_ants, step):
    """
    Display two charts, the ant environment(left), and the pheromone environment(right).
    :param field_data: 2D numpy array provided from the Field class for ants and obstacles.
    :param ph_data: 2D numpy array provided from the Field class for pheromones.
    :param length: Integer height of the plot.
    :param width: Integer width of the plot.
    :param food_col: Integer food collected from Field class.
    :param num_ants: Integer number of ants from Field class colony.
    :param step: Integer number of steps taken from Field class.
    :return: N/A
    """
    # Place environment chart on left
    fig.add_subplot(1, 2, 1)
    display_env(field_data, length, width, food_col)

    # Place pheromones chart on right
    fig.add_subplot(1, 2, 2)
    display_pheromones(ph_data, length, width)

    # Place the title of the plot with dynamic details
    fig.suptitle('Ant Colony Algorithm\nAnt #: {}\nStep #: {}'.format(num_ants, step), fontsize=15)

    # Draw the plots and wait.
    plt.draw()
    plt.pause(1e-15)
    time.sleep(0.1)


def display_pheromones(ph_data, length, width):
    """
    Displays the pheromone environment. This allows us to see the pheromones being dropped.
    :param ph_data: 2D numpy array from Field class for pheromones. (display_env_ph)
    :param length: Integer height of the plot. (display_env_ph)
    :param width: Integer width of the plot. (display_env_ph)
    :return: N/A
    """
    # Set the ph data on the plot and provide titles
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

    # Set line width for the minor ticks
    ax2.grid(which='minor', color='black', linewidth=2)


def display_env(field_data, length, width, food_col):
    """
    Display the ant's environment. This allows us to see where all the ants are moving.
    :param field_data: 2D numpy array provided from Field class for ants and obstacles. (display_env_ph)
    :param length: Integer height of the plot. (display_env_ph)
    :param width: Integer width of the plot. (display_env_ph)
    :param food_col: Integer food collected from Field class. (display_env_ph)
    :return: N/A
    """
    # Select the color set up for display env.
    img_obj = plt.imshow(field_data, cmap=plt.cm.bwr)
    img_obj.set_data(field_data)

    # Putting a grid on the board with dynamic labels
    ax = plt.gca()
    ax.set_title("ANT ENV\nFood Collected: {}".format(food_col))

    # Major ticks & labels
    ax.set_xticks(np.arange(0, width, 1))
    ax.set_yticks(np.arange(0, length, 1))

    # Minor ticks with no labels
    ax.set_xticks(np.arange(-.5, width, 1), minor=True)
    ax.set_yticks(np.arange(-.5, length, 1), minor=True)

    # Set line width for the minor ticks
    ax.grid(which='minor', color='black', linewidth=2)


"""
Ant Class
"""
class Ants:
    def __init__(self, ant_num, length, width, col_coord):
        """
        Initialize individual ants
        :param ant_num: Integer the ant's number
        :param length: Integer height of the plot.
        :param width: Integer width of the plot.
        :param col_coord: Coordinates of the ant colony - where ants start out.
        """
        self.ant_num = ant_num                              # Set the ant number
        self.life_span = 500                                # How long an ant survives - Currently not in use
        self.lim_coord = [length-1, width-1]                # Coordinate limits to prevent ants from leaving environment
        self.home = [col_coord[0], col_coord[1]]            # This is the ant colony's coordinates
        self.old_coord = [col_coord[0], col_coord[1]]       # Where the ant was
        self.new_coord = [col_coord[0], col_coord[1]]       # Where the ant will move to
        self.pheromone_trail = []                           # List of coordinates length 5 - currently not in use
        self.pheromone_drop = int((length + width)*3)       # How much pheromone to drop - initializing
        self.has_food = False                               # If the ant has food

    def look_ahead(self, ph_field, food_coord):   # See where ant can go
        """
        Identify where the ant is allowed to move, it can't go through obstacles or limits.
        :param ph_field: Pheromones on the field
        :param food_coord: The coordinates of the food - not used directly, we just know if the next one is food.
        :return: turn_moves (list of valid moves), ops (set of valid moves), weights (list of floats)
        """
        turn_moves = []     # List of valid moves
        weights = []        # Weights of valid moves
        ops = set()         # Set of valid moves

        # Check if the tile to the South is valid, if it is then add to valid options
        if self.new_coord[0] + 1 <= self.lim_coord[0] and \
                [self.new_coord[0] + 1, self.new_coord[1]] not in walls.blocks:         # In bounds SOUTH
            turn_moves.append('S')
            ops.add('S')
            weights.append(self.follow_ph(self.new_coord[0] + 1, self.new_coord[1], ph_field))
            if np.array_equal([self.new_coord[0] + 1, self.new_coord[1]], food_coord):  # if food coordinate
                weights[-1] = weights[-1] * 10      # Most recently added element * 10

        # Check if the tile to the North is valid, if it is then add to valid options
        if self.new_coord[0] - 1 >= 0 and \
                [self.new_coord[0] - 1, self.new_coord[1]] not in walls.blocks:         # In bounds NORTH
            turn_moves.append('N')
            ops.add('N')
            weights.append(self.follow_ph(self.new_coord[0] - 1, self.new_coord[1], ph_field))
            if np.array_equal([self.new_coord[0] - 1, self.new_coord[1]], food_coord):  # if food coordinate
                weights[-1] = weights[-1] * 10      # Most recently added element * 10

        # Check if the tile to the East is valid, if it is then add to valid options
        if self.new_coord[1] + 1 <= self.lim_coord[1] and \
                [self.new_coord[0], self.new_coord[1] + 1] not in walls.blocks:         # In bounds EAST
            turn_moves.append('E')
            ops.add('E')
            weights.append(self.follow_ph(self.new_coord[0], self.new_coord[1] + 1, ph_field))
            if np.array_equal([self.new_coord[0], self.new_coord[1] + 1], food_coord):  # if food coordinate
                weights[-1] = weights[-1] * 10  # Most recently added element * 10

        # Check if the tile to the West is valid, if it is then add to valid options
        if self.new_coord[1] - 1 >= 0 and \
                [self.new_coord[0], self.new_coord[1] - 1] not in walls.blocks:         # In bounds WEST
            turn_moves.append('W')
            ops.add('W')
            weights.append(self.follow_ph(self.new_coord[0], self.new_coord[1] - 1, ph_field))
            if np.array_equal([self.new_coord[0], self.new_coord[1] - 1], food_coord):  # if food coordinate
                weights[-1] = weights[-1] * 10  # Most recently added element * 10

        # If not all the same, then triple the largest weight
        if not np.all(weights):
            greedy = np.argmax(weights)
            weights[greedy] = weights[greedy] * 3

        # Convert all weights to probabilities
        div = sum(weights)
        weights = [weight / div for weight in weights]

        # Move options for specific grid
        return turn_moves, ops, weights

    def follow_ph(self, coord1, coord2, ph_field):
        """
        Collect the ph value at the specific grid move, add 1 to it to keep it from being 0
        :param coord1: integer
        :param coord2: integer
        :param ph_field: 2D numpy array of ph values
        :return: ph_val + 1 (integer)
        """
        ph_val = ph_field[coord1][coord2]
        return ph_val + 1

    def get_distance(self, temp_coord, home_coord):
        """
        Get the absolute distance for x and y from home coord and current coord
        :param temp_coord: list of 2 coordinates
        :param home_coord: list of 2 coordinates
        :return: x (int), y (int) distances
        """
        x = abs(temp_coord[0] - home_coord[0])
        y = abs(temp_coord[1] - home_coord[1])
        return x, y

    def go_home(self, turn_moves, ph_field):
        """
        Using a heuristic function to head back home, go for moves that decrease distance from home
        :param turn_moves: list of valid move options
        :param ph_field: 2D numpy array of pheromones
        :return: homing_moves
        """
        temp = [0, 0]                       # Initialize temp
        temp2 = [0, 0]                      # Initialize 2nd temp
        homing_moves = []                   # Initialize homing moves

        temp[0] = self.new_coord[0]         # Set temp[0] to new coord
        temp[1] = self.new_coord[1]         # Set temp[1] to new coord

        for move in turn_moves:
            # Move north and collect the distance differences
            if move == 'N':
                temp2[0] = temp[0] - 1
                temp2[1] = temp[1]

                x, y = self.get_distance(temp, self.home)
                x2, y2 = self.get_distance(temp2, self.home)

                if x2 < x or y2 < y:
                    if ph_field[temp2[0]][temp2[1]] >= 0:
                        homing_moves.append(move)

            # Move east and collect the distance differences
            elif move == 'E':
                temp2[0] = temp[0]
                temp2[1] = temp[1] + 1

                x, y = self.get_distance(temp, self.home)
                x2, y2 = self.get_distance(temp2, self.home)

                if x2 < x or y2 < y:
                    if ph_field[temp2[0]][temp2[1]] >= 0:
                        homing_moves.append(move)

            # Move south and collect the distance differences
            elif move == 'S':
                temp2[0] = temp[0] + 1
                temp2[1] = temp[1]

                x, y = self.get_distance(temp, self.home)
                x2, y2 = self.get_distance(temp2, self.home)

                if x2 < x or y2 < y:
                    if ph_field[temp2[0]][temp2[1]] >= 0:
                        homing_moves.append(move)

            # Move west and collect the distance differences
            else:
                temp2[0] = temp[0]
                temp2[1] = temp[1] - 1

                x, y = self.get_distance(temp, self.home)
                x2, y2 = self.get_distance(temp2, self.home)

                if x2 < x or y2 < y:
                    if ph_field[temp2[0]][temp2[1]] >= 0:
                        homing_moves.append(move)

        # Moves ['N', 'E', 'S', 'W']
        return homing_moves

    def make_move(self, ph_field, food_coord):
        """
        Ant makes a move based on ph_field and food coord. If the ant has food head home.
        :param ph_field: 2D numpy array of pheromone values
        :param food_coord: Food coordinates
        :return: N/A
        """
        turn_moves, ops, weights = self.look_ahead(ph_field, food_coord)
        move = rand.choices(turn_moves, weights, k=1)[0]

        # if ant has food, then head home. Need to pheromone_drop pheromones...
        if self.has_food:
            # Adjust turn moves
            home_moves = self.go_home(ops, ph_field)
            if len(home_moves) > 0:
                # Verify there are move options, select randomly
                move = rand.choices(home_moves, k=1)[0]
            else:
                # Follow the lowest pheromone this time
                move = turn_moves[np.argmin(weights)]

        # Adjust to select the correct move
        if move == 'N':         # North
            self.new_coord[0] -= 1
        elif move == 'E':       # East
            self.new_coord[1] += 1
        elif move == 'S':       # South
            self.new_coord[0] += 1
        else:                   # West
            self.new_coord[1] -= 1

        # Verify that ant is in bounds:
        if self.new_coord[0] < 0 or self.new_coord[0] > self.lim_coord[0]\
                or self.new_coord[1] < 0 or self.new_coord[1] > self.lim_coord[1]:
            # Reset coordinates
            self.new_coord[0] = self.old_coord[0]
            self.new_coord[1] = self.old_coord[1]


"""
Field Class
"""
class Field:
    def __init__(self, length=5, width=5, num_ants=1):
        """
        Initialize the environment field and the ph field, ant colony as well. Generic set to 5x5 with 1 ant.
        :param length: Integer height of the plot.
        :param width: Integer width of the plot.
        :param num_ants: Integer number of ants.
        """
        self.length = length                                    # Length of field
        self.width = width                                      # Width of field
        self.colony = [0, 0]                                    # Top left corner
        self.food_collected = 0                                 # Amount of food ants collect
        self.food_coord = [self.length - 1, self.width - 1]     # Bottom right corner for now
        self.ph_env = np.zeros((self.length, self.width))       # Pheromone environment
        self.env = np.zeros((self.length, self.width))          # Environment for ants and food
        np.add.at(self.env, tuple(zip(*walls.blocks)), 4)       # Vectorized add 4 to all walls
        self.env[self.colony[0]][self.colony[1]] = 4            # Add 4 to colony coordinate location
        self.env[self.food_coord[0]][self.food_coord[1]] = 4    # Add 4 to food coordinate location
        self.num_ants = num_ants
        self.ant_colony = [Ants(ant_num, self.length, self.width, self.colony) for ant_num in range(num_ants)]

        # Update all the ants in the colony
        for ant in self.ant_colony:
            self.env[ant.new_coord[0]][ant.new_coord[1]] = 1

        # Display the initial state of the field and ph environment
        display_env_ph(self.env, self.ph_env, self.length, self.width, self.food_collected, self.num_ants, step=0)

    def time(self, step):
        """
        At every time interval, all ants must update their moves and pheromones will decay.
        :param step: Integer current steps.
        :return: N/A
        """
        # For all the ants in the colony
        for ant in self.ant_colony:
            ant.make_move(self.ph_env, self.food_coord)         # Move each of the ants
            self.env[ant.new_coord[0]][ant.new_coord[1]] += 1   # Ant moved to here, update the environment
            self.env[ant.old_coord[0]][ant.old_coord[1]] -= 1   # This ant is no longer here, update environment

            # Check if the new ant coordinate is a food coordinate
            if ant.new_coord[0] == self.food_coord[0] and ant.new_coord[1] == self.food_coord[1]:
                ant.has_food = True     # Let ant know it has food and to head home.
                self.ph_env[ant.new_coord[0]][ant.new_coord[1]] = ant.pheromone_drop    # Drop pheromones on ph env

            # Check if ant has food and if it's reached the colony
            if ant.has_food and ant.new_coord[0] == self.colony[0] and ant.new_coord[1] == self.colony[1]:
                if ant.pheromone_drop >= 2:     # If pheromone is greater than or equal to 2
                    ant.pheromone_drop -= 2     # Lower pheromone drop
                    # Drop pheromones on home base too
                    self.ph_env[ant.new_coord[0]][ant.new_coord[1]] = ant.pheromone_drop

                ant.has_food = False                                        # Deposited the food. Head out again.
                ant.pheromone_drop = int((self.length + self.width)*3)      # Reset the initial pheromone
                self.food_collected += 1                                    # Update food collection

                # Every 5 pieces of food add another ant
                if self.food_collected % 5 == 0:
                    self.num_ants += 1                  # Add another ant
                    self.ant_colony.append(Ants(self.num_ants, self.length, self.width, self.colony))

            # Only drop phermones if have food...
            if ant.has_food:
                # Decay pheromones on the way home
                if ant.pheromone_drop >= 2:
                    ant.pheromone_drop -= 2     # Reduce the pheromone drop by 2

                # Only drop if still relevant trail, pheromones greater than average of length and width
                if ant.pheromone_drop > int(self.length + self.width / 2):
                    self.ph_env[ant.new_coord[0]][ant.new_coord[1]] = ant.pheromone_drop  # Update pheromones

            # Need to manually update the old coordinates or else it just points to new coords
            ant.old_coord[0] = ant.new_coord[0]     # Update the old coordinates
            ant.old_coord[1] = ant.new_coord[1]     # Update the old coordinates

            # Prevent colony from changing value. It is set to 4 like food.
            if self.env[self.colony[0]][self.colony[1]] != 4:
                self.env[self.colony[0]][self.colony[1]] = 4

        # Reduce all pheromones by 1
        sub_ind = np.where(self.ph_env > 0)
        self.ph_env[sub_ind] -= 1     # Subtract 1 from each of these indexes

        # Call the display environments function
        display_env_ph(self.env, self.ph_env, self.length, self.width, self.food_collected, self.num_ants, step)

        # Error Check
        #print(self.env, "\n*****************")                                # Show env after the ants have moved.
        #print(self.ph_env, "\n", sub_ind, "\n-----------------------------")  # Show ph env after the ants have moved.


if __name__ == "__main__":
    # Initialize a field object
    field = Field(LENGTH, WIDTH, NUM_ANTS)

    # Loop through a time span of 500 steps
    for i in range(500):
        field.time(i)   # Update the field with every time step

    # Keep the image around
    plt.show()
