# Ant_Colony
Nature inspired AI algorithm for path finding optimization. 
The idea behind this project is that ants are able to:
1. Locate "food" in their environment.
    - Ants go out and conduct a local search in the physical environment
2. Drop "pheremones" for other ants to follow.
    - Only the best ants will drop pheromones. IE, the ants that found food will drop pheromones for others.
    - The higher the pheromones, the greater probability of going in that direction.
3. Then create the fastest path between the colony and the "food" source.

## Set Up:
* Install Pycharm
    * Set Up git respository
    * Set Project Interpreter
       * Using Python 3.7.6

* Python Modules:
    * `pip install numpy`
    * `pip install matplotlib`
    
## Notes:
* Modify global variables in Ants.py to customize runs.
* Watch how the ants run once they find the food source.

## How to run: 
* `python Ants.py`
    
## Future Steps:
* Make global variables system arguments
* Have ants collect path steps - this is maybe...
* New heuristic to get ants out of death circle...
    * implement ant lifespan
* Implement maze function in the Wall class
* Allow ants to move diagonally (8 degrees of motion instead of 4)
    
## Resources:
* Dynamic Matplotlib
    - https://block.arch.ethz.ch/blog/2016/08/dynamic-plotting-with-matplotlib/
* Adding & adjusting grid
    - https://stackoverflow.com/questions/38973868/adjusting-gridlines-and-ticks-in-matplotlib-imshow
* Multiple Charts
    - https://stackoverflow.com/questions/46615554/how-to-display-multiple-images-in-one-figure-correctly    
* Update pheromones with np where
    - https://stackoverflow.com/questions/44810755/subtracting-a-number-from-an-array-if-condition-is-met-python
* Random weighted choice
    - https://pynative.com/python-random-choice/
* Vectorized add 4 to all walls 
    - https://stackoverflow.com/questions/55176269/list-of-xy-coordinates-to-matrix
    - https://docs.scipy.org/doc/numpy/reference/generated/numpy.ufunc.at.html
* Select random coordinates
    - https://docs.scipy.org/doc/numpy-1.15.1/reference/generated/numpy.random.randint.html
* Convert to list
    - https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.tolist.html
    